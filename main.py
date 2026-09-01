import os
from pathlib import Path
from typing import Optional
import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Mela Space - Vercel Serverless Webhook Ecosystem")

# 📱 የባለቤትነት መብት እና መለያዎች (ከ Environment Variables ይነበባሉ)
MY_TELEBIRR_NUMBER = os.getenv("MY_TELEBIRR_NUMBER", "0913064239")
MY_NAME = os.getenv("MY_NAME", "Melaku Mebrate Tekle")

# 🤖 የቴሌግራም ኮንፊገሬሽን
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8708757199:AAFWfFy9ujnZdXEJ2h6CYfzzqh_z27-_kDo")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID", "1065443252")

# 📂 ዳታቤዝ-አልባ የIn-Memory መዋቅር (ጊዜያዊ)
USERS_MEMORY = {}

# --- Pydantic Models ---
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

# --- 📨 የቦት መልዕክት መላኪያ (Async) ---
async def push_bot_message(chat_id: str, text: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    try:
        async with httpx.AsyncClient() as client:
            await client.post(url, json=payload, timeout=5.0)
    except Exception as e:
        print(f"Bot Notification Error: {e}")

# --- 🌐 1. የቴሌግራም ዌብሁክ መቀበያ መስመር ---
@app.post("/api/webhook")
async def telegram_webhook(request: Request):
    try:
        update = await request.json()
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
                        await push_bot_message(
                            ref_id, 
                            f"🎉 <b>የሪፈራል ስጦታ!</b>\n\n👤 {first_name} በእርስዎ ሊንክ ስለገባ 20 ነፃ 🪙 ተጨምሮልዎታል!"
                        )

                welcome_msg = (
                    f"👋 ሰላም {first_name}!\n\n"
                    f"እንኳን ወደ <b>Mela Space</b> በሰላም መጡ።\n\n"
                    f"🎁 መተግበሪያውን ስለከፈቱ <b>350 ነፃ ኮይኖች</b> ተሰጥተውዎታል።\n\n"
                    f"🔗 <b>የእርስዎ መጋበዣ (Referral) ሊንክ፦</b>\n"
                    f"<code>https://t.me/MelaSpaceBot?start=ref_{chat_id}</code>"
                )
                await push_bot_message(chat_id, welcome_msg)

        return {"status": "ok"}
    except Exception as e:
        print(f"Webhook Processing Error: {e}")
        return {"status": "error", "details": str(e)}

# --- 🔄 2. ዌብሁኩን ለቴሌግራም ማስተዋወቂያ ---
@app.get("/api/setup-webhook")
async def setup_webhook(url: str):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook?url={url}&drop_pending_updates=true"
    async with httpx.AsyncClient() as client:
        res = await client.get(telegram_url)
        return res.json()

# --- 🌐 የባክአንድ ኤፒአይ ኤንድፖይንቶች ---
@app.post("/api/register")
async def register_user(user: UserRegistration):
    tg_id = user.telegram_id
    if tg_id in USERS_MEMORY:
        return {"status": "exists", "telegram_id": tg_id, "coins": USERS_MEMORY[tg_id]["coins"]}

    USERS_MEMORY[tg_id] = {"username": user.username, "coins": 350}
    if user.referred_by and user.referred_by in USERS_MEMORY and user.referred_by != tg_id:
        USERS_MEMORY[user.referred_by]["coins"] += 20
    return {"status": "created", "telegram_id": tg_id, "coins": 350}

@app.get("/api/wallet/{telegram_id}")
async def get_wallet_balance(telegram_id: str):
    if telegram_id not in USERS_MEMORY:
        USERS_MEMORY[telegram_id] = {"username": "እንግዳ", "coins": 350}
    return {
        "telegram_id": telegram_id,
        "username": USERS_MEMORY[telegram_id]["username"],
        "coins": USERS_MEMORY[telegram_id]["coins"],
    }

@app.post("/api/purchase-coins")
async def purchase_coins(data: CoinPurchase):
    admin_msg = (
        f"💳 <b>አዲስ የቴሌብር ክፍያ ጥያቄ!</b>\n\n"
        f"👤 ተጠቃሚ ID: <code>{data.telegram_id}</code>\n"
        f"🪙 መጠን: {data.amount_coins}\n"
        f"🧾 TX ID: <code>{data.telebirr_tx_id}</code>"
    )
    await push_bot_message(ADMIN_CHAT_ID, admin_msg)
    return {"status": "submitted", "message": "የክፍያ ጥያቄዎ ለአስተዳዳሪው ተልኳል፤ ሲረጋገጥ ኮይኑ ይገባል!"}

@app.post("/api/cash-out")
async def cash_out_tokens(data: CashOutRequest):
    tg_id = data.telegram_id
    if tg_id in USERS_MEMORY and USERS_MEMORY[tg_id]["coins"] >= data.coins_to_cash:
        USERS_MEMORY[tg_id]["coins"] -= data.coins_to_cash
        admin_msg = (
            f"💸 <b>የካሽ አውት ጥያቄ!</b>\n\n"
            f"👤 ተጠቃሚ ID: <code>{tg_id}</code>\n"
            f"🪙 ኮይን: {data.coins_to_cash}\n"
            f"📱 ስልክ: {data.telebirr_phone}"
        )
        await push_bot_message(ADMIN_CHAT_ID, admin_msg)
        return {"status": "success", "message": "የመውጫ ጥያቄዎ ተመዝግቧል!"}
    raise HTTPException(status_code=400, detail="በቂ ኮይን የለዎትም!")

# --- 📄 index.html ገጽን የማሳያ መንገድ ---
@app.get("/", response_class=HTMLResponse)
async def get_index():
    index_file = Path(__file__).parent / "index.html"
    if index_file.exists():
        return HTMLResponse(content=index_file.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>index.html ፋይል አልተገኘም!</h1>", status_code=404)
