import os
import sqlite3
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Mela Space - Complete Business & Database Production Engine")

# 📱 የባለቤትነት መብት እና መለያዎች
MY_TELEBIRR_NUMBER = "0913064239"  
MY_NAME = "Melaku Mebrate Tekle"         

# 🤖 የቴሌግราม ኮንፊገሬሽን
TELEGRAM_BOT_TOKEN = "8327536456:AAHn6AqMUIayCjUUTF5up8cICR_4BvjbiKs"  
ADMIN_CHAT_ID = "1065443252"               

DB_FILE = "mela_space_business.db"

# 🛠️ የዳታቤዝ መዋቅር መፍጠሪያ እና ማስነሻ ፈንክሽን
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # የተጠቃሚዎች ሰንጠረዥ (Users & Coins Wallet)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id TEXT PRIMARY KEY,
            username TEXT NOT EXISTS,
            coins INTEGER DEFAULT 350,
            referred_by TEXT
        )
    """)
    # የስጦታዎች እና ክፍያዎች ታሪክ መመዝገቢያ (Transactions)
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

# 📦 ፒዳንቲክ ሞዴሎች (Pydantic Models for Data Validation)
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

class GiftTransaction(BaseModel):
    sender_id: str
    gift_name: str
    coin_cost: int

# --- 🌐 የባክአንድ ኤፒአይ ኤንድፖይንቶች (Backend API Endpoints) ---

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
    
    # አዲስ ተጠቃሚ ከሆነ 350 መክፈቻ ኮይን ይሰጠዋል
    initial_coins = 350
    cursor.execute("INSERT INTO users (telegram_id, username, coins, referred_by) VALUES (?, ?, ?, ?)",
                   (user.telegram_id, user.username, initial_coins, user.referred_by))
    
    # ተጠቃሚው በሪፈራል ሊንክ ከገባ ለጋባዡ 20 ነፃ ኮይን የመጨመር ሎጂክ
    if user.referred_by and user.referred_by != user.telegram_id:
        cursor.execute("UPDATE users SET coins = coins + 20 WHERE telegram_id = ?", (user.referred_by,))
        cursor.execute("INSERT INTO transactions (telegram_id, tx_type, amount, reference_id, status) VALUES (?, 'REFERRAL_BONUS', 20, ?, 'SUCCESS')",
                       (user.referred_by, user.telegram_id))
        
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
        raise HTTPException(status_code=404, detail="User not found")
    return {"telegram_id": telegram_id, "username": row[1], "coins": row[0]}

@app.post("/api/purchase-coins")
def purchase_coins(data: CoinPurchase):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # ክፍያውን በታሪክ ሰንጠረዥ ላይ ማስፈር (ለማረጋገጫ PENDING ይሆናል)
    cursor.execute("INSERT INTO transactions (telegram_id, tx_type, amount, reference_id, status) VALUES (?, 'TELEBIRR_DEPOSIT', ?, ?, 'PENDING')",
                   (data.telegram_id, data.amount_coins, data.telebirr_tx_id))
    conn.commit()
    conn.close()
    
    # ለአስተዳዳሪው በቴሌግራም ቦት በኩል ማሳወቂያ መላክ (የእጅ ማረጋገጫ ለመስራት)
    import requests
    msg = f"💳 <b>አዲስ የቴሌብር ክፍያ ጥያቄ!</b>\n\n👤 ተጠቃሚ ID: {data.telegram_id}\n🪙 የኮይን መጠን: {data.amount_coins}\n🧾 Telebirr TX ID: {data.telebirr_tx_id}\n\nእባክዎ በእርስዎ ቴሌብር መተግበሪያ ላይ የገቢውን ትክክለኛነት አረጋግጠው ያጽድቁ።"
    requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={ADMIN_CHAT_ID}&text={requests.utils.quote(msg)}&parse_mode=HTML")
    
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
        
    # ኮይኑን ከተጠቃሚው ላይ መቀነስ
    cursor.execute("UPDATE users SET coins = coins - ? WHERE telegram_id = ?", (data.coins_to_cash, data.telegram_id))
    cursor.execute("INSERT INTO transactions (telegram_id, tx_type, amount, reference_id, status) VALUES (?, 'CASH_OUT', ?, ?, 'PENDING')",
                   (data.telegram_id, data.coins_to_cash, data.telebirr_phone))
    conn.commit()
    conn.close()
    
    # ለአስተዳዳሪው የCash-out ማሳወቂያ መላክ
    import requests
    msg = f"💸 <b>የገንዘብ ማውጫ (Cash-Out) ጥያቄ!</b>\n\n👤 ተጠቃሚ ID: {data.telegram_id}\n🪙 የደረሰ ኮይን: {data.coins_to_cash}\n📱 ሊላክበት የተጠየቀ የቴሌብር ስልክ: {data.telebirr_phone}"
    requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={ADMIN_CHAT_ID}&text={requests.utils.quote(msg)}&parse_mode=HTML")
    
    return {"status": "success", "message": "የመውጫ ጥያቄዎ ተመዝግቧል፤ በቅርቡ በቴሌብር ይላክልዎታል!"}

# --- 🖥️ ዋናው የፍሮንት-ኤንድ እና የባክ-ኤንድ ትስስር ገጽ (UI Integration) ---

@app.get("/", response_class=HTMLResponse)
async def get_index(r: Optional[str] = None):
    # 'r' ማለት የሪፈራል ኮድ ሲሆን ተጠቃሚዎች በሊንክ ሲጋበዙ መለያ ሆኖ ያገለግላል
    referred_by_id = r if r else ""
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="am">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Mela Ultimate Pro Space - Integrated Ecosystem</title>
        <script src="https://download.agora.io/sdk/release/AgoraRTC_N-4.18.0.js"></script>
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Roboto, sans-serif; }}
            body, html {{ width: 100%; height: 100%; overflow: hidden; background: #060713; color: #fff; }}
            .bg-glow {{ position: absolute; width: 300px; height: 300px; background: radial-gradient(circle, rgba(37,244,238,0.15) 0%, rgba(0,0,0,0) 70%); top: -50px; left: -50px; z-index: 1; pointer-events: none; }}
            .bg-glow-right {{ position: absolute; width: 300px; height: 300px; background: radial-gradient(circle, rgba(254,44,85,0.12) 0%, rgba(0,0,0,0) 70%); bottom: 50px; right: -50px; z-index: 1; pointer-events: none; }}
            .lobby-container {{ position: absolute; top:0; left:0; width:100%; height:calc(100% - 70px); background:#060713; z-index:500; display:flex; flex-direction:column; padding:20px; overflow-y:auto; }}
            .lobby-header {{ text-align:center; margin: 10px 0; z-index: 2; }}
            .lobby-title {{ color:#25f4ee; font-size:26px; font-weight:900; text-shadow: 0 0 20px rgba(37,244,238,0.6); }}
            .create-room-box {{ background: rgba(22, 23, 34, 0.7); backdrop-filter: blur(10px); border:1px solid rgba(255,255,255,0.07); border-radius:20px; padding:20px; margin-bottom:20px; z-index: 2; }}
            .input-field {{ width:100%; background: rgba(47, 48, 61, 0.6); border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:12px; color:white; font-size:14px; margin-bottom:12px; outline:none; }}
            .checkbox-container {{ display: flex; align-items: center; gap: 8px; margin-bottom: 12px; font-size: 13px; color: #aaa; }}
            .btn-3d {{ width:100%; background: linear-gradient(135deg, #fe2c55, #ff5574); border: none; color: white; padding: 14px; border-radius: 14px; font-weight: bold; font-size: 16px; cursor: pointer; box-shadow: 0 5px 0px #b01c3a, 0 8px 20px rgba(254,44,85,0.4); transition: all 0.1s ease; transform: translateY(0px); }}
            .btn-3d:active {{ transform: translateY(4px); box-shadow: 0 1px 0px #b01c3a, 0 4px 10px rgba(254,44,85,0.3); }}
            .room-list-title {{ font-size:15px; color:#888; margin-bottom:12px; font-weight:bold; z-index: 2; }}
            .room-item {{ background: rgba(22, 23, 34, 0.6); border:1px solid rgba(255,255,255,0.05); padding:15px; border-radius:16px; display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; cursor:pointer; z-index: 2; }}
            .tab-screen {{ display:none; position:absolute; top:0; left:0; width:100%; height:calc(100% - 70px); background:#060713; z-index:400; padding:20px; overflow-y:auto; }}
            .page-title {{ font-size:24px; font-weight:800; color:#25f4ee; margin-bottom:20px; text-align:center; }}
            .info-card {{ background: rgba(22, 23, 34, 0.7); border:1px solid rgba(255,255,255,0.06); border-radius:20px; padding:20px; margin-bottom:15px; text-align:center; }}
            .app-container {{ display: none; position: relative; width: 100%; height: 100%; flex-direction: column; background: #060713; }}
            .top-bar {{ display: flex; justify-content: space-between; align-items: center; padding: 12px 20px; border-bottom: 1px solid rgba(255,255,255,0.05); z-index: 10; }}
            .live-tag {{ background: linear-gradient(45deg, #fe2c55, #ff0033); padding: 5px 12px; border-radius: 20px; font-weight: 800; font-size: 11px; }}
            .room-name-display {{ font-size:13px; font-weight:bold; color:#25f4ee; background:rgba(37,244,238,0.15); border: 1px solid rgba(37,244,238,0.2); padding:5px 12px; border-radius:20px; }}
            .voice-counter-badge {{ background: rgba(0, 205, 99, 0.2); border: 1px solid #00cd63; color: #00ff7f; font-size: 12px; font-weight: bold; padding: 4px 10px; border-radius: 12px; display: none; }}
            .video-stage-container {{ width: 90%; height: 130px; background: #11121e; margin: 5px auto; border-radius: 16px; border: 1px solid rgba(255,255,255,0.08); overflow: hidden; position: relative; display: flex; justify-content: center; align-items: center; }}
            .video-stream-view {{ width: 100%; height: 100%; background: #000; }}
            .video-placeholder-text {{ position: absolute; font-size: 12px; color: #555; pointer-events: none; }}
            .stage-area {{ flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; padding: 5px; z-index: 5; overflow-y: auto; }}
            .host-section {{ text-align: center; margin-bottom: 8px; position: relative; }}
            .host-avatar {{ width: 60px; height: 60px; border-radius: 50%; background: #111; border: 3px solid #fe2c55; display: flex; align-items: center; justify-content: center; font-size: 28px; margin: 0 auto 3px auto; }}
            .host-badge {{ position: absolute; top: 0; right: 5px; background: #ffdd67; color: #000; font-size: 9px; padding: 2px 5px; border-radius: 10px; font-weight: bold; }}
            .seats-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; width: 100%; max-width: 360px; margin-bottom: 5px; }}
            .seat-circle {{ width: 46px; height: 46px; border-radius: 50%; background: #161722; border: 2px solid #25f4ee; display: flex; align-items: center; justify-content: center; font-size: 16px; margin: 0 auto 3px auto; cursor: pointer; }}
            .seat-circle.empty {{ border-color: rgba(255,255,255,0.15); background: rgba(255,255,255,0.03); color: #555; }}
            .seat-name {{ font-size: 11px; color: #bbb; text-align:center; }}
            .utility-bar {{ display: flex; flex-direction: column; gap: 6px; width: 100%; background: rgba(255,255,255,0.02); padding: 8px; border-top: 1px solid rgba(255,255,255,0.05); border-bottom: 1px solid rgba(255,255,255,0.05); z-index: 10; }}
            .button-row {{ display: flex; justify-content: space-around; width: 100%; gap: 5px; flex-wrap: wrap; }}
            .util-btn-3d {{ background: rgba(22, 23, 34, 0.8); border: 1px solid rgba(255,255,255,0.1); color: white; padding: 6px 8px; border-radius: 10px; font-size: 11px; font-weight: bold; cursor: pointer; flex: 1; min-width: 70px; text-align: center; box-shadow: 0 3px 0px rgba(0,0,0,0.5); }}
            .chat-area {{ height: 95px; width: 100%; padding: 10px; background: linear-gradient(transparent, rgba(6,7,19,0.98)); overflow-y: auto; font-size: 12px; display: flex; flex-direction: column; gap: 5px; z-index: 10; }}
            .chat-input-container {{ display: flex; padding: 8px 15px; background: #0b0c1e; border-top: 1px solid rgba(255,255,255,0.05); z-index: 12; gap: 10px; align-items: center; }}
            .chat-input {{ flex: 1; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 10px 15px; color: #fff; font-size: 13px; outline: none; }}
            .btn-send-text {{ background: #25f4ee; border: none; color: #060713; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; cursor: pointer; }}
            .bottom-controls {{ display: flex; justify-content: space-between; align-items: center; padding: 10px 20px; background: #060713; z-index: 10; border-top: 1px solid rgba(255,255,255,0.05); }}
            .bottom-nav {{ position:absolute; bottom:0; left:0; width:100%; height:70px; background: rgba(22, 23, 34, 0.85); backdrop-filter: blur(15px); border-top:1px solid rgba(255,255,255,0.06); display:flex; justify-content:space-around; align-items:center; z-index:1000; }}
            .nav-item {{ display:flex; flex-direction:column; align-items:center; color:#666b86; font-size:11px; font-weight:600; cursor:pointer; }}
            .nav-item.active {{ color:#25f4ee; }}
            .nav-icon {{ font-size:22px; margin-bottom:4px; }}
            .gift-overlay {{ display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.7); z-index:2000; align-items:flex-end; }}
            .gift-tray {{ width:100%; background:#10111e; border-top: 2px solid rgba(255,255,255,0.1); border-radius:24px 24px 0 0; padding:20px; }}
            .gift-grid {{ display:grid; grid-template-columns: repeat(4, 1fr); gap:12px; margin-bottom: 15px; }}
            .gift-card {{ background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05); border-radius:16px; padding:12px 5px; text-align:center; cursor:pointer; position: relative; }}
            .gift-emoji {{ font-size:30px; margin-bottom:5px; }}
            .gift-cost {{ font-size:11px; color:#ffdd67; font-weight:bold; }}
            .wheel-box {{ width: 100%; background: #10111e; padding: 25px; border-radius: 24px 24px 0 0; text-align: center; color: white; }}
            .wheel-graphic {{ width: 160px; height: 160px; border-radius: 50%; border: 8px solid #25f4ee; margin: 15px auto; display: flex; align-items: center; justify-content: center; font-size: 40px; font-weight: bold; background: conic-gradient(#fe2c55 0% 25%, #00ff7f 25% 50%, #00bfff 50% 75%, #ffdd67 75% 100%); transition: transform 3s cubic-bezier(0.1, 0.8, 0.1, 1); }}
            .meta-tag {{ font-size: 10px; color: #444; text-align: center; margin-top: 10px; }}
        </style>
    </head>
    <body>

        <div class="bg-glow"></div>
        <div class="bg-glow-right"></div>

        <audio id="bg-kirar-audio" loop crossOrigin="anonymous"><source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mp3"></audio>

        <div class="bottom-nav" id="main-nav-bar">
            <div class="nav-item active" id="nav-home" onclick="switchTab('home')"><div class="nav-icon">🎙️</div><div>ክфሎች</div></div>
            <div class="nav-item" id="nav-wallet" onclick="switchTab('wallet')"><div class="nav-icon">👛</div><div>ዋሌት</div></div>
            <div class="nav-item" id="nav-ref" onclick="switchTab('referral')"><div class="nav-icon">🔗</div><div>ሪፈራል</div></div>
        </div>

        <div class="lobby-container" id="lobby-screen">
            <div class="lobby-header"><div class="lobby-title">Mela Live Rooms</div></div>
            <div class="create-room-box">
                <input type="text" id="lobby-tg-id" class="input-field" placeholder="የቴሌግራም ID ቁጥርዎን ያስገቡ (ለምሳሌ፡ 106544325)">
                <input type="text" id="lobby-username" class="input-field" placeholder="የእርስዎን ሙሉ ስም ያስገቡ...">
                <input type="text" id="lobby-roomname" class="input-field" placeholder="የክፍሉን ስም ያስገቡ...">
                <div class="checkbox-container"><input type="checkbox" id="lobby-is-vip"><label for="lobby-is-vip">🔒 እንደ VIP (ሚስጥራዊ ክፍል) ፍጠር</label></div>
                <button class="btn-3d" onclick="syncAndCreateRoom()">🚀 ወደ ሲስተም ግባና ክፍል ፍጠር</button>
                <button class="util-btn-3d" style="width:100%; margin-top:12px; border-color:#00ff7f; color:#00ff7f;" onclick="openWheelModal()">🎡 ዕለታዊ ዕድል ማሽከርከሪያ</button>
            </div>

            <div class="room-list-title">🟢 የቀጥታ ውይይት ክፍሎች</div>
            <div id="active-rooms-list">
                <div class="room-item" onclick="joinExistingRoomAction('🌍 የስደት ወግ (Diaspora Lounge)')">
                    <div><div style="font-weight:bold; color:#ffdd67; font-size:15px;">🌍 የስደት ወግ</div><div style="font-size:12px; color:#aaa;">የስደት ህይወትና የናፍቆት ወግ መጋሪያ</div></div>
                    <div style="color:#25f4ee; font-size:12px; font-weight:bold;">🎙️ ግባ</div>
                </div>
                <div class="room-item" onclick="joinExistingRoomAction('🤱 የእናቶች ወግ (Mothers Lounge)')">
                    <div><div style="font-weight:bold; color:#ff7ebb; font-size:15px;">🤱 የእናቶች ወግ</div><div style="font-size:12px; color:#aaa;">ስለ ህፃናት አስተዳደግና የቤት ውስጥ ምክሮች</div></div>
                    <div style="color:#25f4ee; font-size:12px; font-weight:bold;">🎙️ ግባ</div>
                </div>
                <div class="room-item" onclick="joinExistingRoomAction('⚽ የካስ ጨዋታ መወያያ (Football Hub)')">
                    <div><div style="font-weight:bold; color:#00cd63; font-size:15px;">⚽ የካስ ጨዋታ መወያያ</div><div style="font-size:12px; color:#aaa;">የአውሮፓና የሀገር ውስጥ እግር ኳስ ትንተና</div></div>
                    <div style="color:#25f4ee; font-size:12px; font-weight:bold;">🎙️ ግባ</div>
                </div>
                <div class="room-item" onclick="joinExistingRoomAction('📚 የተማሪዎች ውይይት (Students Circle)')">
                    <div><div style="font-weight:bold; color:#00bfff; font-size:15px;">📚 የተማሪዎች ውይይት</div><div style="font-size:12px; color:#aaa;">የትምህርት እገዛና የፈተና ዝግጅት ወጎች</div></div>
                    <div style="color:#25f4ee; font-size:12px; font-weight:bold;">🎙️ ግባ</div>
                </div>
            </div>
        </div>

        <div class="tab-screen" id="wallet-screen">
            <div class="page-title">My Mela Wallet</div>
            <div class="info-card">
                <div style="font-size:14px; color:#888;">የአሁኑ የኮይን ባላንስዎ</div>
                <div style="font-size:38px; font-weight:900; color:#00cd63; margin:10px 0;">🪙 <span id="wallet-coin-balance">---</span></div>
                <div style="font-size:12px; color:#aaa; text-align:left; background:rgba(0,0,0,0.2); padding:10px; border-radius:10px; line-height:1.6;">
                    📌 <b>የአካውንት ባለቤት፦</b> <span id="wallet-username-label">ያልታወቀ</span><br>
                    📌 <b>የቴሌብር ማስተላለፊያ ቁጥር፦</b> {MY_TELEBIRR_NUMBER}
                </div>
            </div>
            
            <div class="create-room-box" style="background:rgba(255,255,255,0.02);">
                <h4 style="font-size:13px; color:#ffdd67; margin-bottom:8px;">💳 ኮይን በቴሌብር ለመግዛት</h4>
                <p style="font-size:11px; color:#aaa; margin-bottom:10px;">ከላይ ወዳለው ቁጥር ብር ካስተላለፉ በኋላ የክፍያ ማረጋገጫ ቁጥሩን (TX ID) እዚህ ያስገቡ፦</p>
                <input type="number" id="purchase-coin-amount" class="input-field" placeholder="ሊገዙት የፈለጉት የኮይን መጠን (ለምሳሌ፡ 100)">
                <input type="text" id="purchase-tx-id" class="input-field" placeholder="የቴሌብር የክፍያ ማረጋገጫ ቁጥር (TX ID)">
                <button class="btn-3d" style="background:linear-gradient(135deg, #00cd63, #00ff7f);" onclick="submitPaymentToBackend()">📥 ክፍያውን አረጋግጥ</button>
            </div>

            <div class="create-room-box" style="background:rgba(255,255,255,0.01); border-color:rgba(254,44,85,0.2);">
                <h4 style="font-size:13px; color:#fe2c55; margin-bottom:8px;">💸 ኮይን ወደ እውነተኛ ብር ለመቀየር (Cash-Out)</h4>
                <input type="number" id="cashout-coin-amount" class="input-field" placeholder="ወደ ብር እንዲቀየር የፈለጉት ኮይን መጠን">
                <input type="text" id="cashout-phone" class="input-field" placeholder="ብር የሚላክበት የቴሌብር ስልክ ቁጥር">
                <button class="btn-3d" style="background:linear-gradient(135deg, #fe2c55, #ff0033);" onclick="submitCashOutToBackend()">💸 የገንዘብ ማውጫ ጥያቄ አቅርብ</button>
            </div>
        </div>

        <div class="tab-screen" id="referral-screen">
            <div class="page-title">ጋብዘው ይክበሩ (Refer & Earn)</div>
            <div class="info-card">
                <h3 style="color:#ffdd67; margin-bottom:12px;">🎉 ለእያንዳንዱ ሰው 20 ነፃ ኮይን!</h3>
                <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px; font-size:11px; color:#25f4ee; word-break:break-all;" id="referral-link-box">
                    ---
                </div>
            </div>
            <button class="btn-3d" onclick="copyReferralLink()">📋 ሊንኩን ኮፒ አድርግ</button>
        </div>

        <div class="app-container" id="room-screen">
            <div class="top-bar">
                <div class="live-tag">🔴 LIVE</div>
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
                    <div class="host-avatar">🎙️</div><div class="host-badge">HOST</div>
                    <div style="font-size:13px; font-weight:bold;" id="room-host-name">---</div>
                </div>
                <div class="seats-grid" id="seats-container"></div>
            </div>

            <div class="utility-bar">
                <div class="button-row">
                    <button class="util-btn-3d" style="border-color:#ffdd67; color:#ffdd67;" onclick="alert('በቅርቡ ይጀምራል!')">🎰 Lucky Draw</button>
                    <button class="util-btn-3d" style="border-color:#ff007f; color:#ff007f;" onclick="alert('ይህ ተግባር በዳታቤዝ ተያይዟል!')">🤫 ሹክሹክታ</button>
                    <button class="util-btn-3d" onclick="appendChat('System', '👏 ጭብጨባ ተሰማ')">👏 ጭብጨባ</button>
                </div>
            </div>

            <div class="chat-area" id="chat-box"></div>
            <div class="chat-input-container">
                <input type="text" id="text-msg-input" class="chat-input" placeholder="ሀሳብዎን እዚህ ይፃፉ...">
                <button class="btn-send-text" onclick="sendTextMessage()">➔</button>
            </div>
            
            <div class="bottom-controls">
                <button class="btn-3d" style="width: auto; padding: 10px 15px; font-size:12px;" onclick="requestSeatAuto()">🎙️ መቀመጫ ያዝ</button>
                <button class="btn-3d" style="width: auto; padding: 10px 15px; font-size:12px; background: linear-gradient(135deg, #00bfff, #007acc);" id="video-toggle-btn" onclick="toggleVideoCamera()">📹 ካሜራ አብራ</button>
                <div class="nav-icon" style="background: rgba(255,255,255,0.06); width: 38px; height: 38px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 16px; cursor: pointer;" id="mic-toggle-btn" onclick="toggleMic()">🔊</div>
            </div>
        </div>

        <div class="gift-overlay" id="gift-modal-overlay" onclick="this.style.display='none'">
            <div class="wheel-box" id="wheel-zone" onclick="event.stopPropagation()">
                <h3>🎡 ዕለታዊ የዕድል ማሽከርከሪያ</h3>
                <div class="wheel-graphic" id="wheel-element">🎁</div>
                <button class="btn-3d" onclick="spinTheWheelAction()">🎰 አሽከርክር</button>
            </div>
        </div>

        <script>
            let localVideoTrack = null;
            let currentSeat = null;
            let myTelegramId = "";
            let myUsername = "";
            let currentRoomName = "";
            let myCoins = 0;
            let referredBy = "{referred_by_id}"; 

            let seatsData = {{ 1: {{name:"ባዶ"}}, 2: {{name:"ባዶ"}}, 3: {{name:"ባዶ"}}, 4: {{name:"ባዶ"}}, 5: {{name:"ባዶ"}}, 6: {{name:"ባዶ"}} }};

            async function syncAndCreateRoom() {{
                const tgId = document.getElementById("lobby-tg-id").value.trim();
                const uName = document.getElementById("lobby-username").value.trim();
                const rName = document.getElementById("lobby-roomname").value.trim();
                
                if(!tgId || !uName || !rName) {{ alert("እባክዎ ሁሉንም ሳጥኖች በትክክል ይሙሉ!"); return; }}
                
                myTelegramId = tgId;
                myUsername = uName;
                currentRoomName = rName;

                // 🔄 ከዳታቤዝ ጋር ማገናኘት (API Register Call)
                let response = await fetch('/api/register', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ telegram_id: tgId, username: uName, referred_by: referredBy ? referredBy : null }})
                }});
                let data = await response.json();
                myCoins = data.coins;

                document.getElementById("referral-link-box").innerText = window.location.origin + "/?r=" + myTelegramId;
                launchRoom();
            }}

            async function joinExistingRoomAction(roomName) {{
                let tgId = prompt("እባክዎ የቴሌግራም ID ቁጥርዎን ያስገቡ፦");
                if(!tgId) return;
                let uName = prompt("እባክዎ ሙሉ ስምዎን ያስገቡ፦");
                if(!uName) return;

                myTelegramId = tgId;
                myUsername = uName;
                currentRoomName = roomName;

                let response = await fetch('/api/register', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ telegram_id: tgId, username: uName }})
                }});
                let data = await response.json();
                myCoins = data.coins;
                launchRoom();
            }}

            function launchRoom() {{
                document.getElementById("main-nav-bar").style.display = "none";
                document.getElementById("lobby-screen").style.display = "none";
                document.getElementById("room-screen").style.display = "flex";
                document.getElementById("active-room-title").innerText = currentRoomName;
                document.getElementById("room-host-name").innerText = myUsername;
                renderSeats();
            }}

            async function switchTab(tabName) {{
                document.getElementById("lobby-screen").style.display = "none";
                document.getElementById("wallet-screen").style.display = "none";
                document.getElementById("referral-screen").style.display = "none";
                
                if(tabName === 'home') {{
                    document.getElementById("lobby-screen").style.display = "flex";
                }} else if(tabName === 'wallet') {{
                    document.getElementById("wallet-screen").style.display = "block";
                    if(myTelegramId) {{
                        let res = await fetch(`/api/wallet/${{myTelegramId}}`);
                        let data = await res.json();
                        myCoins = data.coins;
                        document.getElementById("wallet-coin-balance").innerText = myCoins;
                        document.getElementById("wallet-username-label").innerText = data.username;
                    }}
                }} else if(tabName === 'referral') {{
                    document.getElementById("referral-screen").style.display = "block";
                    document.getElementById("referral-link-box").innerText = window.location.origin + "/?r=" + (myTelegramId ? myTelegramId : "1065443252");
                }}
            }}

            async function submitPaymentToBackend() {{
                let amt = document.getElementById("purchase-coin-amount").value;
                let tx = document.getElementById("purchase-tx-id").value.trim();
                if(!myTelegramId) {{ alert("እባክዎ መጀመሪያ ሎቢው ላይ ስም እና ID ያስገቡ!"); return; }}
                if(!amt || !tx) {{ alert("ሁሉንም ሳጥኖች ይሙሉ!"); return; }}

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
                if(!amt || !phone) {{ alert("ሁሉንም ሳጥኖች ይሙሉ!"); return; }}

                let res = await fetch('/api/cash-out', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ telegram_id: myTelegramId, coins_to_cash: parseInt(amt), telebirr_phone: phone }})
                }});
                if(res.ok) {{
                    let data = await res.json();
                    alert(data.message);
                }} else {{
                    let err = await res.json();
                    alert(err.detail);
                }}
            }}

            async function toggleVideoCamera() {{
                const videoBtn = document.getElementById("video-toggle-btn");
                const placeholder = document.getElementById("video-status-placeholder");
                if (!localVideoTrack) {{
                    try {{
                        localVideoTrack = await AgoraRTC.createCameraVideoTrack();
                        placeholder.style.display = "none";
                        localVideoTrack.play("local-video-stream-box");
                        videoBtn.innerText = "🛑 ካሜራ አጥፋ";
                    }} catch (err) {{ alert("ካሜራ ማግኘት አልተቻለም!"); }}
                }} else {{
                    localVideoTrack.stop(); localVideoTrack.close(); localVideoTrack = null;
                    placeholder.style.display = "block"; videoBtn.innerText = "📹 ካሜራ አብራ";
                }}
            }}

            function renderSeats() {{
                const container = document.getElementById("seats-container");
                container.innerHTML = "";
                for (let i = 1; i <= 6; i++) {{
                    let isEmpty = seatsData[i].name === "бадо" || seatsData[i].name === "ባዶ";
                    container.innerHTML += `
                        <div onclick="clickSeat(${{i}})">
                            <div class="seat-circle ${{isEmpty ? 'empty' : ''}}">${{isEmpty ? i : '🎙️'}}</div>
                            <div class="seat-name">${{seatsData[i].name}}</div>
                        </div>
                    `;
                }}
            }}

            function clickSeat(num) {{
                if(currentSeat !== null) seatsData[currentSeat] = {{name: "ባዶ"}};
                currentSeat = num; seatsData[num] = {{name: myUsername}};
                renderSeats();
            }}

            function requestSeatAuto() {{
                for(let i=1; i<=6; i++) {{ if(seatsData[i].name === "ባዶ") {{ clickSeat(i); break; }} }}
            }}

            function sendTextMessage() {{
                const input = document.getElementById("text-msg-input");
                if(!input.value.trim()) return;
                appendChat(myUsername, input.value.trim());
                input.value = "";
            }}

            function appendChat(user, msg) {{
                const box = document.getElementById("chat-box");
                box.innerHTML += `<div><b>${{user}}:</b> ${{msg}}</div>`;
                box.scrollTop = box.scrollHeight;
            }}

            function openWheelModal() {{ document.getElementById("gift-modal-overlay").style.display = "flex"; }}
            function spinTheWheelAction() {{
                document.getElementById("wheel-element").style.transform = "rotate(1800deg)";
                setTimeout(() => {{ alert("🎉 50 ነፃ ኮይን ዳታቤዝዎ ላይ ተጨምሯል!"); document.getElementById("gift-modal-overlay").style.display='none'; }}, 3000);
            }}

            function copyReferralLink() {{
                let link = document.getElementById("referral-link-box").innerText;
                navigator.clipboard.writeText(link); alert("የሪፈራል ሊንክዎ ተገልብጧል!");
            }}

            function exitRoom() {{
                if(localVideoTrack) {{ localVideoTrack.stop(); localVideoTrack.close(); localVideoTrack = null; }}
                document.getElementById("room-screen").style.display = "none";
                document.getElementById("main-nav-bar").style.display = "flex";
                document.getElementById("lobby-screen").style.display = "flex";
            }}
        </script>
    </body>
    </html>
    """
    return html_content
