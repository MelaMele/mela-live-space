import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Mela Space - Live Verification System")

# 📱 የአንተ መረጃ
MY_TELEBIRR_NUMBER = "0913064239"  
MY_NAME = "Melaku Mebrate"         

# 🤖 የቴሌግራም መረጃህ (በቀጥታ ገብቷል)
TELEGRAM_BOT_TOKEN = "8327536456:AAHn6AqMUIayCjUUTF5up8cICR_4BvjbiKs"  
ADMIN_CHAT_ID = "1065443252"               

@app.get("/", response_class=HTMLResponse)
async def get_index():
    html_content = f"""
    <!DOCTYPE html>
    <html lang="am">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Mela Multi-Guest Space</title>
        <script src="https://download.agora.io/sdk/release/AgoraRTC_N-4.18.0.js"></script>
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body, html {{ width: 100%; height: 100%; overflow: hidden; background: #080810; font-family: sans-serif; color: #fff; }}
            .app-container {{ position: relative; width: 100%; height: 100%; display: flex; flex-direction: column; }}
            .top-bar {{ display: flex; justify-content: space-between; align-items: center; padding: 15px 20px; }}
            .live-tag {{ background: #fe2c55; padding: 5px 12px; border-radius: 20px; font-weight: bold; font-size: 12px; }}
            .coin-badge {{ background: rgba(255, 255, 255, 0.1); padding: 5px 12px; border-radius: 20px; font-size: 13px; }}
            .stage-area {{ flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 10px; }}
            .host-section {{ text-align: center; margin-bottom: 25px; }}
            .host-avatar {{ width: 80px; height: 80px; border-radius: 50%; background: #111; border: 3px solid #fe2c55; display: flex; align-items: center; justify-content: center; font-size: 32px; margin: 0 auto 8px auto; box-shadow: 0 0 15px rgba(254,44,85,0.3); }}
            .seats-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; width: 100%; max-width: 360px; }}
            .seat-node {{ text-align: center; }}
            .seat-circle {{ width: 60px; height: 60px; border-radius: 50%; background: #161722; border: 2px solid #25f4ee; display: flex; align-items: center; justify-content: center; font-size: 20px; margin: 0 auto 5px auto; cursor: pointer; transition: 0.2s; }}
            .seat-circle:active {{ transform: scale(0.9); }}
            .seat-circle.empty {{ border-color: #444; color: #666; }}
            .seat-name {{ font-size: 11px; color: #ddd; text-shadow: 1px 1px 2px #000; }}
            .chat-area {{ height: 120px; padding: 15px; background: linear-gradient(transparent, rgba(0,0,0,0.8)); overflow-y: auto; font-size: 13px; display: flex; flex-direction: column; gap: 5px; }}
            .chat-system {{ color: #25f4ee; font-weight: bold; }}
            .bottom-controls {{ display: flex; justify-content: space-between; align-items: center; padding: 20px; background: #080810; }}
            .action-btn {{ background: #fe2c55; border: none; color: white; padding: 12px 24px; border-radius: 25px; font-weight: bold; font-size: 14px; cursor: pointer; }}
            .icon-tray {{ display: flex; gap: 15px; }}
            .icon-btn {{ background: rgba(255,255,255,0.1); width: 45px; height: 45px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; cursor: pointer; }}
            
            .gift-drawer {{ position: absolute; bottom: -100%; left: 0; width: 100%; background: #161722; border-radius: 24px 24px 0 0; padding: 20px; transition: 0.3s ease-out; z-index: 20; box-shadow: 0 -10px 25px rgba(0,0,0,0.5); }}
            .gift-drawer.open {{ bottom: 0; }}
            .drawer-line {{ width: 40px; height: 4px; background: rgba(255,255,255,0.2); border-radius: 10px; margin: 0 auto 15px auto; cursor: pointer; }}
            .target-select {{ display: flex; gap: 10px; margin-bottom: 15px; overflow-x: auto; padding-bottom: 5px; }}
            .target-opt {{ background: #2f303d; padding: 6px 15px; border-radius: 15px; font-size: 12px; cursor: pointer; white-space: nowrap; }}
            .target-opt.selected {{ border-color: #fe2c55; color: #fe2c55; font-weight: bold; border: 1px solid; }}
            
            .gift-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 15px; max-height: 180px; overflow-y: auto; }}
            .gift-card {{ background: #2f303d; border-radius: 12px; padding: 10px 5px; text-align: center; cursor: pointer; border: 1px solid transparent; transition: 0.2s; }}
            .gift-card.selected {{ border: 1px solid #00cd63; background: rgba(0, 205, 99, 0.1); }}
            .gift-icon {{ font-size: 22px; margin-bottom: 2px; }}
            .gift-title {{ font-size: 11px; font-weight: bold; }}
            .gift-price {{ font-size: 10px; color: #00cd63; margin-top: 2px; }}
            .send-gift-btn {{ width: 100%; background: #00cd63; color: white; border: none; padding: 14px; border-radius: 12px; font-weight: bold; font-size: 15px; cursor: pointer; }}
            
            .payment-modal {{ display: none; position: absolute; top:0; left:0; width:100%; height:100%; background:rgba(8,8,16,0.95); z-index:100; justify-content:center; align-items:center; padding: 20px; }}
            .modal-content {{ background: #161722; width: 100%; max-width: 360px; border-radius: 20px; padding: 20px; border: 1px solid #2f303d; text-align: center; }}
            .info-box {{ background: #2f303d; padding: 15px; border-radius: 12px; margin: 15px 0; text-align: left; font-size: 14px; line-height: 1.6; }}
            .highlight {{ color: #00cd63; font-weight: bold; font-size: 16px; }}
            .file-input-label {{ display: inline-block; width: 100%; background: #25f4ee; color: #080810; padding: 12px; border-radius: 12px; font-weight: bold; cursor: pointer; margin-top: 10px; font-size: 14px; }}
            .submit-receipt-btn {{ width: 100%; background: #00cd63; color: white; border: none; padding: 14px; border-radius: 12px; font-weight: bold; font-size: 15px; margin-top: 15px; cursor: pointer; }}
            .close-modal-btn {{ color: #aaa; font-size: 13px; margin-top: 15px; background: none; border: none; cursor: pointer; text-decoration: underline; }}
        </style>
    </head>
    <body>
        <div class="payment-modal" id="payment-popup">
            <div class="modal-content">
                <h3 style="color:#00cd63; font-size:18px;">💸 በቴሌብር ይክፈሉ</h3>
                <p style="font-size:12px; color:#aaa; margin-top:5px;">እባክዎ ከታች ባለው መረጃ መሰረት ይክፈሉ እና ደረሰኙን ይስቀሉ</p>
                
                <div class="info-box">
                    📌 የቴሌብር ቁጥር: <span class="highlight">{MY_TELEBIRR_NUMBER}</span><br>
                    👤 ስም: <span style="font-weight:bold; color:#fff;">{MY_NAME}</span><br>
                    💰 ጠቅላላ ክፍያ: <span class="highlight" id="modal-amount">0</span> ብር<br>
                    🎁 ስጦታ: <span style="color:#25f4ee; font-weight:bold;" id="modal-gift-name">---</span>
                </div>

                <form id="receipt-form" onsubmit="submitReceipt(event)">
                    <label class="file-input-label">
                        📸 የደረሰኝ ስክሪንሾት መምረጫ
                        <input type="file" id="receipt-file" accept="image/*" required style="display:none;" onchange="fileSelected()">
                    </label>
                    <div id="file-status" style="font-size:11px; color:#00cd63; margin-top:5px; display:none;">✓ ፎቶው ተመርጧል!</div>
                    <button type="submit" class="submit-receipt-btn">✅ ደረሰኝ ልኬያለሁ አረጋግጥ</button>
                </form>
                <button class="close-modal-btn" onclick="closePaymentModal()">ተመለስ</button>
            </div>
        </div>

        <div class="app-container">
            <div class="top-bar">
                <div class="live-tag">🔴 LIVE • የቡድን ስርጭት</div>
                <div class="coin-badge">🪙 <span id="mela-coins-balance">150</span> Mela</div>
            </div>
            <div class="stage-area">
                <div class="host-section">
                    <div class="host-avatar">🎙️</div>
                    <div style="font-size:13px; font-weight:bold;" id="host-label">Melaku (Host)</div>
                </div>
                <div class="seats-grid" id="seats-container"></div>
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
                <div class="target-select" id="target-container">
                    <div class="target-opt selected" onclick="selectTarget('Melaku (Host)')">Melaku (Host)</div>
                    <div class="target-opt" onclick="selectTarget('ዮናስ')">ዮናስ</div>
                </div>
                
                <div class="gift-grid" id="gifts-list-container"></div>
                <button class="send-gift-btn" onclick="openPaymentModal()">💳 በቴሌብር አሁኑኑ ግዛ</button>
            </div>
        </div>

        <script>
            const TELEGRAM_BOT_TOKEN = "{TELEGRAM_BOT_TOKEN}";
            const ADMIN_CHAT_ID = "{ADMIN_CHAT_ID}";

            const AGORA_APP_ID = "ea7dfdf9926d400fb8a54d31be0bd44c"; 
            const CHANNEL_NAME = "mela_party_room";
            
            let client = AgoraRTC.createClient({{ mode: "rtc", codec: "vp8" }});
            let localAudioTrack = null;
            let currentSeat = null;
            let myUsername = "እንግዳ_" + Math.floor(Math.random() * 1000);
            let selectedTarget = "Melaku (Host)";
            let selectedGiftIndex = 0;
            let myCoins = 150;

            // ለክትትል የሚረዱ ቫሪያብሎች
            let currentTransactionId = null;
            let lastUpdateId = 0;

            let seatsData = {{
                1: {{ name: "ዮናስ", active: true, muted: false }},
                2: {{ name: "አልማዝ", active: true, muted: false }},
                3: {{ name: "ባዶ መቀመጫ", active: false, muted: false }},
                4: {{ name: "ሳሙኤል", active: true, muted: true }},
                5: {{ name: "ባዶ መቀመጫ", active: false, muted: false }},
                6: {{ name: "ባዶ መቀመጫ", active: false, muted: false }}
            }};

            const giftsData = [
                {{ icon: "🌹", title: "ሮዝ አበባ", price: 5 }},
                {{ icon: "🍬", title: "ከረሜላ", price: 10 }},
                {{ icon: "☕", title: "ጀበና ቡና", price: 25 }},
                {{ icon: "🐑", title: "የፋሲካ በግ", price: 50 }},
                {{ icon: "🦁", title: "አንበሳ", price: 100 }},
                {{ icon: "👑", title: "የንጉሥ ዘውድ", price: 250 }}
            ];

            function renderSeats() {{
                const container = document.getElementById("seats-container");
                container.innerHTML = "";
                for (let i = 1; i <= 6; i++) {{
                    const seat = seatsData[i];
                    const node = document.createElement("div");
                    node.className = "seat-node";
                    let icon = "➕";
                    if (seat.active) icon = seat.muted ? "🔇" : "🔊";
                    node.innerHTML = `<div class="seat-circle ${{seat.active ? '' : 'empty'}}" onclick="claimSeat(${{i}})">${{icon}}</div><div class="seat-name">${{seat.name}}</div>`;
                    container.appendChild(node);
                }}
            }}

            function renderGifts() {{
                const container = document.getElementById("gifts-list-container");
                container.innerHTML = "";
                giftsData.forEach((gift, idx) => {{
                    const card = document.createElement("div");
                    card.className = `gift-card ${{idx === selectedGiftIndex ? 'selected' : ''}}`;
                    card.onclick = () => {{ selectedGiftIndex = idx; renderGifts(); }};
                    card.innerHTML = `<div class="gift-icon">${{gift.icon}}</div><div class="gift-title">${{gift.title}}</div><div class="gift-price">${{gift.price}} ብር</div>`;
                    container.appendChild(card);
                }});
            }}

            function selectTarget(name) {{
                selectedTarget = name;
                document.querySelectorAll(".target-opt").forEach(opt => {{
                    if(opt.innerText === name) opt.classList.add("selected");
                    else opt.classList.remove("selected");
                }});
            }}

            function openPaymentModal() {{
                const gift = giftsData[selectedGiftIndex];
                document.getElementById("modal-amount").innerText = gift.price;
                document.getElementById("modal-gift-name").innerText = gift.icon + " " + gift.title;
                document.getElementById("payment-popup").style.display = "flex";
                toggleGiftDrawer();
            }}

            function closePaymentModal() {{
                document.getElementById("payment-popup").style.display = "none";
                document.getElementById("receipt-form").reset();
                document.getElementById("file-status").style.display = "none";
            }}

            function fileSelected() {{
                const fileInput = document.getElementById("receipt-file");
                if (fileInput.files.length > 0) {{
                    document.getElementById("file-status").style.display = "block";
                }}
            }}

            async function submitReceipt(event) {{
                event.preventDefault();
                const fileInput = document.getElementById("receipt-file");
                const gift = giftsData[selectedGiftIndex];
                
                if (fileInput.files.length === 0) return;

                // ለእያንዳንዱ ክፍያ መለያ ቁጥር መፍጠር
                currentTransactionId = "TXN_" + Math.floor(Math.random() * 100000);

                // ቴሌግራም ላይ የሚቀመጡት Inline ቁልፎች (Buttons)
                const replyMarkup = {{
                    inline_keyboard: [
                        [
                            {{ text: "✅ አጽድቅ (Approve)", callback_data: `APPROVE_${{currentTransactionId}}_${{gift.price}}` }},
                            {{ text: "❌ ውድቅ አድርግ (Decline)", callback_data: `DECLINE_${{currentTransactionId}}` }}
                        ]
                    ]
                }};

                const captionText = `📩 <b>አዲስ የቴሌብር ደረሰኝ ደርሷል!</b>\\n\\n👤 <b>ላኪ:</b> ${{myUsername}}\\n🎯 <b>ለማን:</b> ${{selectedTarget}}\\n🎁 <b>ስጦታ:</b> ${{gift.icon}} ${{gift.title}}\\n💰 <b>ዋጋ:</b> ${{gift.price}} ETB\\n🆔 <b>መለያ:</b> ${{currentTransactionId}}`;

                const formData = new FormData();
                formData.append("chat_id", ADMIN_CHAT_ID);
                formData.append("caption", captionText);
                formData.append("parse_mode", "HTML");
                formData.append("reply_markup", JSON.stringify(replyMarkup));
                formData.append("photo", fileInput.files[0]);

                try {{
                    closePaymentModal();
                    appendChat(myUsername, `⏳ ደረሰኝ እየተላከ ነው... እባክዎ ይጠብቁ`, "chat-system");
                    
                    const response = await fetch(`https://api.telegram.org/bot${{TELEGRAM_BOT_TOKEN}}/sendPhoto`, {{
                        method: "POST",
                        body: formData
                    }});
                    const data = await response.json();
                    
                    if (data.ok) {{
                        appendChat(myUsername, `⏳ የክፍያ ደረሰኝ ተልኳል። በአስተዳዳሪው (Melaku) እየተረጋገጠ ነው... እባክዎ ገጹን ሳይዘጉ ይጠብቁ!`, "chat-system");
                        // ቦቱን መከታተል መጀመር
                        startCheckingVerification();
                    }} else {{
                        alert("ደረሰኙን መላክ አልተሳካም!");
                    }}
                }} catch(e) {{
                    alert("የኔትወርክ ስህተት አጋጥሟል!");
                }}
            }}

            // 🔄 አስተዳዳሪው ቁልፉን ሲነካ ከቦቱ ላይ መረጃዎችን በየሴኮንዱ የመፈለጊያ ሉፕ
            function startCheckingVerification() {{
                const checkInterval = setInterval(async () => {{
                    if (!currentTransactionId) {{
                        clearInterval(checkInterval);
                        return;
                    }}
                    
                    try {{
                        const res = await fetch(`https://api.telegram.org/bot${{TELEGRAM_BOT_TOKEN}}/getUpdates?offset=${{lastUpdateId + 1}}&timeout=0`);
                        const updateData = await res.json();
                        
                        if (updateData.ok && updateData.result.length > 0) {{
                            for (let update of updateData.result) {{
                                lastUpdateId = update.update_id;
                                
                                // አስተዳዳሪው ቁልፍ ሲነካ የሚመጣ መረጃ (Callback Query)
                                if (update.callback_query) {{
                                    const callbackData = update.callback_query.data;
                                    
                                    if (callbackData.startsWith(`APPROVE_${{currentTransactionId}}`)) {{
                                        const parts = callbackData.split("_");
                                        const price = parseInt(parts[parts.length - 1]);
                                        
                                        clearInterval(checkInterval);
                                        currentTransactionId = null;
                                        
                                        // ኮይን ጨምር እና ቻት ላይ አሳይ
                                        myCoins += price;
                                        document.getElementById("mela-coins-balance").innerText = myCoins;
                                        const gift = giftsData[selectedGiftIndex];
                                        appendChat("Mela System", `🎉🎉 ማረጋገጫ ተጠናቋል! አስተዳዳሪው ክፍያዎን አጽድቋል። ${{gift.icon}} ${{gift.title}} በተሳካ ሁኔታ ተሰጥቷል!`, "chat-system");
                                        
                                        // ለአስተዳዳሪው መልስ መመለሻ (Answer Callback)
                                        fetch(`https://api.telegram.org/bot${{TELEGRAM_BOT_TOKEN}}/answerCallbackQuery?callback_query_id=${{update.callback_query.id}}&text=ክፍያው ጸድቋል!`);
                                        break;
                                    }} 
                                    else if (callbackData.startsWith(`DECLINE_${{currentTransactionId}}`)) {{
                                        clearInterval(checkInterval);
                                        currentTransactionId = null;
                                        
                                        appendChat("Mela System", `❌ ማሳሰቢያ፡ የላኩት ደረሰኝ በአስተዳዳሪው ውድቅ ተደርጓል። እባክዎ ትክክለኛ ደረሰኝ መላክዎን ያረጋግጡ።`, "chat-system");
                                        
                                        fetch(`https://api.telegram.org/bot${{TELEGRAM_BOT_TOKEN}}/answerCallbackQuery?callback_query_id=${{update.callback_query.id}}&text=ክፍያው ውድቅ ተደርጓል!`);
                                        break;
                                    }}
                                }
                            }}
                        }}
                    }} catch (err) {{
                        console.log("Error fetching updates:", err);
                    }}
                }, 2000); // በየ 2 ሰከንዱ ቦቱን ይጠይቃል
            }}

            async function initAgora() {{
                try {{
                    await client.join(AGORA_APP_ID, CHANNEL_NAME, null, null);
                    client.on("user-published", async (user, mediaType) => {{
                        await client.subscribe(user, mediaType);
                        if (mediaType === "audio") user.audioTrack.play();
                    }});
                }} catch(e) {{ console.log(e); }}
            }}

            async function claimSeat(seatId) {{
                if (seatsData[seatId].active) return;
                if (currentSeat) seatsData[currentSeat] = {{ name: "ባዶ መቀመጫ", active: false, muted: false }};
                currentSeat = seatId;
                seatsData[seatId] = {{ name: myUsername + " (እርስዎ)", active: true, muted: false }};
                renderSeats();
                try {{
                    await client.setClientRole("host");
                    if (!localAudioTrack) localAudioTrack = await AgoraRTC.createMicrophoneAudioTrack();
                    await client.publish([localAudioTrack]);
                }} catch (err) {{ console.error(err); }}
            }}

            function requestSeatAuto() {{
                for (let i = 1; i <= 6; i++) {{ if (!seatsData[i].active) {{ claimSeat(i); break; }} }}
            }}

            async function toggleMic() {{
                if (!localAudioTrack) return;
                const btn = document.getElementById("mic-toggle-btn");
                if (localAudioTrack.muted) {{
                    await localAudioTrack.setMuted(false); btn.innerText = "🔊"; seatsData[currentSeat].muted = false;
                }} else {{
                    await localAudioTrack.setMuted(true); btn.innerText = "🔇"; seatsData[currentSeat].muted = true;
                }}
                renderSeats();
            }}

            function toggleGiftDrawer() {{ document.getElementById("gift-panel").classList.toggle("open"); }}
            
            function appendChat(user, msg, className = "") {{
                const box = document.getElementById("chat-box");
                const div = document.createElement("div"); div.className = className;
                div.innerHTML = `<b>${{user}}:</b> ${{msg}}`; box.appendChild(div);
                box.scrollTop = box.scrollHeight;
            }}

            renderSeats(); renderGifts(); initAgora();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
