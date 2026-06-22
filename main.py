import os
import requests
import threading
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Mela Space - Ultimate Video & Voice Ecosystem")

# 📱 የባለቤትነት መብት እና መለያዎች
MY_TELEBIRR_NUMBER = "0913064239"  
MY_NAME = "Melaku Mebrate Tekle"         

# 🤖 የቴሌግራም ኮንፊገሬሽን
TELEGRAM_BOT_TOKEN = "8327536456:AAHn6AqMUIayCjUUTF5up8cICR_4BvjbiKs"  
ADMIN_CHAT_ID = "1065443252"               

# 📂 ዳታቤዝ-አልባ የIn-Memory መዋቅር (Vercel ወይም ማናቸውም ሰርቨር ላይ እንዳይበላሽ)
USERS_MEMORY = {}

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

# --- 🤖 የቴሌግራም ቦት ጀርባ ሰራተኛ (Telegram Bot Engine) ---
def push_bot_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"}, timeout=5)
    except Exception as e:
        print("Bot Notification Error:", e)

def run_telegram_polling():
    offset = 0
    print("🤖 Mela Telegram Bot successfully hooked and running...")
    while True:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates?offset={offset}&timeout=10"
            updates = requests.get(url, timeout=12).json()
            if "result" in updates:
                for update in updates["result"]:
                    offset = update["update_id"] + 1
                    if "message" in update and "text" in update["message"]:
                        msg = update["message"]
                        chat_id = str(msg["chat"]["id"])
                        text = msg["text"].strip()
                        first_name = msg["from"].get("first_name", "ተጠቃሚ")

                        if text.startswith("/start"):
                            ref_id = None
                            if " " in text:
                                parts = text.split(" ")
                                if len(parts) > 1 and parts[1].startswith("ref_"):
                                    ref_id = parts[1].replace("ref_", "")

                            if chat_id not in USERS_MEMORY:
                                USERS_MEMORY[chat_id] = {"username": first_name, "coins": 350}
                                if ref_id and ref_id in USERS_MEMORY and ref_id != chat_id:
                                    USERS_MEMORY[ref_id]["coins"] += 20
                                    push_bot_message(ref_id, f"🎉 <b>የሪፈራል ስጦታ!</b>\n\n👤 {first_name} በእርስዎ ሊንክ ስለገባ 20 ነፃ 🪙 ተጨምሮልዎታል!")

                            welcome_msg = f"👋 ሰላም {first_name}!\n\nእንኳን ወደ <b>Mela Space</b> በሰላም መጡ።\n\n🎁 መተግበሪያውን ስለከፈቱ <b>350 ነፃ ኮይኖች</b> ተሰጥተውዎታል።\n\n🔗 <b>የእርስዎ መጋበዣ (Referral) ሊንክ፦</b>\n<code>https://t.me/MelaSpaceBot?start=ref_{chat_id}</code>"
                            push_bot_message(chat_id, welcome_msg)
        except Exception as e:
            time.sleep(2)

# ቦቱን ከFastAPI ጎን ለጎን ማስነሳት
threading.Thread(target=run_telegram_polling, daemon=True).start()

# --- 🌐 የባክአንድ ኤፒአይ ኤንድፖይንቶች ---

@app.post("/api/register")
def register_user(user: UserRegistration):
    tg_id = user.telegram_id
    if tg_id in USERS_MEMORY:
        return {"status": "exists", "telegram_id": tg_id, "coins": USERS_MEMORY[tg_id]["coins"]}
    
    USERS_MEMORY[tg_id] = {"username": user.username, "coins": 350}
    if user.referred_by and user.referred_by in USERS_MEMORY and user.referred_by != tg_id:
        USERS_MEMORY[user.referred_by]["coins"] += 20
    return {"status": "created", "telegram_id": tg_id, "coins": 350}

@app.get("/api/wallet/{telegram_id}")
def get_wallet_balance(telegram_id: str):
    if telegram_id not in USERS_MEMORY:
        USERS_MEMORY[telegram_id] = {"username": "እንግዳ", "coins": 350}
    return {"telegram_id": telegram_id, "username": USERS_MEMORY[telegram_id]["username"], "coins": USERS_MEMORY[telegram_id]["coins"]}

@app.post("/api/purchase-coins")
def purchase_coins(data: CoinPurchase):
    admin_msg = f"💳 <b>አዲስ የቴሌብር ክፍያ ጥያቄ!</b>\n\n👤 ተጠቃሚ ID: <code>{data.telegram_id}</code>\n🪙 መጠን: {data.amount_coins}\n🧾 TX ID: <code>{data.telebirr_tx_id}</code>"
    push_bot_message(ADMIN_CHAT_ID, admin_msg)
    return {"status": "submitted", "message": "የክፍያ ጥያቄዎ ለአስተዳዳሪው ተልኳል፤ ሲረጋገጥ ኮይኑ ይገባል!"}

@app.post("/api/cash-out")
def cash_out_tokens(data: CashOutRequest):
    tg_id = data.telegram_id
    if tg_id in USERS_MEMORY and USERS_MEMORY[tg_id]["coins"] >= data.coins_to_cash:
        USERS_MEMORY[tg_id]["coins"] -= data.coins_to_cash
        admin_msg = f"💸 <b>የካሽ አውት ጥያቄ!</b>\n\n👤 ተጠቃሚ ID: <code>{tg_id}</code>\n🪙 ኮይን: {data.coins_to_cash}\n📱 ስልክ: {data.telebirr_phone}"
        push_bot_message(ADMIN_CHAT_ID, admin_msg)
        return {"status": "success", "message": "የመውጫ ጥያቄዎ ተመዝግቧል!"}
    raise HTTPException(status_code=400, detail="በቂ ኮይን የለዎትም!")

