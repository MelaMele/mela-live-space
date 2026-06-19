import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Mela Space Serverless Engine")

# Vercel እንዲያገኘው ተለዋዋጭ ስሙን ለብቻው እናጋልጣለን
handler = app

MY_TELEBIRR_NUMBER = "0913064239"  
MY_NAME = "Melaku Mebrate Tekle"         
TELEGRAM_BOT_TOKEN = "8327536456:AAHn6AqMUIayCjUUTF5up8cICR_4BvjbiKs"  
ADMIN_CHAT_ID = "1065443252"               

USERS_DB = {}
TRANSACTIONS_LOG = []

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

@app.post("/api/register")
def register_user(user: UserRegistration):
    tg_id = user.telegram_id
    if tg_id in USERS_DB:
        return {"status": "exists", "telegram_id": tg_id, "coins": USERS_DB[tg_id]["coins"]}
    
    USERS_DB[tg_id] = {
        "username": user.username,
        "coins": 350,
        "referred_by": user.referred_by
    }
    
    if user.referred_by and user.referred_by in USERS_DB and user.referred_by != tg_id:
        USERS_DB[user.referred_by]["coins"] += 20
        TRANSACTIONS_LOG.append({"telegram_id": user.referred_by, "type": "REFERRAL_BONUS", "amount": 20})
        
    return {"status": "created", "telegram_id": tg_id, "coins": 350}

@app.get("/api/wallet/{telegram_id}")
def get_wallet_balance(telegram_id: str):
    if telegram_id not in USERS_DB:
        USERS_DB[telegram_id] = {"username": "እንግዳ ተጠቃሚ", "coins": 350, "referred_by": None}
    return {"telegram_id": telegram_id, "username": USERS_DB[telegram_id]["username"], "coins": USERS_DB[telegram_id]["coins"]}

@app.post("/api/purchase-coins")
def purchase_coins(data: CoinPurchase):
    TRANSACTIONS_LOG.append({
        "telegram_id": data.telegram_id,
        "type": "TELEBIRR_DEPOSIT",
        "amount": data.amount_coins,
        "tx_id": data.telebirr_tx_id,
        "status": "PENDING"
    })
    
    try:
        msg = f"💳 አዲስ የቴሌብር ክፍያ!\n\n👤 ID: {data.telegram_id}\n🪙 ኮይን: {data.amount_coins}\n🧾 TX ID: {data.telebirr_tx_id}"
        requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={ADMIN_CHAT_ID}&text={msg}", timeout=5)
    except Exception as e:
        pass
        
    return {"status": "submitted", "message": "የክፍያ ጥያቄዎ ለአስተዳዳሪው ተልኳል፤ ሲረጋገጥ ኮይኑ ይገባል!"}

@app.post("/api/cash-out")
def cash_out_tokens(data: CashOutRequest):
    tg_id = data.telegram_id
    if tg_id not in USERS_DB or USERS_DB[tg_id]["coins"] < data.coins_to_cash:
        raise HTTPException(status_code=400, detail="ለማውጣት የጠየቁት ኮይን ከባላንስዎ ይበልጣል!")
        
    USERS_DB[tg_id]["coins"] -= data.coins_to_cash
    TRANSACTIONS_LOG.append({"telegram_id": tg_id, "type": "CASH_OUT", "amount": data.coins_to_cash, "status": "PENDING"})
    
    try:
        msg = f"💸 የካሽ አውት ጥያቄ!\n\n👤 ID: {tg_id}\n🪙 ኮይን: {data.coins_to_cash}\n📱 ስልክ: {data.telebirr_phone}"
        requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={ADMIN_CHAT_ID}&text={msg}", timeout=5)
    except Exception as e:
        pass
        
    return {"status": "success", "message": "የመውጫ ጥያቄዎ ተመዝግቧል፤ በቅርቡ በቴሌብር ይላክልዎታል!"}

