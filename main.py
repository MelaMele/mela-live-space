import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Mela Multi-Guest Audio Space Backend")

# 1. መረጃዎችን በጊዜያዊነት ለመያዝ የተዘጋጁ መዋቅሮች (In-Memory Database for Demo)
class UserSeat(BaseModel):
    seat_id: int
    username: str
    is_muted: bool = False

class GiftRequest(BaseModel):
    sender: str
    receiver: str
    gift_name: str
    amount_etb: float
    phone_number: str

# የክፍሉ መነሻ ሁኔታ (6 ባዶ መቀመጫዎች)
active_seats = {i: "ባዶ መቀመጫ" for i in range(1, 7)}
chat_history = [
    {"user": "ዮናስ", "msg": "ሰላም እንዴት ናችሁ? 🙌", "type": "chat"},
    {"user": "ሳሙኤል", "msg": "ለ Melaku '🦁 አንበሳ' በስጦታ ሰጠ!", "type": "system"}
]

# 2. የፊት ገጹን (index.html) ለተጠቃሚው የሚያሳይ Endpoint
@app.get("/", response_class=HTMLResponse)
async def get_index():
    # በ GitHub ላይ አብሮ የሚቀመጠውን index.html ያነባል
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as file:
            return file.read()
    return "<h1>Mela Audio Space: index.html አልተገኘም!</h1>"

# 3. የአጎራ (Agora) ድምፅ መለያ ቶከን ማመንጫ (Agora Token Generator Mock)
@app.get("/api/agora/token")
async def get_agora_token(channel_name: str, uid: int, role: int):
    """
    ይህ ኤንድፖይንት ተጠቃሚዎች መድረኩን ተቀላቅለው በሰላም እንዲያወሩ 
    የአጎራ ደህንነት ማረጋገጫ ቶከን (RTC Token) ያመነጫል።
    """
    # ማስታወሻ፦ እውነተኛ አምራች ሲሆን እዚህ ላይ የአጎራ AppID እና AppCertificate ይገባል
    mock_token = f"agora_token_for_{channel_name}_{uid}_role_{role}"
    return {"token": mock_token, "uid": uid, "channel": channel_name}

# 4. የመድረክ መቀመጫዎችን ለማስተዳደር (Seat Management API)
@app.get("/api/seats")
async def get_seats():
    return active_seats

@app.post("/api/seats/take")
async def take_seat(seat: UserSeat):
    if seat.seat_id not in active_seats:
        raise HTTPException(status_code=400, detail="ልክ ያልሆነ የመቀመጫ ቁጥር")
    
    if active_seats[seat.seat_id] != "ባዶ መቀመጫ":
        raise HTTPException(status_code=400, detail="ይህ መቀመጫ ቀድሞ ተይዟል")
    
    active_seats[seat.seat_id] = seat.username
    return {"status": "success", "message": f"መቀመጫ ቁጥር {seat.seat_id} በ{seat.username} ተይዟል"}

# 5. የታለመ ስጦታ እና የቴሌብር ክፍያ ማስተናገጃ (Telebirr Gifting API)
@app.post("/api/gift/send")
async def send_targeted_gift(gift: GiftRequest):
    """
    ተጠቃሚው በመድረክ ላይ ላለ ሰው መርጦ በቴሌብር ስጦታ ሲገዛ
    ይህ ኤንድፖይንት የቴሌብርን API ጠርቶ ክፍያውን ያስፈጽማል።
    """
    # እዚህ ላይ የቴሌብር API ጥሪ (H5 / In-App Payment Logic) ይገናኛል
    # ለጊዜው ክፍያው እንደተሳካ አድርገን ወደ ሪል-ታይም ቻት እንልከዋለን
    
    system_msg = f"🎉 {gift.sender} 🎁 ለ {gift.receiver} \"{gift.gift_name}\" በስጦታ ሰጠ!"
    chat_history.append({"user": "System", "msg": system_msg, "type": "system"})
    
    return {
        "status": "success",
        "message": f"የ{gift.amount_etb} ብር ክፍያ በቴሌብር ተሳክቷል",
        "chat_update": system_msg
    }

@app.get("/api/chat")
async def get_chat():
    return chat_history