@app.get("/", response_class=HTMLResponse)
async def get_index():
    html_content = f"""
    <!DOCTYPE html>
    <html lang="am">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Mela Ultimate Pro Space - Created by Melaku Mebrate Tekle</title>
        
        <script src="https://download.agora.io/sdk/release/AgoraRTC_N-4.18.0.js"></script>
        
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Roboto, sans-serif; }}
            body, html {{ width: 100%; height: 100%; overflow: hidden; background: #060713; color: #fff; }}
            
            /* ✨ የጀርባ ኒዮን ማብሪያዎች */
            .bg-glow {{ position: absolute; width: 300px; height: 300px; background: radial-gradient(circle, rgba(37,244,238,0.15) 0%, rgba(0,0,0,0) 70%); top: -50px; left: -50px; z-index: 1; pointer-events: none; }}
            .bg-glow-right {{ position: absolute; width: 300px; height: 300px; background: radial-gradient(circle, rgba(254,44,85,0.12) 0%, rgba(0,0,0,0) 70%); bottom: 50px; right: -50px; z-index: 1; pointer-events: none; }}

            /* 🚪 ሎቢ ገጽ */
            .lobby-container {{ position: absolute; top:0; left:0; width:100%; height:calc(100% - 70px); background:#060713; z-index:500; display:flex; flex-direction:column; padding:20px; overflow-y:auto; }}
            .lobby-header {{ text-align:center; margin: 10px 0; z-index: 2; }}
            .lobby-title {{ color:#25f4ee; font-size:26px; font-weight:900; text-shadow: 0 0 20px rgba(37,244,238,0.6); }}
            
            .create-room-box {{ background: rgba(22, 23, 34, 0.7); backdrop-filter: blur(10px); border:1px solid rgba(255,255,255,0.07); border-radius:20px; padding:20px; margin-bottom:20px; box-shadow: 0 8px 32px rgba(0,0,0,0.3); z-index: 2; }}
            .input-field {{ width:100%; background: rgba(47, 48, 61, 0.6); border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:12px; color:white; font-size:14px; margin-bottom:12px; outline:none; }}
            
            .checkbox-container {{ display: flex; align-items: center; gap: 8px; margin-bottom: 12px; font-size: 13px; color: #aaa; }}
            
            /* 🔥 3D በተኖች */
            .btn-3d {{ 
                width:100%; 
                background: linear-gradient(135deg, #fe2c55, #ff5574); 
                border: none; 
                color: white; 
                padding: 14px; 
                border-radius: 14px; 
                font-weight: bold; 
                font-size: 16px; 
                cursor: pointer; 
                box-shadow: 0 5px 0px #b01c3a, 0 8px 20px rgba(254,44,85,0.4);
                transition: all 0.1s ease;
                transform: translateY(0px);
            }}
            .btn-3d:active {{ transform: translateY(4px); box-shadow: 0 1px 0px #b01c3a, 0 4px 10px rgba(254,44,85,0.3); }}
            
            .room-list-title {{ font-size:15px; color:#888; margin-bottom:12px; font-weight:bold; z-index: 2; }}
            .room-item {{ background: rgba(22, 23, 34, 0.6); border:1px solid rgba(255,255,255,0.05); padding:15px; border-radius:16px; display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; cursor:pointer; z-index: 2; }}

            /* 🗂️  ታብ ገፆች */
            .tab-screen {{ display:none; position:absolute; top:0; left:0; width:100%; height:calc(100% - 70px); background:#060713; z-index:400; padding:20px; overflow-y:auto; }}
            .page-title {{ font-size:24px; font-weight:800; color:#25f4ee; margin-bottom:20px; text-align:center; }}
            .info-card {{ background: rgba(22, 23, 34, 0.7); border:1px solid rgba(255,255,255,0.06); border-radius:20px; padding:20px; margin-bottom:15px; text-align:center; }}
            
            /* 🎙️ 🎬 ዋናው የውስጥ ሩም (ቪዲዮ የሚታይበት ክልል ጨምሮ) */
            .app-container {{ display: none; position: relative; width: 100%; height: 100%; flex-direction: column; background: #060713; }}
            .top-bar {{ display: flex; justify-content: space-between; align-items: center; padding: 12px 20px; border-bottom: 1px solid rgba(255,255,255,0.05); z-index: 10; }}
            .live-tag {{ background: linear-gradient(45deg, #fe2c55, #ff0033); padding: 5px 12px; border-radius: 20px; font-weight: 800; font-size: 11px; }}
            .room-name-display {{ font-size:13px; font-weight:bold; color:#25f4ee; background:rgba(37,244,238,0.15); border: 1px solid rgba(37,244,238,0.2); padding:5px 12px; border-radius:20px; }}
            
            .voice-counter-badge {{ background: rgba(0, 205, 99, 0.2); border: 1px solid #00cd63; color: #00ff7f; font-size: 12px; font-weight: bold; padding: 4px 10px; border-radius: 12px; display: none; }}

            /* 📺 የቪዲዮ ማሳያ መስኮት (Video Stage) */
            .video-stage-container {{ width: 90%; height: 130px; background: #11121e; margin: 5px auto; border-radius: 16px; border: 1px solid rgba(255,255,255,0.08); overflow: hidden; position: relative; display: flex; justify-content: center; align-items: center; }}
            .video-stream-view {{ width: 100%; height: 100%; background: #000; }}
            .video-placeholder-text {{ position: absolute; font-size: 12px; color: #555; pointer-events: none; }}

            .stage-area {{ flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; padding: 5px; z-index: 5; overflow-y: auto; }}
            .host-section {{ text-align: center; margin-bottom: 8px; position: relative; }}
            .host-avatar {{ width: 60px; height: 60px; border-radius: 50%; background: #111; border: 3px solid #fe2c55; display: flex; align-items: center; justify-content: center; font-size: 28px; margin: 0 auto 3px auto; box-shadow: 0 0 15px rgba(254,44,85,0.3); }}
            .host-badge {{ position: absolute; top: 0; right: 5px; background: #ffdd67; color: #000; font-size: 9px; padding: 2px 5px; border-radius: 10px; font-weight: bold; }}

            /* 🪑 የመቀመጫ ግሪዶች */
            .seats-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; width: 100%; max-width: 360px; margin-bottom: 5px; }}
            .seat-circle {{ width: 46px; height: 46px; border-radius: 50%; background: #161722; border: 2px solid #25f4ee; display: flex; align-items: center; justify-content: center; font-size: 16px; margin: 0 auto 3px auto; cursor: pointer; position: relative; }}
            .seat-circle.empty {{ border-color: rgba(255,255,255,0.15); background: rgba(255,255,255,0.03); color: #555; }}
            .seat-name {{ font-size: 11px; color: #bbb; text-align:center; }}

            /* 🎛️ የመቆጣጠሪያ ቁልፎች */
            .utility-bar {{ display: flex; flex-direction: column; gap: 6px; width: 100%; background: rgba(255,255,255,0.02); padding: 8px; border-top: 1px solid rgba(255,255,255,0.05); border-bottom: 1px solid rgba(255,255,255,0.05); z-index: 10; }}
            .button-row {{ display: flex; justify-content: space-around; width: 100%; gap: 5px; flex-wrap: wrap; }}
            
            .util-btn-3d {{ 
                background: rgba(22, 23, 34, 0.8); 
                border: 1px solid rgba(255,255,255,0.1); 
                color: white; 
                padding: 6px 8px; 
                border-radius: 10px; 
                font-size: 11px; 
                font-weight: bold; 
                cursor: pointer; 
                flex: 1; 
                min-width: 70px; 
                text-align: center;
                box-shadow: 0 3px 0px rgba(0,0,0,0.5);
                transition: all 0.05s ease;
            }}
            .util-btn-3d:active {{ transform: translateY(2px); box-shadow: 0 1px 0px rgba(0,0,0,0.5); }}

            .slider-fx-container {{ display: flex; flex-direction: column; gap: 6px; width: 95%; margin: 0 auto; }}
            .volume-control-box {{ display: flex; align-items: center; justify-content: center; gap: 10px; font-size: 11px; color: #aaa; }}
            .volume-slider {{ flex: 1; -webkit-appearance: none; background: rgba(255,255,255,0.1); height: 5px; border-radius: 3px; outline: none; }}
            .volume-slider::-webkit-slider-thumb {{ -webkit-appearance: none; appearance: none; width: 14px; height: 14px; border-radius: 50%; background: #25f4ee; cursor: pointer; }}

            /* 💬 የቀጥታ ቻት ክልል */
            .chat-area {{ height: 95px; width: 100%; padding: 10px; background: linear-gradient(transparent, rgba(6,7,19,0.98)); overflow-y: auto; font-size: 12px; display: flex; flex-direction: column; gap: 5px; z-index: 10; scroll-behavior: smooth; }}
            
            /* ✍️ የፅሁፍ መፃፊያ ባር */
            .chat-input-container {{ display: flex; padding: 8px 15px; background: #0b0c1e; border-top: 1px solid rgba(255,255,255,0.05); z-index: 12; gap: 10px; align-items: center; }}
            .chat-input {{ flex: 1; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 10px 15px; color: #fff; font-size: 13px; outline: none; }}
            .btn-send-text {{ background: #25f4ee; border: none; color: #060713; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; cursor: pointer; }}

            .bottom-controls {{ display: flex; justify-content: space-between; align-items: center; padding: 10px 20px; background: #060713; z-index: 10; border-top: 1px solid rgba(255,255,255,0.05); }}
            
            /* 🧭 የታችኛው ዋና ሜኑ */
            .bottom-nav {{ position:absolute; bottom:0; left:0; width:100%; height:70px; background: rgba(22, 23, 34, 0.85); backdrop-filter: blur(15px); border-top:1px solid rgba(255,255,255,0.06); display:flex; justify-content:space-around; align-items:center; z-index:1000; }}
            .nav-item {{ display:flex; flex-direction:column; align-items:center; color:#666b86; font-size:11px; font-weight:600; cursor:pointer; }}
            .nav-item.active {{ color:#25f4ee; }}
            .nav-icon {{ font-size:22px; margin-bottom:4px; }}

            /* 🎁 የስጦታዎች Overlay */
            .gift-overlay {{ display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.7); z-index:2000; align-items:flex-end; }}
            .gift-tray {{ width:100%; background:#10111e; border-top: 2px solid rgba(255,255,255,0.1); border-radius:24px 24px 0 0; padding:20px; }}
            .gift-grid {{ display:grid; grid-template-columns: repeat(4, 1fr); gap:12px; margin-bottom: 15px; }}
            .gift-card {{ background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05); border-radius:16px; padding:12px 5px; text-align:center; cursor:pointer; position: relative; }}
            .gift-emoji {{ font-size:30px; margin-bottom:5px; }}
            .gift-cost {{ font-size:11px; color:#ffdd67; font-weight:bold; }}
            
            .combo-badge {{ position: absolute; top: -8px; right: -8px; background: linear-gradient(45deg, #ff007f, #fe2c55); color: white; border-radius: 50%; width: 22px; height: 22px; font-size: 11px; display: flex; align-items: center; justify-content: center; font-weight: 900; box-shadow: 0 0 10px #fe2c55; display: none; }}

            /* 🎡 Wheel UI */
            .wheel-box {{ width: 100%; background: #10111e; padding: 25px; border-radius: 24px 24px 0 0; text-align: center; color: white; }}
            .wheel-graphic {{ width: 160px; height: 160px; border-radius: 50%; border: 8px solid #25f4ee; margin: 15px auto; display: flex; align-items: center; justify-content: center; font-size: 40px; font-weight: bold; background: conic-gradient(#fe2c55 0% 25%, #00ff7f 25% 50%, #00bfff 50% 75%, #ffdd67 75% 100%); transition: transform 3s cubic-bezier(0.1, 0.8, 0.1, 1); }}

            /* 🎬 አኒሜሽን ንብርብር */
            .cinematic-stage {{ display:none; position:fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:2500; align-items:center; justify-content:center; }}
            .big-gift-anim {{ font-size:120px; animation: cinematicBlast 1.2s forwards cubic-bezier(0.175, 0.885, 0.32, 1.275); }}
            @keyframes cinematicBlast {{
                0% {{ transform: scale(0) rotate(-45deg); opacity: 0; }}
                30% {{ transform: scale(1.5) rotate(15deg); opacity: 1; text-shadow: 0 0 40px #ff007f; }}
                50% {{ transform: scale(1) rotate(0deg); }}
                100% {{ opacity: 0; transform: scale(0.5) translateY(-200px); }}
            }}
            
            .meta-tag {{ font-size: 10px; color: #444; text-align: center; margin-top: 10px; }}
        </style>
    </head>
    <body>

        <div class="bg-glow"></div>
        <div class="bg-glow-right"></div>

        <audio id="bg-kirar-audio" loop crossOrigin="anonymous">
            <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mp3">
        </audio>
        <audio id="snd-applause" crossOrigin="anonymous">
            <source src="https://www.soundjay.com/human/sounds/applause-01.mp3" type="audio/mp3">
        </audio>
        <audio id="snd-laughter" crossOrigin="anonymous">
            <source src="https://www.soundjay.com/human/sounds/laughter-01.mp3" type="audio/mp3">
        </audio>

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
                <div class="checkbox-container">
                    <input type="checkbox" id="lobby-is-vip">
                    <label for="lobby-is-vip">🔒 እንደ VIP (የግል ሚስጥራዊ ክፍል) ፍጠር</label>
                </div>
                <button class="btn-3d" onclick="createNewRoomAction()">🚀 አዲስ ክፍል ፍጠር</button>
                <button class="util-btn-3d" style="width:100%; margin-top:12px; border-color:#00ff7f; color:#00ff7f;" onclick="openWheelModal()">🎡 ዕለታዊ ዕድል ማሽከርከሪያ (Daily Wheel)</button>
            </div>

            <div class="room-list-title">🟢  የቀጥታ ውይይት ክፍሎች</div>
            <div id="active-rooms-list">
                <div class="room-item" onclick="joinExistingRoom('🌍 የስደት ወግ (Diaspora Lounge)')">
                    <div>
                        <div style="font-weight:bold; color:#ffdd67; font-size:15px;">🌍 የስደት ወግ (Diaspora Lounge) ⭐</div>
                        <div style="font-size:12px; color:#aaa; margin-top:3px;">የስደት ህይወትና የናፍቆት ወግ መጋሪያ አዳራሽ</div>
                    </div>
                    <div style="color:#25f4ee; font-size:12px; font-weight:bold; background:rgba(37,244,238,0.1); padding:6px 12px; border-radius:12px;">🎙️ ግባ</div>
                </div>

                <div class="room-item" onclick="joinExistingRoom('🤱 የእናቶች ወግ (Mothers Lounge)')">
                    <div>
                        <div style="font-weight:bold; color:#ff7ebb; font-size:15px;">🤱 የእናቶች ወግ (Mothers Lounge) 💕</div>
                        <div style="font-size:12px; color:#aaa; margin-top:3px;">ስለ ህፃናት አስተዳደግና የቤት ውስጥ ምክረ-ሃሳቦች መወያያ</div>
                    </div>
                    <div style="color:#25f4ee; font-size:12px; font-weight:bold; background:rgba(37,244,238,0.1); padding:6px 12px; border-radius:12px;">🎙️ ግባ</div>
                </div>

                <div class="room-item" onclick="joinExistingRoom('⚽ የካስ ጨዋታ መወያያ (Football Hub)')">
                    <div>
                        <div style="font-weight:bold; color:#00cd63; font-size:15px;">⚽ የካስ ጨዋታ መወያያ (Football Hub) 🏆</div>
                        <div style="font-size:12px; color:#aaa; margin-top:3px;">የአውሮፓና የሀገር ውስጥ እግር ኳስ ትንተናዎችና ጭቅጭቆች</div>
                    </div>
                    <div style="color:#25f4ee; font-size:12px; font-weight:bold; background:rgba(37,244,238,0.1); padding:6px 12px; border-radius:12px;">🎙️ ግባ</div>
                </div>

                <div class="room-item" onclick="joinExistingRoom('📚 የተማሪዎች ውይይት (Students Circle)')">
                    <div>
                        <div style="font-weight:bold; color:#00bfff; font-size:15px;">📚 የተማሪዎች ውይይት (Students Circle) 🎓</div>
                        <div style="font-size:12px; color:#aaa; margin-top:3px;">የትምህርት እገዛ፣ የፈተና ዝግጅትና የዩኒቨርሲቲ ህይወት ወጎች</div>
                    </div>
                    <div style="color:#25f4ee; font-size:12px; font-weight:bold; background:rgba(37,244,238,0.1); padding:6px 12px; border-radius:12px;">🎙️ ግባ</div>
                </div>
            </div>
            <div class="meta-tag">created by: {MY_NAME}</div>
        </div>

        <div class="tab-screen" id="wallet-screen">
            <div class="page-title">My Mela Wallet</div>
            <div class="info-card">
                <div style="font-size:14px; color:#888;">የአሁኑ የኮይን ባላንስዎ</div>
                <div style="font-size:38px; font-weight:900; color:#00cd63; margin:10px 0;">🪙 <span id="wallet-coin-balance">---</span></div>
                <div style="font-size:12px; color:#aaa; line-height:1.6; text-align:left; background:rgba(0,0,0,0.2); padding:10px; border-radius:10px;">
                    📌 <b>የአካውንት ባለቤት፦</b> <span id="wallet-username-label">ያልታወቀ</span><br>
                    📌 <b>የቴሌብር ቁጥር፦</b> {MY_TELEBIRR_NUMBER}
                </div>
            </div>
            
            <div class="create-room-box" style="background:rgba(255,255,255,0.02);">
                <h4 style="font-size:13px; color:#ffdd67; margin-bottom:8px;">💳 ኮይን በቴሌብር ለመግዛት</h4>
                <input type="number" id="purchase-coin-amount" class="input-field" placeholder="የኮይን መጠን (ለምሳሌ፡ 100)">
                <input type="text" id="purchase-tx-id" class="input-field" placeholder="የቴሌብር TX ID ያስገቡ">
                <button class="btn-3d" style="background:linear-gradient(135deg, #00cd63, #00ff7f);" onclick="submitPaymentToBackend()">📥 ክፍያውን አረጋግጥ</button>
            </div>

            <div class="create-room-box" style="background:rgba(255,255,255,0.01);">
                <h4 style="font-size:13px; color:#fe2c55; margin-bottom:8px;">💸 ኮይን ወደ ብር ለመቀየር (Cash-Out)</h4>
                <input type="number" id="cashout-coin-amount" class="input-field" placeholder="የኮይን መጠን">
                <input type="text" id="cashout-phone" class="input-field" placeholder="የቴሌብር ስልክ ቁጥር">
                <button class="btn-3d" style="background:linear-gradient(135deg, #fe2c55, #ff0033);" onclick="submitCashOutToBackend()">💸 የገንዘብ ማውጫ ጥያቄ አቅርብ</button>
            </div>
        </div>

        <div class="tab-screen" id="referral-screen">
            <div class="page-title">ጋብዘው ይክበሩ (Refer & Earn)</div>
            <div class="info-card">
                <h3 style="color:#ffdd67; margin-bottom:12px;">🎉 ለእያንዳንዱ ሰው 20 ነፃ ኮይን!</h3>
                <p style="font-size:13px; color:#ccc; margin-bottom:15px; line-height:1.5;">ሊንኩን ተጠቅመው መተግበሪያውን ሲቀላቀሉ ለእርስዎ 20 ኮይን ዋሌትዎ ላይ ይጨመራል።</p>
                <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px; font-size:11px; color:#25f4ee; border:1px dashed rgba(37,244,238,0.3); word-break:break-all;" id="referral-link-box">
                    ---
                </div>
            </div>
            <button class="btn-3d" onclick="copyReferralLink()">📋 ሊንኩን ኮፒ አድርግ</button>
        </div>

        <div class="app-container" id="room-screen">
            <div class="top-bar">
                <div class="live-tag" id="room-badge-type">🔴 LIVE</div>
                <div class="room-name-display" id="active-room-title">ክፍል: ---</div>
                <div class="voice-counter-badge" id="voice-timer-display">⏱️ On Mic: 0s</div>
                <div style="font-size:13px; color:#fe2c55; cursor:pointer; font-weight:bold;" onclick="exitRoom()">🚪 ውጣ</div>
            </div>
            
            <div class="video-stage-container">
                <div class="video-placeholder-text" id="video-status-placeholder">📷 ቪዲዮው ሲበራ እዚህ ይፈሳል...</div>
                <div id="local-video-stream-box" class="video-stream-view"></div>
            </div>

            <div class="stage-area">
                <div class="host-section">
                    <div class="host-avatar" id="host-crown-zone">🎙️</div>
                    <div class="host-badge">HOST</div>
                    <div style="font-size:13px; font-weight:bold; color:#fff;" id="room-host-name">---</div>
                </div>
                <div class="seats-grid" id="seats-container"></div>
            </div>

            <div class="utility-bar">
                <div class="button-row">
                    <button class="util-btn-3d" style="border-color:#ffdd67; color:#ffdd67;" onclick="alert('ዕድል መሞከሪያው በቅርቡ ይጀምራል!')">🎰 Lucky Draw</button>
                    <button class="util-btn-3d" style="border-color:#00ff7f; color:#00ff7f;" onclick="alert('ቢንጎ በቅርቡ ይዘጋጃል!')">🎲 Bingo</button>
                    <button class="util-btn-3d" style="border-color:#ff007f; color:#ff007f;" onclick="triggerSecretWhisper()">🤫 ሹክሹክታ (5 🪙)</button>
                    <button class="util-btn-3d" onclick="playRealSound('applause')">👏 ጭብጨባ</button>
                    <button class="util-btn-3d" onclick="playRealSound('laughter')">😂 ሳቅ</button>
                </div>
                
                <div class="slider-fx-container">
                    <div class="volume-control-box">
                        <span>🔇 ዜማ</span>
                        <input type="range" min="0" max="100" value="15" class="volume-slider" id="kirar-vol-slider" oninput="adjustMusicVolume(this.value)">
                        <span>🔊</span>
                    </div>
                </div>
            </div>

            <div class="chat-area" id="chat-box"></div>

            <div class="chat-input-container">
                <input type="text" id="text-msg-input" class="chat-input" placeholder="ሀሳብዎን እዚህ ይፃፉ..." onkeypress="if(event.key==='Enter') sendTextMessage()">
                <button class="btn-send-text" onclick="sendTextMessage()">➔</button>
            </div>
            
            <div class="bottom-controls">
                <button class="btn-3d" style="width: auto; padding: 10px 15px; font-size:12px;" onclick="requestSeatAuto()">🎙️ መቀመጫ ያዝ</button>
                
                <button class="btn-3d" style="width: auto; padding: 10px 15px; font-size:12px; background: linear-gradient(135deg, #00bfff, #007acc); box-shadow: 0 4px 0 #005999;" id="video-toggle-btn" onclick="toggleVideoCamera()">📹 ካሜራ አብራ</button>
                
                <div style="display:flex; align-items:center;">
                    <button class="btn-3d" style="width: auto; padding: 10px 15px; font-size:12px; background: linear-gradient(135deg, #ff0055, #ff5574);" onclick="openGiftTray()">🎁 ስጦታ</button>
                    <div class="nav-icon" style="background: rgba(255,255,255,0.06); width: 38px; height: 38px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 16px; cursor: pointer; margin-left:8px;" id="mic-toggle-btn" onclick="toggleMic()">🔊</div>
                </div>
            </div>
        </div>

        <div class="gift-overlay" id="gift-modal-overlay" onclick="closeGiftTray()">
            <div class="gift-tray" id="gift-tray-zone" onclick="event.stopPropagation()">
                <h3 style="color:#fff; font-size:14px; margin-bottom:12px; text-align:center;">የስጦታ ማዕበል (Combo Surge)</h3>
                <div class="gift-grid">
                    <div class="gift-card" onclick="processGiftSend('🌹 ጽጌረዳ', 10, '🌹', this)">
                        <div class="combo-badge">0</div><div class="gift-emoji">🌹</div><div class="gift-cost">10 🪙</div>
                    </div>
                    <div class="gift-card" onclick="processGiftSend('☕ ጀበና ቡና', 50, '☕', this)">
                        <div class="combo-badge">0</div><div class="gift-emoji">☕</div><div class="gift-cost">50 🪙</div>
                    </div>
                    <div class="gift-card" onclick="processGiftSend('🦁 አንበሳ', 200, '🦁', this)">
                        <div class="combo-badge">0</div><div class="gift-emoji">🦁</div><div class="gift-cost">200 🪙</div>
                    </div>
                    <div class="gift-card" onclick="processGiftSend('👑 Mela አክሊል', 500, '👑', this)">
                        <div class="combo-badge">0</div><div class="gift-emoji">👑</div><div class="gift-cost">500 🪙</div>
                    </div>
                </div>
                <button class="util-btn-3d" style="width:100%;" onclick="closeGiftTray()">ዝጋ</button>
            </div>
            
            <div class="wheel-box" id="wheel-zone" style="display:none;" onclick="event.stopPropagation()">
                <h3>🎡 ዕለታዊ የዕድል ማሽከርከሪያ</h3>
                <div class="wheel-graphic" id="wheel-element">🎁</div>
                <button class="btn-3d" onclick="spinTheWheelAction()">🎰 አሽከርክር</button>
                <button class="util-btn-3d" style="margin-top:10px; width:100%;" onclick="closeGiftTray()">ዝጋ</button>
            </div>
        </div>

        <div class="cinematic-stage" id="animation-stage-layer"><div class="big-gift-anim" id="big-gift-emoji-element">👑</div></div>

        <script>
            let client = AgoraRTC.createClient({{ mode: "rtc", codec: "vp8" }});
            let localAudioTrack = null; 
            let localVideoTrack = null; 
            
            let currentSeat = null;
            let myTelegramId = "";
            let myUsername = "እንግዳ"; 
            let currentRoomName = ""; 
            let myCoins = 350;
            
            let voiceTimerInterval = null;
            let secondsOnMic = 0;
            let lastGiftTime = 0;
            let comboCount = 0;
            let currentComboGift = "";

            let seatsData = {{ 
                1: {{name:"ባዶ", active:false}}, 
                2: {{name:"ባዶ", active:false}}, 
                3: {{name:"ባዶ", active:false}}, 
                4: {{name:"ባዶ", active:false}}, 
                5: {{name:"ባዶ", active:false}}, 
                6: {{name:"ባዶ", active:false}} 
            }};

            async function syncUserWithBackend() {{
                const tgId = document.getElementById("lobby-tg-id").value.trim();
                const uName = document.getElementById("lobby-username").value.trim();
                if(!tgId || !uName) return;
                
                myTelegramId = tgId;
                myUsername = uName;

                let response = await fetch('/api/register', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ telegram_id: tgId, username: uName }})
                }});
                let data = await response.json();
                myCoins = data.coins;

                document.getElementById("referral-link-box").innerText = "https://t.me/MelaSpaceBot?start=ref_" + myTelegramId;
            }}

            async function switchTab(tabName) {{
                document.getElementById("lobby-screen").style.display = "none";
                document.getElementById("wallet-screen").style.display = "none";
                document.getElementById("referral-screen").style.display = "none";
                document.getElementById("nav-home").classList.remove("active");
                document.getElementById("nav-wallet").classList.remove("active");
                document.getElementById("nav-ref").classList.remove("active");
                
                if(tabName === 'home') {{
                    document.getElementById("lobby-screen").style.display = "flex";
                    document.getElementById("nav-home").classList.add("active");
                }} else if(tabName === 'wallet') {{
                    document.getElementById("wallet-screen").style.display = "block";
                    document.getElementById("nav-wallet").classList.add("active");
                    if(myTelegramId) {{
                        let res = await fetch(`/api/wallet/${{myTelegramId}}`);
                        let data = await res.json();
                        myCoins = data.coins;
                        document.getElementById("wallet-username-label").innerText = data.username;
                    }}
                    document.getElementById("wallet-coin-balance").innerText = myCoins;
                }} else if(tabName === 'referral') {{
                    document.getElementById("referral-screen").style.display = "block";
                    document.getElementById("nav-ref").classList.add("active");
                    document.getElementById("referral-link-box").innerText = "https://t.me/MelaSpaceBot?start=ref_" + (myTelegramId ? myTelegramId : "{ADMIN_CHAT_ID}");
                }}
            }}

            async function createNewRoomAction() {{
                const tgId = document.getElementById("lobby-tg-id").value.trim();
                const uName = document.getElementById("lobby-username").value.trim();
                const rName = document.getElementById("lobby-roomname").value.trim();
                if(!tgId || !uName || !rName) {{ alert("እባክዎ መረጃዎችን በሙሉ ያስገቡ!"); return; }}
                
                await syncUserWithBackend();
                currentRoomName = rName;
                
                if(document.getElementById("lobby-is-vip").checked) {{
                    let pin = prompt("ለቪአይፒ ክፍሉ መቆለፊያ ባለ 4 አሃዝ PIN ያስገቡ፦");
                    if(!pin) return;
                    currentRoomName = "🔒 [VIP] " + rName;
                }}
                launchRoom();
            }}

            async function joinExistingRoom(roomName) {{
                const tgId = document.getElementById("lobby-tg-id").value.trim();
                const uName = document.getElementById("lobby-username").value.trim();
                if(!tgId || !uName) {{ alert("እባክዎ መጀመሪያ የቴሌግራም ID እና ስምዎን ከላይ ይሙሉ!"); return; }}
                
                await syncUserWithBackend();
                currentRoomName = roomName; 
                launchRoom();
            }}

            function launchRoom() {{
                document.getElementById("main-nav-bar").style.display = "none";
                document.getElementById("lobby-screen").style.display = "none";
                document.getElementById("room-screen").style.display = "flex";
                document.getElementById("active-room-title").innerText = currentRoomName;
                document.getElementById("room-host-name").innerText = myUsername;
                
                const audio = document.getElementById("bg-kirar-audio");
                audio.volume = 0.15;
                audio.play().catch(e => console.log("Audio ready."));

                appendChat("🚀 Mela System", ` ወደ "${{currentRoomName}}" ክፍል በሰላም መጡ!`, "color:#25f4ee; font-weight:bold;");
                renderSeats();
            }}

            async function submitPaymentToBackend() {{
                let amt = document.getElementById("purchase-coin-amount").value;
                let tx = document.getElementById("purchase-tx-id").value.trim();
                if(!myTelegramId) {{ alert("እባክዎ መጀመሪያ ሎቢው ላይ ID ቁጥርዎን ያስገቡ!"); return; }}
                if(!amt || !tx) {{ alert("እባክዎ ሁሉንም ሳጥኖች ይሙሉ!"); return; }}

                let res = await fetch('/api/purchase-coins', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ telegram_id: myTelegramId, amount_coins: parseInt(amt), telebirr_tx_id: tx }})
                }});
                let data = await res.json();
                alert(data.message);
            }}

            async function submitCashOutToBackend() {{
                let amt = document.getElementById("cashout-coin-amount").value;
                let phone = document.getElementById("cashout-phone").value.trim();
                if(!myTelegramId) {{ alert("እባክዎ መጀመሪያ መለያዎን ያስገቡ!"); return; }}
                if(!amt || !phone) {{ alert("እባክዎ ሁሉንም ሳጥኖች ይሙሉ!"); return; }}

                let res = await fetch('/api/cash-out', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ telegram_id: myTelegramId, coins_to_cash: parseInt(amt), telebirr_phone: phone }})
                }});
                let data = await res.json();
                alert(data.message);
            }}

            function renderSeats() {{
                const container = document.getElementById("seats-container");
                container.innerHTML = "";
                for (let i = 1; i <= 6; i++) {{
                    let seat = seatsData[i];
                    let isEmpty = seat.name === "ባዶ";
                    container.innerHTML += `
                        <div onclick="clickSeat(${{i}})">
                            <div class="seat-circle ${{isEmpty ? 'empty' : ''}}">
                                ${{isEmpty ? i : '🎙️'}}
                            </div>
                            <div class="seat-name">${{seat.name}}</div>
                        </div>
                    `;
                }}
            }}

            function clickSeat(num) {{
                if(currentSeat !== null) {{ seatsData[currentSeat] = {{name: "ባዶ", active: false}}; }}
                currentSeat = num;
                seatsData[num] = {{name: myUsername, active: true}};
                renderSeats();
                appendChat("🎙️ System", ` መድረክ ቁጥር ${{num}}ን በስኬት ይዘዋል!`, "color:#ffdd67;");
            }}

            function requestSeatAuto() {{
                for(let i=1; i<=6; i++) {{ if(seatsData[i].name === "ባዶ") {{ clickSeat(i); break; }} }}
            }}

            async function toggleVideoCamera() {{
                const videoBtn = document.getElementById("video-toggle-btn");
                const placeholder = document.getElementById("video-status-placeholder");
                if (!localVideoTrack) {{
                    try {{
                        placeholder.innerText = "🔄 ካሜራ በመነሳት ላይ...";
                        localVideoTrack = await AgoraRTC.createCameraVideoTrack();
                        placeholder.style.display = "none";
                        localVideoTrack.play("local-video-stream-box");
                        videoBtn.innerText = "🛑 ካሜራ አጥፋ";
                    }} catch (err) {{ placeholder.innerText = "❌ ስህተት ተፈጥሯል"; }}
                }} else {{
                    localVideoTrack.stop(); localVideoTrack.close(); localVideoTrack = null;
                    placeholder.style.display = "block"; videoBtn.innerText = "📹 ካሜራ አብራ";
                }}
            }}

            function startVoiceMonetizationLoop() {{
                voiceTimerInterval = setInterval(() => {{
                    secondsOnMic += 10;
                    document.getElementById("voice-timer-display").innerText = `⏱️ On Mic: ${{secondsOnMic}}s`;
                    if(myCoins >= 2) {{
                        myCoins -= 2;
                        appendChat("👛 Wallet", " ማይክራፎን ስለተጠቀሙ 2 🪙 ተቀንሷል", "color:#ffaa00; font-size:11px;");
                    }} else {{ toggleMic(true); }}
                }}, 10000);
            }}

            function toggleMic(forceMute = false) {{
                const micBtn = document.getElementById("mic-toggle-btn");
                if(micBtn.innerText === "🔊" || forceMute) {{
                    micBtn.innerText = "🔇"; clearInterval(voiceTimerInterval);
                }} else {{
                    micBtn.innerText = "🔊"; startVoiceMonetizationLoop();
                }}
            }}

            function triggerSecretWhisper() {{
                let target = prompt("የእርሱ ስም?");
                let whisperMsg = prompt("ሚስጥራዊ መልእክት?");
                if(myCoins >= 5 && whisperMsg) {{
                    myCoins -= 5; appendChat("🤫 ሹክሹክታ", whisperMsg, "color:#ff007f;");
                }}
            }}

            function processGiftSend(name, cost, emoji, cardElement) {{
                if(myCoins >= cost) {{
                    myCoins -= cost; appendChat("🎁 ስጦታ", `${{myUsername}} ${{emoji}} አበረከተ!`, "color:#00ff7f;");
                }} else {{ alert("በቂ ኮይን የለዎትም!"); }}
            }}

            function openGiftTray() {{ document.getElementById("gift-modal-overlay").style.display = "flex"; }}
            function closeGiftTray() {{ document.getElementById("gift-modal-overlay").style.display = "none"; }}
            function openWheelModal() {{ document.getElementById("gift-modal-overlay").style.display = "flex"; }}
            
            function spinTheWheelAction() {{
                document.getElementById("wheel-element").style.transform = "rotate(1440deg)";
                setTimeout(() => {{ alert("50 ኮይን አሸንፈዋል!"); closeGiftTray(); }}, 3000);
            }}

            function sendTextMessage() {{
                const input = document.getElementById("text-msg-input");
                if(!input.value.trim()) return;
                appendChat(myUsername, input.value.trim()); input.value = "";
            }}

            function appendChat(user, msg, style="") {{
                const box = document.getElementById("chat-box");
                box.innerHTML += `<div style="${{style}}"><b>${{user}}:</b> ${{msg}}</div>`;
                box.scrollTop = box.scrollHeight;
            }}

            function copyReferralLink() {{
                navigator.clipboard.writeText(document.getElementById("referral-link-box").innerText); alert("ተገልብጧል!");
            }}

            function exitRoom() {{
                document.getElementById("room-screen").style.display = "none";
                document.getElementById("main-nav-bar").style.display = "flex";
                document.getElementById("lobby-screen").style.display = "flex";
            }}
        </script>
    </body>
    </html>
    """
    return html_content