@app.get("/", response_class=HTMLResponse)
async def get_index(r: Optional[str] = None):
    referred_by_id = r if r else ""
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="am">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Mela Space - Vercel Fix</title>
        <script src="https://download.agora.io/sdk/release/AgoraRTC_N-4.18.0.js"></script>
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Roboto, sans-serif; }}
            body, html {{ width: 100%; height: 100%; overflow: hidden; background: #060713; color: #fff; }}
            .lobby-container {{ position: absolute; top:0; left:0; width:100%; height:calc(100% - 70px); background:#060713; display:flex; flex-direction:column; padding:20px; overflow-y:auto; }}
            .lobby-title {{ color:#25f4ee; font-size:26px; font-weight:900; text-align:center; margin-bottom:20px; }}
            .create-room-box {{ background: rgba(22, 23, 34, 0.7); border:1px solid rgba(255,255,255,0.07); border-radius:20px; padding:20px; margin-bottom:20px; }}
            .input-field {{ width:100%; background: rgba(47, 48, 61, 0.6); border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:12px; color:white; font-size:14px; margin-bottom:12px; outline:none; }}
            .btn-3d {{ width:100%; background: linear-gradient(135deg, #fe2c55, #ff5574); border: none; color: white; padding: 14px; border-radius: 14px; font-weight: bold; font-size: 16px; cursor: pointer; }}
            .room-item {{ background: rgba(22, 23, 34, 0.6); border:1px solid rgba(255,255,255,0.05); padding:15px; border-radius:16px; display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; cursor:pointer; }}
            .tab-screen {{ display:none; position:absolute; top:0; left:0; width:100%; height:calc(100% - 70px); background:#060713; padding:20px; overflow-y:auto; }}
            .app-container {{ display: none; position: relative; width: 100%; height: 100%; flex-direction: column; background: #060713; }}
            .top-bar {{ display: flex; justify-content: space-between; align-items: center; padding: 12px 20px; border-bottom: 1px solid rgba(255,255,255,0.05); }}
            .video-stage-container {{ width: 90%; height: 130px; background: #11121e; margin: 5px auto; border-radius: 16px; overflow: hidden; position: relative; display: flex; justify-content: center; align-items: center; }}
            .video-stream-view {{ width: 100%; height: 100%; background: #000; }}
            .stage-area {{ flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; padding: 5px; }}
            .chat-area {{ height: 110px; width: 100%; padding: 10px; background: rgba(6,7,19,0.98); overflow-y: auto; font-size: 12px; }}
            .chat-input-container {{ display: flex; padding: 8px 15px; background: #0b0c1e; gap: 10px; }}
            .chat-input {{ flex: 1; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 10px 15px; color: #fff; outline: none; }}
            .bottom-nav {{ position:absolute; bottom:0; left:0; width:100%; height:70px; background: rgba(22, 23, 34, 0.85); border-top:1px solid rgba(255,255,255,0.06); display:flex; justify-content:space-around; align-items:center; }}
            .nav-item {{ display:flex; flex-direction:column; align-items:center; color:#666b86; font-size:11px; font-weight:600; cursor:pointer; }}
            .nav-item.active {{ color:#25f4ee; }}
        </style>
    </head>
    <body>

        <div class="bottom-nav" id="main-nav-bar">
            <div class="nav-item active" onclick="switchTab('home')">🎙️<div>ክፍሎች</div></div>
            <div class="nav-item" onclick="switchTab('wallet')">👛<div>ዋሌት</div></div>
            <div class="nav-item" onclick="switchTab('referral')">🔗<div>ሪፈራል</div></div>
        </div>

        <div class="lobby-container" id="lobby-screen">
            <div class="lobby-title">Mela Live Rooms</div>
            <div class="create-room-box">
                <input type="text" id="lobby-tg-id" class="input-field" placeholder="የቴሌግራም ID ቁጥር">
                <input type="text" id="lobby-username" class="input-field" placeholder="ሙሉ ስምዎን ያስገቡ...">
                <input type="text" id="lobby-roomname" class="input-field" placeholder="የክፍሉን ስም ያስገቡ...">
                <button class="btn-3d" onclick="syncAndCreateRoom()">🚀 ግባና ክፍል ፍጠር</button>
            </div>
            <div id="active-rooms-list">
                <div class="room-item" onclick="joinExistingRoomAction('🌍 የስደት ወግ')">
                    <div><b>🌍 የስደት ወግ</b><br><small style="color:#aaa;">የናфቆት ወግ መጋሪያ</small></div>
                    <div style="color:#25f4ee;">🎙️ ግባ</div>
                </div>
            </div>
            <div style="font-size:10px; color:#444; text-align:center; margin-top:15px;">created by: {MY_NAME}</div>
        </div>

        <div class="tab-screen" id="wallet-screen">
            <h2>My Mela Wallet</h2>
            <div style="background:#161722; padding:20px; border-radius:15px; margin:15px 0; text-align:center;">
                <div>የኮይን ባላንስዎ</div>
                <div style="font-size:32px; color:#00cd63; font-weight:bold;">🪙 <span id="wallet-coin-balance">350</span></div>
            </div>
        </div>

        <div class="tab-screen" id="referral-screen">
            <h2>Refer & Earn</h2>
            <div style="background:#161722; padding:15px; border-radius:10px; font-size:12px; margin-top:15px;" id="ref-box">---</div>
        </div>

        <div class="app-container" id="room-screen">
            <div class="top-bar">
                <div style="color:#fe2c55;">🔴 LIVE</div>
                <div id="active-room-title">---</div>
                <div style="cursor:pointer;" onclick="exitRoom()">🚪 ውጣ</div>
            </div>
            <div class="video-stage-container">
                <div id="local-video-stream-box" class="video-stream-view"></div>
            </div>
            <div class="chat-area" id="chat-box"></div>
            <div class="chat-input-container">
                <input type="text" id="text-msg-input" class="chat-input" placeholder="ፃፉ...">
                <button onclick="sendTextMessage()">➔</button>
            </div>
        </div>

        <script>
            let localVideoTrack = null;
            let myTelegramId = "";
            let myUsername = "";
            let currentRoomName = "";
            let myCoins = 350;

            async function syncAndCreateRoom() {{
                myTelegramId = document.getElementById("lobby-tg-id").value.trim();
                myUsername = document.getElementById("lobby-username").value.trim();
                currentRoomName = document.getElementById("lobby-roomname").value.trim();
                
                if(!myTelegramId || !myUsername || !currentRoomName) {{ alert("ሁሉንም ይሙሉ!"); return; }}

                await fetch('/api/register', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ telegram_id: myTelegramId, username: myUsername }})
                }});

                document.getElementById("ref-box").innerText = window.location.origin + "/?r=" + myTelegramId;
                document.getElementById("lobby-screen").style.display = "none";
                document.getElementById("main-nav-bar").style.display = "none";
                document.getElementById("room-screen").style.display = "flex";
                document.getElementById("active-room-title").innerText = currentRoomName;
            }}

            function joinExistingRoomAction(name) {{
                myTelegramId = prompt("ID ያስገቡ፦");
                myUsername = prompt("ስም ያስገቡ፦");
                if(myTelegramId && myUsername) {{
                    currentRoomName = name;
                    document.getElementById("lobby-screen").style.display = "none";
                    document.getElementById("main-nav-bar").style.display = "none";
                    document.getElementById("room-screen").style.display = "flex";
                    document.getElementById("active-room-title").innerText = currentRoomName;
                }}
            }}

            function switchTab(tab) {{
                document.getElementById("lobby-screen").style.display = "none";
                document.getElementById("wallet-screen").style.display = "none";
                document.getElementById("referral-screen").style.display = "none";
                if(tab === 'home') document.getElementById("lobby-screen").style.display = "flex";
                if(tab === 'wallet') document.getElementById("wallet-screen").style.display = "block";
                if(tab === 'referral') document.getElementById("referral-screen").style.display = "block";
            }}

            function sendTextMessage() {{
                let input = document.getElementById("text-msg-input");
                if(!input.value.trim()) return;
                document.getElementById("chat-box").innerHTML += `<div><b>${{myUsername}}:</b> ${{input.value.trim()}}</div>`;
                input.value = "";
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
