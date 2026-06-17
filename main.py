from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Mela Multi-Guest Audio Space Backend")

class UserSeat(BaseModel):
    seat_id: int
    username: str

active_seats = {i: "ባዶ መቀመጫ" for i in range(1, 7)}

@app.get("/", response_class=HTMLResponse)
async def get_index():
    html_content = """
    <!DOCTYPE html>
    <html lang="am">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Mela Multi-Guest Space</title>
        <script src="https://download.agora.io/sdk/release/AgoraRTC_N-4.18.0.js"></script>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body, html { width: 100%; height: 100%; overflow: hidden; background: #080810; font-family: sans-serif; color: #fff; }
            .app-container { position: relative; width: 100%; height: 100%; display: flex; flex-direction: column; }
            .top-bar { display: flex; justify-content: space-between; align-items: center; padding: 15px 20px; }
            .live-tag { background: #fe2c55; padding: 5px 12px; border-radius: 20px; font-weight: bold; font-size: 12px; }
            .coin-badge { background: rgba(255, 255, 255, 0.1); padding: 5px 12px; border-radius: 20px; font-size: 13px; }
            .stage-area { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 10px; }
            .host-section { text-align: center; margin-bottom: 25px; }
            .host-avatar { width: 80px; height: 80px; border-radius: 50%; background: #111; border: 3px solid #fe2c55; display: flex; align-items: center; justify-content: center; font-size: 32px; margin: 0 auto 8px auto; box-shadow: 0 0 15px rgba(254,44,85,0.3); }
            .seats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; width: 100%; max-width: 360px; }
            .seat-node { text-align: center; }
            .seat-circle { width: 60px; height: 60px; border-radius: 50%; background: #161722; border: 2px solid #25f4ee; display: flex; align-items: center; justify-content: center; font-size: 20px; margin: 0 auto 5px auto; cursor: pointer; transition: 0.2s; }
            .seat-circle:active { transform: scale(0.9); }
            .seat-circle.empty { border-color: #444; color: #666; }
            .seat-name { font-size: 11px; color: #ddd; text-shadow: 1px 1px 2px #000; }
            .chat-area { height: 120px; padding: 15px; background: linear-gradient(transparent, rgba(0,0,0,0.8)); overflow-y: auto; font-size: 13px; display: flex; flex-direction: column; gap: 5px; }
            .chat-system { color: #25f4ee; font-weight: bold; }
            .bottom-controls { display: flex; justify-content: space-between; align-items: center; padding: 20px; background: #080810; }
            .action-btn { background: #fe2c55; border: none; color: white; padding: 12px 24px; border-radius: 25px; font-weight: bold; font-size: 14px; cursor: pointer; }
            .icon-tray { display: flex; gap: 15px; }
            .icon-btn { background: rgba(255,255,255,0.1); width: 45px; height: 45px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; cursor: pointer; }
            .gift-drawer { position: absolute; bottom: -100%; left: 0; width: 100%; background: #161722; border-radius: 24px 24px 0 0; padding: 20px; transition: 0.3s ease-out; z-index: 20; }
            .gift-drawer.open { bottom: 0; }
            .drawer-line { width: 40px; height: 4px; background: rgba(255,255,255,0.2); border-radius: 10px; margin: 0 auto 15px auto; }
            .target-select { display: flex; gap: 10px; margin-bottom: 15px; }
            .target-opt { background: #2f303d; padding: 6px 15px; border-radius: 15px; font-size: 12px; cursor: pointer; }
            .target-opt.selected { border-color: #fe2c55; color: #fe2c55; font-weight: bold; border: 1px solid; }
            .gift-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 15px; }
            .gift-card { background: #2f303d; border-radius: 12px; padding: 12px; text-align: center; cursor: pointer; }
            .gift-card.selected { border: 1px solid #00cd63; }
            .gift-price { font-size: 10px; color: #00cd63; margin-top: 4px; }
            .send-gift-btn { width: 100%; background: #00cd63; color: white; border: none; padding: 14px; border-radius: 12px; font-weight: bold; font-size: 15px; cursor: pointer; }
        </style>
    </head>
    <body>
        <div class="app-container">
            <div class="top-bar">
                <div class="live-tag">🔴 LIVE • የቡድን ስርጭት</div>
                <div class="coin-badge">🪙 150 Mela</div>
            </div>
            <div class="stage-area">
                <div class="host-section">
                    <div class="host-avatar">🎙️</div>
                    <div style="font-size:13px; font-weight:bold;">Melaku (Host)</div>
                </div>
                <div class="seats-grid" id="seats-container">
                    </div>
            </div>
            <div class="chat-area" id="chat-box">
                <div><b>ዮናስ:</b> ሰላም እንዴት ናችሁ? 🙌</div>
                <div class="chat-system">🎉 ሳሙኤል 🎁 ለ Melaku "🦁 አንበሳ" በስጦታ ሰጠ!</div>
            </div>
            <div class="bottom-controls">
                <button class="action-btn" onclick="requestSeatAuto()">🎙️ መቀመጫ ያዝ</button>
                <div class="icon-tray">
                    <div class="icon-btn" onclick="toggleGiftDrawer()">🎁</div>
                    <div class="icon-btn">🔗</div>
                    <div class="icon-btn" id="mic-toggle-btn" onclick="toggleMic()">🔊</div>
                </div>
            </div>
            <div class="gift-drawer" id="gift-panel">
                <div class="drawer-line" onclick="toggleGiftDrawer()"></div>
                <h4 style="margin-bottom:12px; font-size:14px; color:#aaa;">🎯 ስጦታው ለሚያገኘው ሰው:</h4>
                <div class="target-select">
                    <div class="target-opt selected">Melaku (Host)</div>
                    <div class="target-opt">ዮናስ</div>
                </div>
                <div class="gift-grid">
                    <div class="gift-card selected"><div>🌹</div><div>ሮዝ</div><div class="gift-price">5 ብር</div></div>
                    <div class="gift-card"><div>🦁</div><div>አንበሳ</div><div class="gift-price">100 ብር</div></div>
                </div>
                <button class="send-gift-btn" onclick="sendGift()">💳 በቴሌብር ገዝተህ ላክ</button>
            </div>
        </div>

        <script>
            // Agora Configuration (Free Sandbox App ID for demo)
            const AGORA_APP_ID = "ea7dfdf9926d400fb8a54d31be0bd44c"; 
            const CHANNEL_NAME = "mela_party_room";
            
            let client = AgoraRTC.createClient({ mode: "rtc", codec: "vp8" });
            let localAudioTrack = null;
            let currentSeat = null;
            let myUsername = "እንግዳ_" + Math.floor(Math.random() * 1000);

            // Mock State for 6 Seats
            let seatsData = {
                1: { name: "ዮናስ", active: true, muted: false },
                2: { name: "አልማዝ", active: true, muted: false },
                3: { name: "ባዶ መቀመጫ", active: false, muted: false },
                4: { name: "ሳሙኤል", active: true, muted: true },
                5: { name: "ባዶ መቀመጫ", active: false, muted: false },
                6: { name: "ባዶ መቀመጫ", active: false, muted: false }
            };

            function renderSeats() {
                const container = document.getElementById("seats-container");
                container.innerHTML = "";
                for (let i = 1; i <= 6; i++) {
                    const seat = seatsData[i];
                    const node = document.createElement("div");
                    node.className = "seat-node";
                    
                    let icon = "➕";
                    if (seat.active) {
                        icon = seat.muted ? "🔇" : "🔊";
                    }
                    
                    node.innerHTML = `
                        <div class="seat-circle ${seat.active ? '' : 'empty'}" onclick="claimSeat(${i})">${icon}</div>
                        <div class="seat-name">${seat.name}</div>
                    `;
                    container.appendChild(node);
                }
            }

            async function initAgora() {
                // Join the voice channel as audience initially
                await client.join(AGORA_APP_ID, CHANNEL_NAME, null, null);
                client.on("user-published", async (user, mediaType) => {
                    await client.subscribe(user, mediaType);
                    if (mediaType === "audio") {
                        user.audioTrack.play();
                    }
                });
            }

            async function claimSeat(seatId) {
                if (seatsData[seatId].active) return; // Stated seat is taken
                
                // If user already occupies another seat, clear it
                if (currentSeat) {
                    seatsData[currentSeat] = { name: "ባዶ መቀመጫ", active: false, muted: false };
                }

                currentSeat = seatId;
                seatsData[seatId] = { name: myUsername + " (እርስዎ)", active: true, muted: false };
                renderSeats();

                // Turn on Microphone and Stream Audio via Agora
                try {
                    await client.setClientRole("host");
                    if (!localAudioTrack) {
                        localAudioTrack = await AgoraRTC.createMicrophoneAudioTrack();
                    }
                    await client.publish([localAudioTrack]);
                    appendChat("ሲስተም", "ማይክራፎንዎ በርቷል፤ መናገር ይችላሉ!", "chat-system");
                } catch (err) {
                    console.error("Microphone Access Denied", err);
                }
            }

            function requestSeatAuto() {
                for (let i = 1; i <= 6; i++) {
                    if (!seatsData[i].active) {
                        claimSeat(i);
                        break;
                    }
                }
            }

            async function toggleMic() {
                if (!localAudioTrack) return;
                const btn = document.getElementById("mic-toggle-btn");
                if (localAudioTrack.muted) {
                    await localAudioTrack.setMuted(false);
                    btn.innerText = "🔊";
                    seatsData[currentSeat].muted = false;
                } else {
                    await localAudioTrack.setMuted(true);
                    btn.innerText = "🔇";
                    seatsData[currentSeat].muted = true;
                }
                renderSeats();
            }

            function toggleGiftDrawer() { document.getElementById("gift-panel").classList.toggle("open"); }
            
            function sendGift() {
                appendChat(myUsername, "🎁 ለ Melaku '🌹 ሮዝ' በስጦታ ሰጠ!", "chat-system");
                toggleGiftDrawer();
            }

            function appendChat(user, msg, className = "") {
                const box = document.getElementById("chat-box");
                const div = document.createElement("div");
                div.className = className;
                div.innerHTML = `<b>${user}:</b> ${msg}`;
                box.appendChild(div);
                box.scrollTop = box.scrollHeight;
            }

            // Initialize on Load
            renderSeats();
            initAgora();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
