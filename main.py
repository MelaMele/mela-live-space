import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Mela Space - Ultimate Multi-Room System")

# 📱 የአንተ መረጃ
MY_TELEBIRR_NUMBER = "0913064239"  
MY_NAME = "Melaku Mebrate"         

# 🤖 የቴሌግራም መረጃህ
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
            
            /* 🚪 ሎቢ (ክፍል መፍጠሪያ ገጽ) ስታይል */
            .lobby-container {{ position: absolute; top:0; left:0; width:100%; height:100%; background:#080810; z-index:500; display:flex; flex-direction:column; padding:20px; overflow-y:auto; }}
            .lobby-header {{ text-align:center; margin: 30px 0; }}
            .lobby-title {{ color:#25f4ee; font-size:24px; font-weight:bold; text-shadow: 0 0 10px rgba(37,244,238,0.3); }}
            .create-room-box {{ background:#161722; border:1px solid #2f303d; border-radius:16px; padding:20px; margin-bottom:25px; }}
            .input-field {{ width:100%; background:#2f303d; border:1px solid #444; border-radius:10px; padding:12px; color:white; font-size:14px; margin-bottom:12px; outline:none; }}
            .input-field:focus {{ border-color:#25f4ee; }}
            .btn-create {{ width:100%; background:#fe2c55; border:none; color:white; padding:14px; border-radius:10px; font-weight:bold; font-size:15px; cursor:pointer; }}
            .room-list-title {{ font-size:16px; color:#aaa; margin-bottom:12px; font-weight:bold; }}
            .room-item {{ background:#161722; border:1px solid #2f303d; padding:15px; border-radius:12px; display:flex; justify-content:between; align-items:center; margin-bottom:10px; cursor:pointer; }}
            .room-item:active {{ background:#1a1b29; }}

            /* 🎙️ የውስጥ ሩም ስታይል */
            .app-container {{ display: none; position: relative; width: 100%; height: 100%; flex-direction: column; }}
            .top-bar {{ display: flex; justify-content: space-between; align-items: center; padding: 15px 20px; }}
            .live-tag {{ background: #fe2c55; padding: 5px 12px; border-radius: 20px; font-weight: bold; font-size: 12px; }}
            .room-name-display {{ font-size:14px; font-weight:bold; color:#25f4ee; background:rgba(37,244,238,0.1); padding:4px 10px; border-radius:10px; }}
            
            /* 🌊 የድምፅ ሞገድ ካንቫስ ስታይል */
            .wave-container {{ width:100%; height:40px; background:rgba(0,0,0,0.2); margin-bottom:15px; display:none; border-radius:8px; overflow:hidden; }}
            .wave-canvas {{ width:100%; height:100%; }}

            .stage-area {{ flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 10px; }}
            .host-section {{ text-align: center; margin-bottom: 25px; }}
            .host-avatar {{ width: 80px; height: 80px; border-radius: 50%; background: #111; border: 3px solid #fe2c55; display: flex; align-items: center; justify-content: center; font-size: 32px; margin: 0 auto 8px auto; box-shadow: 0 0 15px rgba(254,44,85,0.3); }}
            .seats-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; width: 100%; max-width: 360px; }}
            .seat-node {{ text-align: center; }}
            .seat-circle {{ width: 60px; height: 60px; border-radius: 50%; background: #161722; border: 2px solid #25f4ee; display: flex; align-items: center; justify-content: center; font-size: 20px; margin: 0 auto 5px auto; cursor: pointer; }}
            .seat-circle.empty {{ border-color: #444; color: #666; }}
            .seat-name {{ font-size: 11px; color: #ddd; }}
            .chat-area {{ height: 120px; padding: 15px; background: linear-gradient(transparent, rgba(0,0,0,0.8)); overflow-y: auto; font-size: 13px; display: flex; flex-direction: column; gap: 5px; }}
            .bottom-controls {{ display: flex; justify-content: space-between; align-items: center; padding: 20px; background: #080810; }}
            .action-btn {{ background: #fe2c55; border: none; color: white; padding: 12px 24px; border-radius: 25px; font-weight: bold; font-size: 14px; cursor: pointer; }}
            .icon-tray {{ display: flex; gap: 15px; }}
            .icon-btn {{ background: rgba(255,255,255,0.1); width: 45px; height: 45px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; cursor: pointer; }}
        </style>
    </head>
    <body>

        <!-- 🚪 ሎቢ ገጽ (Lobby) -->
        <div class="lobby-container" id="lobby-screen">
            <div class="lobby-header">
                <div class="lobby-title">🎙️ Mela Multi-Room Lobby</div>
                <p style="color:#aaa; font-size:13px; margin-top:5px;">የራስዎን የውይይት ክፍል ይፍጠሩ ወይም ያሉትን ይቀላቀሉ</p>
            </div>

            <div class="create-room-box">
                <h4 style="margin-bottom:12px; font-size:15px; color:#fff;">🆕 አዲስ ክፍል መክፈቻ</h4>
                <input type="text" id="lobby-username" class="input-field" placeholder="የእርስዎን ስም ያስገቡ...">
                <input type="text" id="lobby-roomname" class="input-field" placeholder="የክፍሉን ስም (ለምሳሌ፡ የልጆች መዝናኛ)...">
                <button class="btn-create" onclick="createNewRoomAction()">🚀 ክፍል ፍጠርና ግባ</button>
            </div>

            <div class="room-list-title">🟢 የቀጥታ ውይይት ክፍሎች (Live Rooms)</div>
            <div id="active-rooms-list">
                <!-- ተንቀሳቃሽ ክፍሎች እዚህ ይደረደራሉ -->
                <div class="room-item" onclick="joinExistingRoom('Mela Main Lounge')">
                    <div>
                        <div style="font-weight:bold; color:#fff;">🏢 Mela Main Lounge</div>
                        <div style="font-size:12px; color:#aaa; margin-top:2px;">ፈጣሪ: Melaku (Host)</div>
                    </div>
                    <div style="color:#00cd63; font-size:12px; font-weight:bold;">🟢 ተቀላቀል</div>
                </div>
                <div class="room-item" onclick="joinExistingRoom('የእግር ኳስ ጨዋታ ግምገማ')">
                    <div>
                        <div style="font-weight:bold; color:#fff;">⚽ የእግር ኳስ ጨዋታ ግምገማ</div>
                        <div style="font-size:12px; color:#aaa; margin-top:2px;">ፈጣሪ: ዮናስ</div>
                    </div>
                    <div style="color:#00cd63; font-size:12px; font-weight:bold;">🟢 ተቀላቀል</div>
                </div>
            </div>
        </div>

        <!-- 🎙️ ዋናው የውይይት ሩም ገጽ -->
        <div class="app-container" id="room-screen">
            <div class="top-bar">
                <div class="live-tag">🔴 LIVE</div>
                <div class="room-name-display" id="active-room-title">ክፍል: ---</div>
                <div style="font-size:13px; color:#00cd63; cursor:pointer; text-decoration:underline;" onclick="exitRoom()">🚪 ውጣ</div>
            </div>
            
            <div class="stage-area">
                <!-- 🌊 የድምፅ ሞገድ (Voice Audio Visualizer) ካንቫስ -->
                <div class="wave-container" id="wave-visualizer-box">
                    <canvas id="wave-canvas" class="wave-canvas"></canvas>
                </div>

                <div class="host-section">
                    <div class="host-avatar">🎙️</div>
                    <div style="font-size:13px; font-weight:bold;" id="room-host-name">---</div>
                </div>
                <div class="seats-grid" id="seats-container"></div>
            </div>
            
            <div class="chat-area" id="chat-box"></div>
            
            <div class="bottom-controls">
                <button class="action-btn" onclick="requestSeatAuto()">🎙️ መቀመጫ ያዝ</button>
                <div class="icon-tray">
                    <div class="icon-btn" id="mic-toggle-btn" onclick="toggleMic()">🔊</div>
                </div>
            </div>
        </div>

        <script>
            const AGORA_APP_ID = "ea7dfdf9926d400fb8a54d31be0bd44c"; 
            let client = AgoraRTC.createClient({{ mode: "rtc", codec: "vp8" }});
            let localAudioTrack = null;
            let currentSeat = null;
            
            let myUsername = "እንግዳ";
            let currentRoomName = "";
            
            // የድምፅ ሞገድ (Visualizer) ቫሪያብሎች
            let audioContext = null;
            let analyser = null;
            let dataArray = null;
            let animationFrameId = null;

            let seatsData = {{
                1: {{ name: "ባዶ መቀመጫ", active: false }},
                2: {{ name: "ባዶ መቀመጫ", active: false }},
                3: {{ name: "ባዶ መቀመጫ", active: false }},
                4: {{ name: "ባዶ መቀመጫ", active: false }},
                5: {{ name: "ባዶ መቀመጫ", active: false }},
                6: {{ name: "ባዶ መቀመጫ", active: false }}
            }};

            // 🚀 አዲስ ክፍል የመፍጠሪያ ተግባር
            function createNewRoomAction() {{
                const uName = document.getElementById("lobby-username").value.trim();
                const rName = document.getElementById("lobby-roomname").value.trim();
                
                if(!uName || !rName) {{
                    alert("እባክዎ ስምዎን እና የክፍሉን ስም ያስገቡ!");
                    return;
                }}
                
                myUsername = uName;
                currentRoomName = rName;
                launchRoom();
            }}

            // 🟢 ያሉትን ክፍሎች የመቀላቀያ ተግባር
            function joinExistingRoom(roomName) {{
                let uName = prompt("እባክዎ ስምዎን ያስገቡ:");
                if(!uName || uName.trim() === "") return;
                
                myUsername = uName;
                currentRoomName = roomName;
                launchRoom();
            }}

            // 🎬 ክፍሉን የማስጀመርያ ተግባር
            function launchRoom() {{
                document.getElementById("lobby-screen").style.display = "none";
                document.getElementById("room-screen").style.display = "flex";
                document.getElementById("active-room-title").innerText = "ክፍል: " + currentRoomName;
                document.getElementById("room-host-name").innerText = currentRoomName + " (Host)";
                
                appendChat("Mela System", ` እንኳን ወደ "${{currentRoomName}}" ክፍል በሰላም መጡ!`, "color:#25f4ee; font-weight:bold;");
                renderSeats();
                initAgora(currentRoomName);
            }}

            // 🚪 ከክፍል መውጫ ተግባር
            async function exitRoom() {{
                if(localAudioTrack) {{
                    localAudioTrack.stop();
                    localAudioTrack.close();
                    localAudioTrack = null;
                }}
                stopVoiceWave();
                await client.leave();
                
                // ሪሴት ማድረግ
                currentSeat = null;
                for(let i=1; i<=6; i++) seatsData[i] = {{ name: "ባዶ መቀመጫ", active: false }};
                
                document.getElementById("room-screen").style.display = "none";
                document.getElementById("lobby-screen").style.display = "flex";
            }}

            function renderSeats() {{
                const container = document.getElementById("seats-container");
                container.innerHTML = "";
                for (let i = 1; i <= 6; i++) {{
                    const seat = seatsData[i];
                    const node = document.createElement("div");
                    node.className = "seat-node";
                    let icon = seat.active ? "👤" : "➕";
                    node.innerHTML = `<div class="seat-circle ${{seat.active ? '' : 'empty'}}" onclick="claimSeat(${{i}})">${{icon}}</div><div class="seat-name">${{seat.name}}</div>`;
                    container.appendChild(node);
                }}
            }}

            async function initAgora(channelName) {{
                try {{
                    // የቻናሉን ስም ዳይናሚክ በማድረግ የተለያየ ሩም ይፈጥራል
                    await client.join(AGORA_APP_ID, channelName, null, null);
                    client.on("user-published", async (user, mediaType) => {{
                        await client.subscribe(user, mediaType);
                        if (mediaType === "audio") user.audioTrack.play();
                    }});
                }} catch(e) {{ console.log(e); }}
            }}

            async function claimSeat(seatId) {{
                if (seatsData[seatId].active) return;
                if (currentSeat) seatsData[currentSeat] = {{ name: "ባዶ መቀመጫ", active: false }};
                currentSeat = seatId;
                seatsData[seatId] = {{ name: myUsername + " (እርስዎ)", active: true }};
                renderSeats();
                try {{
                    await client.setClientRole("host");
                    if (!localAudioTrack) {{
                        localAudioTrack = await AgoraRTC.createMicrophoneAudioTrack();
                        // 🌊 የማይኩን ድምፅ ሞገድ ማስጀመር
                        startVoiceWave(localAudioTrack.getMediaStreamTrack());
                    }}
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
                    await localAudioTrack.setMuted(false); 
                    btn.innerText = "🔊"; 
                    document.getElementById("wave-visualizer-box").style.display = "block";
                }} else {{
                    await localAudioTrack.setMuted(true); 
                    btn.innerText = "🔇"; 
                    document.getElementById("wave-visualizer-box").style.display = "none";
                }}
            }}

            // 🌊 የድምፅ ሞገድ (Visualizer) መሳያ ዋና ህግ
            function startVoiceWave(mediaStreamTrack) {{
                document.getElementById("wave-visualizer-box").style.display = "block";
                const stream = new MediaStream([mediaStreamTrack]);
                
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
                const source = audioContext.createMediaStreamSource(stream);
                analyser = audioContext.createAnalyser();
                analyser.fftSize = 64; 
                source.connect(analyser);
                
                const bufferLength = analyser.frequencyBinCount;
                dataArray = new Uint8Array(bufferLength);
                
                const canvas = document.getElementById("wave-canvas");
                const canvasCtx = canvas.getContext("2d");
                
                function drawWave() {{
                    animationFrameId = requestAnimationFrame(drawWave);
                    analyser.getByteFrequencyData(dataArray);
                    
                    canvasCtx.fillStyle = "#161722";
                    canvasCtx.fillRect(0, 0, canvas.width, canvas.height);
                    
                    const barWidth = (canvas.width / bufferLength) * 1.5;
                    let barHeight;
                    let x = 0;
                    
                    for(let i = 0; i < bufferLength; i++) {{
                        barHeight = dataArray[i] * 0.4;
                        // ማራኪ የሰማያዊ እና ሮዝ ቀለም ውህደት ሞገድ
                        canvasCtx.fillStyle = `rgb(${{barHeight+100}}, 37, 244)`;
                        canvasCtx.fillRect(x, canvas.height - barHeight, barWidth - 2, barHeight);
                        x += barWidth;
                    }}
                }}
                drawWave();
            }}

            function stopVoiceWave() {{
                if(animationFrameId) cancelAnimationFrame(animationFrameId);
                if(audioContext) audioContext.close();
                document.getElementById("wave-visualizer-box").style.display = "none";
            }}
            
            function appendChat(user, msg, style = "") {{
                const box = document.getElementById("chat-box");
                const div = document.createElement("div");
                div.style = style;
                div.innerHTML = `<b>${{user}}:</b> ${{msg}}`; box.appendChild(div);
                box.scrollTop = box.scrollHeight;
            }}
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
