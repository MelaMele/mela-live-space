import os
import sqlite3
import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Mela Space - Ultimate Video & Voice Ecosystem")

# 📱 የባለቤትነት መብት እና መለያዎች
MY_TELEBIRR_NUMBER = "0913064239"  
MY_NAME = "Melaku Mebrate Tekle"         

# 🤖 የቴሌግራም ኮንፊገሬሽን
TELEGRAM_BOT_TOKEN = "8708757199:AAFWfFy9ujnZdXEJ2h6CYfzzqh_z27-_kDo"  
ADMIN_CHAT_ID = "1065443252"               

# ⚠️ Vercel (Serverless) ላይ ዳታ መጻፍ እንዲችል የዲቢ ቦታውን ወደ /tmp መቀየር
DB_FILE = "/tmp/mela_space_pro.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id TEXT PRIMARY KEY,
            username TEXT,
            coins INTEGER DEFAULT 350,
            referred_by TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id TEXT,
            tx_type TEXT,
            amount INTEGER,
            reference_id TEXT,
            status TEXT DEFAULT 'PENDING'
        )
    """)
    conn.commit()
    conn.close()

init_db()

# 📦 ፒዳንቲክ ሞዴሎች (Data Schemas)
class UserRegistration(BaseModel):
    telegram_id: str
    username: str
    referred_by: Optional[str] = None

class CoinPurchase(BaseModel):
    telegram_id: str
    amount_coins: int
    telebirr_tx_id: str

class CashOutRequest(BaseModel):
    telegram_id: str
    coins_to_cash: int
    telebirr_phone: str

# ✉️ የቴሌግራም መልዕክት መላኪያ (አዝራር/Button እንዲቀበል ተደርጎ የተሻሻለ)
def send_telegram_message(chat_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id, 
        "text": text, 
        "parse_mode": "HTML"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
        
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print("Telegram Push Failed:", e)

# --- 🎯 የቴሌግራም ዌብሁክ መቀበያ መስመር (Webhook Endpoint) ---
@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        update = await request.json()
        if "message" in update and "text" in update["message"]:
            msg = update["message"]
            chat_id = str(msg["chat"]["id"])
            text = msg["text"].strip()
            user_first_name = msg["from"].get("first_name", "ተጠቃሚ")

            # 🔗 የሪፈራል /start ትዕዛዝ አያያዝ
            if text.startswith("/start"):
                ref_id = None
                if " " in text:
                    ref_parts = text.split(" ")
                    if len(ref_parts) > 1 and ref_parts[1].startswith("ref_"):
                        ref_id = ref_parts[1].replace("ref_", "")

                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()
                cursor.execute("SELECT coins FROM users WHERE telegram_id = ?", (chat_id,))
                user_exists = cursor.fetchone()

                if not user_exists:
                    cursor.execute("INSERT INTO users (telegram_id, username, coins, referred_by) VALUES (?, ?, ?, ?)",
                                   (chat_id, user_first_name, 350, ref_id))
                    if ref_id and ref_id != chat_id:
                        cursor.execute("UPDATE users SET coins = coins + 20 WHERE telegram_id = ?", (ref_id,))
                        cursor.execute("INSERT INTO transactions (telegram_id, tx_type, amount, status) VALUES (?, 'REFERRAL_BONUS', 20, 'SUCCESS')", (ref_id,))
                        send_telegram_message(ref_id, f"🎉 <b>የሪፈራል ስጦታ!</b>\n\n👤 {user_first_name} በእርስዎ ሊንክ ስለተቀላቀለ 20 ነፃ 🪙 ዋሌትዎ ላይ ተጨምሯል!")
                    conn.commit()
                conn.close()

                welcome_text = f"👋 ሰላም {user_first_name}!\n\nእንኳን ወደ <b>Mela Space</b> መጡ።\n\n🎁 ለመጀመሪያ ጊዜ ስለገቡ <b>350 የ Mela ኮይኖች</b> በነፃ ተበርክቶልዎታል።\n\n🔗 <b>ያንተ የሪፈራል ሊንክ፦</b>\n<code>https://t.me/MelaLiveAudioVideoChat_bot?start=ref_{chat_id}</code>\n\n🎙️ አሁኑኑ ክፍሎችን ለመቀላቀል ከታች ያለውን መተግበሪያ ይክፈቱ!"
                
                # 📱 አፑን በቀጥታ የሚከፍተው የቴሌግራም inline ቁልፍ
                app_button = {
                    "inline_keyboard": [[
                        {
                            "text": "🎙️ Open Mela Space (አፑን ክፈት)",
                            "web_app": {"url": "https://mela-live-space.vercel.app"} 
                        }
                    ]]
                }
                
                send_telegram_message(chat_id, welcome_text, reply_markup=app_button)

            # 🛠️ ለአስተዳዳሪው የሚሰሩ የትዕዛዝ ቁልፎች (Admin Approval)
            elif chat_id == ADMIN_CHAT_ID:
                if text.startswith("/approve_deposit"):
                    parts = text.split("_")
                    if len(parts) >= 4:
                        target_id = parts[2]
                        amount = int(parts[3])
                        conn = sqlite3.connect(DB_FILE)
                        cursor = conn.cursor()
                        cursor.execute("UPDATE users SET coins = coins + ? WHERE telegram_id = ?", (amount, target_id))
                        conn.commit()
                        conn.close()
                        send_telegram_message(ADMIN_CHAT_ID, f"✅ ተጠቃሚ {target_id} በስኬት {amount} ኮይን ገብቶለታል።")
                        send_telegram_message(target_id, f"💳 <b>የክፍያ ማረጋገጫ!</b>\n\nበቴሌብር የገዙት <b>{amount} 🪙</b> ዋሌትዎ ላይ በስኬት ተጨምሯል!")
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- 🌐 የባክአንድ ኤፒአይ ኤንድፖይንቶች (FastAPI REST Engine) ---

@app.post("/api/register")
def register_user(user: UserRegistration):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT coins FROM users WHERE telegram_id = ?", (user.telegram_id,))
    row = cursor.fetchone()
    
    if row:
        current_coins = row[0]
        conn.close()
        return {"status": "exists", "telegram_id": user.telegram_id, "coins": current_coins}
    
    initial_coins = 350
    cursor.execute("INSERT INTO users (telegram_id, username, coins, referred_by) VALUES (?, ?, ?, ?)",
                   (user.telegram_id, user.username, initial_coins, user.referred_by))
    conn.commit()
    conn.close()
    return {"status": "created", "telegram_id": user.telegram_id, "coins": initial_coins}

@app.get("/api/wallet/{telegram_id}")
def get_wallet_balance(telegram_id: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT coins, username FROM users WHERE telegram_id = ?", (telegram_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return {"telegram_id": telegram_id, "username": "እንግዳ", "coins": 350}
    return {"telegram_id": telegram_id, "username": row[1], "coins": row[0]}

@app.post("/api/purchase-coins")
def purchase_coins(data: CoinPurchase):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (telegram_id, tx_type, amount, reference_id, status) VALUES (?, 'TELEBIRR_DEPOSIT', ?, ?, 'PENDING')",
                   (data.telegram_id, data.amount_coins, data.telebirr_tx_id))
    conn.commit()
    conn.close()
    
    admin_msg = f"💳 <b>አዲስ የኮይን ግዢ ጥያቄ!</b>\n\n👤 ተጠቃሚ ID: <code>{data.telegram_id}</code>\n🪙 የኮይን መጠን: {data.amount_coins}\n🧾 Telebirr TX ID: <code>{data.telebirr_tx_id}</code>\n\nለማጽደቅ፦ <code>/approve_deposit_{data.telegram_id}_{data.amount_coins}</code>"
    send_telegram_message(ADMIN_CHAT_ID, admin_msg)
    return {"status": "submitted", "message": "የክፍያ ጥያቄዎ ለአስተዳዳሪው ተልኳል፤ ሲረጋገጥ ኮይኑ ይገባል!"}

@app.post("/api/cash-out")
def cash_out_tokens(data: CashOutRequest):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT coins FROM users WHERE telegram_id = ?", (data.telegram_id,))
    row = cursor.fetchone()
    
    if not row or row[0] < data.coins_to_cash:
        conn.close()
        raise HTTPException(status_code=400, detail="ለማውጣት የጠየቁት ኮይን ከባላንስዎ ይበልጣል!")
        
    cursor.execute("UPDATE users SET coins = coins - ? WHERE telegram_id = ?", (data.coins_to_cash, data.telegram_id))
    cursor.execute("INSERT INTO transactions (telegram_id, tx_type, amount, reference_id, status) VALUES (?, 'CASH_OUT', ?, ?, 'PENDING')",
                   (data.telegram_id, data.coins_to_cash, data.telebirr_phone))
    conn.commit()
    conn.close()
    
    admin_msg = f"💸 <b>የገንዘብ ማውጫ (Cash-Out) ጥያቄ!</b>\n\n👤 ተጠቃሚ ID: <code>{data.telegram_id}</code>\n🪙 የደረሰ ኮይን: {data.coins_to_cash}\n📱 የቴሌብር ስልክ: {data.telebirr_phone}"
    send_telegram_message(ADMIN_CHAT_ID, admin_msg)
    return {"status": "success", "message": "የመውጫ ጥያቄዎ ተመዝግቧል፤ በቅርቡ በቴሌብር ይላክልዎታል!"}

# --- 🖥️ ዋናው የፊት-ለፊት (UI HTML) ገጽ ---
@app.get("/", response_class=HTMLResponse)
async def get_index():
    html_content = f"""
    <!DOCTYPE html>
    <html lang="am">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Mela Ultimate Pro Space - Created by {MY_NAME}</title>
        <script src="https://download.agora.io/sdk/release/AgoraRTC_N-4.18.0.js"></script>
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Roboto, sans-serif; }}
            body, html {{ width: 100%; height: 100%; overflow: hidden; background: #060713; color: #fff; }}
            .bg-glow {{ position: absolute; width: 300px; height: 300px; background: radial-gradient(circle, rgba(37,244,238,0.15) 0%, rgba(0,0,0,0) 70%); top: -50px; left: -50px; z-index: 1; pointer-events: none; }}
            .bg-glow-right {{ position: absolute; width: 300px; height: 300px; background: radial-gradient(circle, rgba(254,44,85,0.12) 0%, rgba(0,0,0,0) 70%); bottom: 50px; right: -50px; z-index: 1; pointer-events: none; }}
            .lobby-container {{ position: absolute; top:0; left:0; width:100%; height:calc(100% - 70px); background:#060713; z-index:500; display:flex; flex-direction:column; padding:20px; overflow-y:auto; }}
            .lobby-header {{ text-align:center; margin: 10px 0; z-index: 2; }}
            .lobby-title {{ color:#25f4ee; font-size:26px; font-weight:900; text-shadow: 0 0 20px rgba(37,244,238,0.6); }}
            .create-room-box {{ background: rgba(22, 23, 34, 0.7); backdrop-filter: blur(10px); border:1px solid rgba(255,255,255,0.07); border-radius:20px; padding:20px; margin-bottom:20px; box-shadow: 0 8px 32px rgba(0,0,0,0.3); z-index: 2; }}
            .input-field {{ width:100%; background: rgba(47, 48, 61, 0.6); border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:12px; color:white; font-size:14px; margin-bottom:12px; outline:none; }}
            .btn-3d {{ width:100%; background: linear-gradient(135deg, #fe2c55, #ff5574); border: none; color: white; padding: 14px; border-radius: 14px; font-weight: bold; font-size: 16px; cursor: pointer; box-shadow: 0 5px 0px #b01c3a, 0 8px 20px rgba(254,44,85,0.4); transition: all 0.1s ease; transform: translateY(0px); }}
            .btn-3d:active {{ transform: translateY(4px); box-shadow: 0 1px 0px #b01c3a, 0 4px 10px rgba(254,44,85,0.3); }}
            .room-list-title {{ font-size:15px; color:#888; margin-bottom:12px; font-weight:bold; z-index: 2; }}
            .room-item {{ background: rgba(22, 23, 34, 0.6); border:1px solid rgba(255,255,255,0.05); padding:15px; border-radius:16px; display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; cursor:pointer; z-index: 2; }}
            .tab-screen {{ display:none; position:absolute; top:0; left:0; width:100%; height:calc(100% - 70px); background:#060713; z-index:400; padding:20px; overflow-y:auto; }}
            .bottom-nav {{ position:absolute; bottom:0; left:0; width:100%; height:70px; background: rgba(22, 23, 34, 0.85); backdrop-filter: blur(15px); border-top:1px solid rgba(255,255,255,0.06); display:flex; justify-content:space-around; align-items:center; z-index:1000; }}
            .nav-item {{ display:flex; flex-direction:column; align-items:center; color:#666b86; font-size:11px; font-weight:600; cursor:pointer; }}
            .nav-item.active {{ color:#25f4ee; }}
            .nav-icon {{ font-size:22px; margin-bottom:4px; }}
            .meta-tag {{ font-size: 10px; color: #444; text-align: center; margin-top: 10px; }}
        </style>
    </head>
    <body>
        <div class="bg-glow"></div>
        <div class="bg-glow-right"></div>

        <div class="bottom-nav" id="main-nav-bar">
            <div class="nav-item active" id="nav-home" onclick="switchTab('home')">
                <div class="nav-icon">🎙️</div>
                <div>ክፍሎች</div>
            </div>
            <div class="nav-item" id="nav-wallet" onclick="switchTab('wallet')">
                <div class="nav-icon">👛</div>
                <div>ዋሌት</div>
            </div>
            <div class="nav-item" id="nav-ref" onclick="switchTab('referral')">
                <div class="nav-icon">🔗</div>
                <div>ሪፈራል</div>
            </div>
        </div>

        <div class="lobby-container" id="lobby-screen">
            <div class="lobby-header"><div class="lobby-title">Mela Live Rooms</div></div>
            <div class="create-room-box">
                <input type="text" id="lobby-tg-id" class="input-field" placeholder="የቴሌግራም መለያ ቁጥር (ID) ያስገቡ...">
                <input type="text" id="lobby-username" class="input-field" placeholder="የእርስዎን ስም ያስገቡ...">
                <input type="text" id="lobby-roomname" class="input-field" placeholder="የክፍሉን ስም ያስገቡ...">
                <button class="btn-3d" onclick="createNewRoomAction()">🚀 አዲስ ክፍል ፍጠር</button>
            </div>
            <div class="room-list-title">🟢 የቀጥታ ውይይት ክፍሎች</div>
            <div id="active-rooms-list">
                <div class="room-item">
                    <div><div style="font-weight:bold; color:#ffdd67; font-size:15px;">🌍 Mela Diaspora Lounge</div></div>
                    <div style="color:#25f4ee; font-size:12px; font-weight:bold;">🎙️ ግባ</div>
                </div>
            </div>
            <div class="meta-tag">Created by: {MY_NAME}</div>
        </div>

        <script>
            function switchTab(tab) {{
                document.getElementById('lobby-screen').style.display = (tab === 'home') ? 'flex' : 'none';
                document.getElementById('wallet-screen').style.display = (tab === 'wallet') ? 'block' : 'none';
                document.getElementById('referral-screen').style.display = (tab === 'referral') ? 'block' : 'none';
            }}
            function createNewRoomAction() {{ alert('ክፍል የመፍጠር ስራ በቅርቡ ዝግጁ ይሆናል!'); }}
        </script>
    </body>
    </html>
    """
    return html_content
