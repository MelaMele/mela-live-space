import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Mela Space - Social Live Platform")

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
            .lobby-container {{ position: absolute; top:0; left:0; width:100%; height:calc(100% - 65px); background:#080810; z-index:500; display:flex; flex-direction:column; padding:20px; overflow-y:auto; }}
            .lobby-header {{ text-align:center; margin: 20px 0; }}
            .lobby-title {{ color:#25f4ee; font-size:24px; font-weight:bold; text-shadow: 0 0 10px rgba(37,244,238,0.3); }}
            .create-room-box {{ background:#161722; border:1px solid #2f303d; border-radius:16px; padding:20px; margin-bottom:25px; }}
            .input-field {{ width:100%; background:#2f303d; border:1px solid #444; border-radius:10px; padding:12px; color:white; font-size:14px; margin-bottom:12px; outline:none; }}
            .btn-create {{ width:100%; background:#fe2c55; border:none; color:white; padding:14px; border-radius:10px; font-weight:bold; font-size:15px; cursor:pointer; }}
            .room-list-title {{ font-size:16px; color:#aaa; margin-bottom:12px; font-weight:bold; }}
            .room-item {{ background:#161722; border:1px solid #2f303d; padding:15px; border-radius:12px; display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; cursor:pointer; }}

            /* 🗂️ ሌሎች ታቦች (Wallet, Referral) ስታይል */
            .tab-screen {{ display:none; position:absolute; top:0; left:0; width:100%; height:calc(100% - 65px); background:#080810; z-index:400; padding:20px; overflow-y:auto; }}
            .page-title {{ font-size:22px; font-weight:bold; color:#25f4ee; margin-bottom:20px; text-align:center; }}
            .info-card {{ background:#161722; border:1px solid #2f303d; border-radius:16px; padding:20px; margin-bottom:20px; text-align:center; }}
            
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
            .host-avatar {{ width: 75px; height: 75px; border-radius: 50%; background: #111; border: 3px solid #fe2c55; display: flex; align-items: center; justify-content: center; font-size: 32px; margin: 0 auto 8px auto; }}
            .seats-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; width: 100%; max-width: 360px; }}
            .seat-node {{ text-align: center; }}
            .seat-circle {{ width: 55px; height: 55px; border-radius: 50%; background: #161722; border: 2px solid #25f4ee; display: flex; align-items: center; justify-content: center; font-size: 20px; margin: 0 auto 5px auto; cursor: pointer; }}
            .seat-circle.empty {{ border-color: #444; color: #666; }}
            .seat-name {{ font-size: 11px; color: #ddd; }}
            .chat-area {{ height: 100px; padding: 15px; background: linear-gradient(transparent, rgba(0,0,0,0.8)); overflow-y: auto; font-size: 13px; display: flex; flex-direction: column; gap: 5px; }}
            .bottom-controls {{ display: flex; justify-content: space-between; align-items: center; padding: 15px 20px; background: #080810; }}
            .action-btn {{ background: #fe2c55; border: none; color: white; padding: 10px 16px; border-radius: 25px; font-weight: bold; font-size: 12px; cursor: pointer; }}
            .gift-btn {{ background: #00cd63; border: none; color: white; padding: 10px 16px; border-radius: 25px; font-weight: bold; font-size: 12px; cursor: pointer; margin-left: 5px; }}
            
            /* 🧭 የታችኛው ሜኑ (Bottom Navigation Bar) */
            .bottom-nav {{ position:absolute; bottom:0; left:0; width:100%; height:65px; background:#161722; border-top:1px solid #2f303d; display:flex; justify-content:space-around; align-items:center; z-index:1000; }}
            .nav-item {{ display:flex; flex-direction:column; align-items:center; color:#aaa; font-size:11px; cursor:pointer; text-decoration:none; }}
            .nav-item.active {{ color:#25f4ee; font-weight:bold; }}
            .nav-icon {{ font-size:20px; margin-bottom:3px; }}
        </style>
    </head>
    <body>

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
            <div class="lobby-header">
                <div class="lobby-title">Mela Live Rooms</div>
            </div>

            <div class="create-room-box">
                <input type="text" id="lobby-username" class="input-field" placeholder="የእርስዎን ስም ያስገቡ...">
                <input type="text" id="lobby-roomname" class="input-field" placeholder="የክፍሉን ስም ያስገቡ...">
                <button class="btn-create" onclick="createNewRoomAction()">🚀 አዲስ ክፍል ፍጠር</button>
            </div>

            <div class="room-list-title">🟢 የቀጥታ ውይይት ክፍሎች</div>
            <div id="active-rooms-list">
                
                <div class="room-item" onclick="joinExistingRoom('👵 የእናቶች ወግ (Mela Lounge)')">
                    <div>
                        <div style="font-weight:bold; color:#fff;">👵 የእናቶች ወግ (Mela Lounge)</div>
                        <div style="font-size:12px; color:#aaa; margin-top:2px;">የባህል ወጎች፣ ምክሮች እና ማህበራዊ ጨዋታዎች</div>
                    </div>
                    <div style="color:#25f4ee; font-size:12px; font-weight:bold;">🎙️ ግባ</div>
                </div>

                <div class="room-item" onclick="joinExistingRoom('📚 የተማሪዎች መወያያ (Mela Room)')">
                    <div>
                        <div style="font-weight:bold; color:#fff;">📚 የተማሪዎች መወያያ (Mela Room)</div>
                        <div style="font-size:12px; color:#aaa; margin-top:2px;">ለትምህርት፣ ለዕውቀት እና ለክህሎት ማሳደጊያ ውይይት</div>
                    </div>
                    <div style="color:#25f4ee; font-size:12px; font-weight:bold;">🎙️ ግባ</div>
                </div>

                <div class="room-item" onclick="joinExistingRoom('⚽ የኳስ ሜዳ (Football Fan Zone)')">
                    <div>
                        <div style="font-weight:bold; color:#fff;">⚽ የኳስ ሜዳ (Football Fan Zone)</div>
                        <div style="font-size:12px; color:#aaa; margin-top:2px;">የእግር ኳስ ጨዋታዎች በቀጥታ መክረካሪያ</div>
                    </div>
                    <div style="color:#25f4ee; font-size:12px; font-weight:bold;">🎙️ ግባ</div>
                </div>

            </div>
        </div>

        <div class="tab-screen" id="wallet-screen">
            <div class="page-title">My Mela Wallet</div>
            <div class="info-card">
                <div style="font-size:14px; color:#aaa;">የአሁኑ የኮይን ባላንስዎ</div>
                <div style="font-size:36px; font-weight:bold; color:#00cd63; margin:10px 0;">🪙 <span id="wallet-coin-balance">150</span></div>
                <div style="font-size:12px; color:#aaa;">( 10 ኮይን = 1 የኢትዮጵያ ብር )</div>
            </div>
            <button class="btn-create" style="background:#00cd63; margin-bottom:12px;" onclick="alert('በቴሌብር ኮይን መግዣ ሲስተም በቅርቡ ይበራል።')">💳 በቴሌብር ኮይን ግዛ (Top Up)</button>
            <button class="btn-create" style="background:#25f4ee; color:#080810;" onclick="alert('ያጠራቀሙትን ኮይን ወደ ብር ቀይረው ቴሌብርዎ ላይ የሚላክበት ሲስተም በቅርቡ ይበራል።')">💸 ኮይን ወደ ብር ቀይር (Cash Out)</button>
        </div>

        <div class="tab-screen" id="referral-screen">
            <div class="page-title">ጋብዘው ይክበሩ (Refer & Earn)</div>
            <div class="info-card">
                <div style="font-size:40px; margin-bottom:10px;">🎁</div>
                <h3 style="color:#fff; margin-bottom:8px;">ለእያንዳንዱ ሰው 20 ነፃ ኮይን!</h3>
                <p style="font-size:13px; color:#aaa; line-height:1.5;">የእርስዎን መለያ ሊንክ ለጓደኞችዎ ያጋሩ፤ እነሱ ገጹን ሲቀላቀሉ ለእርስዎ 20 ኮይን በነፃ እንሰጣለን!</p>
            </div>
            <div class="info-card" style="text-align:left; padding:15px;">
                <div style="font-size:12px; color:#aaa; margin-bottom:5px;">የእርስዎ መጋበዣ ሊንክ፦</div>
                <div style="background:#2f303d; padding:10px; border-radius:8px; font-size:12px; color:#25f4ee; word-break:break-all;" id="my-ref-link">https://mela-space.vercel.app/?ref=mela1065</div>
            </div>
            <button class="btn-create" onclick="copyRefLink()">📋 ሊንኩን ኮፒ አድርግ</button>
        </div>

        <div class="app-container" id="room-screen">
            <div class="top-bar">
                <div class="live-tag">🔴 LIVE</div>
                <div class="room-name-display" id="active-room-title">ክፍል: ---</div>
                <div style="font-size:13px; color:#fe2c55; cursor:pointer; font-weight:bold;" onclick="exitRoom()">🚪 ውጣ</div>
            </div>
            
            <div class="stage-area">
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
                <div style="display:flex; align-items:center;">
                    <button class="gift-btn" onclick="sendRoomGift()">🎁 ስጦታ ስጥ</button>
                    <div class="icon-btn" style="background: rgba(255,255,255,0.1); width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 16px; cursor: pointer; margin-left:10px;" id="mic-toggle-btn" onclick="toggleMic()">🔊</div>
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
            let myCoins = 150; // የኮይን መጠን መነሻ
            
            let audioContext = null;
            let analyser = null;
            let dataArray = null;
            let animationFrameId = null;

            let seatsData = {{ 1:{{name:"ባዶ",active:false}}, 2:{{name:"ባዶ",active:false}}, 3:{{name:"ባዶ",active:false}}, 4:{{name:"ባዶ",active:false}}, 5:{{name:"ባዶ",active:false}}, 6:{{name:"ባዶ",active:false}} }};

            function switchTab(tabName) {{
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
                }} else if(tabName === 'referral') {{
                    document.getElementById("referral-screen").style.display = "block";
                    document.getElementById("nav-ref").classList.add("active");
                }}
            }}

            function createNewRoomAction() {{
                const uName = document.getElementById("lobby-username").value.trim();
                const rName = document.getElementById("lobby-roomname").value.trim();
                if(!uName || !rName) {{ alert("እባክዎ መረጃዎችን በትክክል ያስገቡ!"); return; }}
                myUsername = uName; currentRoomName = rName; launchRoom();
            }}

            function joinExistingRoom(roomName) {{
                let uName = prompt("እባክዎ ስምዎን ያስገቡ:");
                if(!uName || uName.trim() === "") return;
                myUsername = uName; currentRoomName = roomName; launchRoom();
            }}

            function launchRoom() {{
                document.getElementById("main-nav-bar").style.display = "none";
                document.getElementById("lobby-screen").style.display = "none";
                document.getElementById("wallet-screen").style.display = "none";
                document.getElementById("referral-screen").style.display = "none";
                
                document.getElementById("room-screen").style.display = "flex";
                document.getElementById("active-room-title").innerText = currentRoomName;
                document.getElementById("room-host-name").innerText = currentRoomName + " (Host)";
                
                // ሩም ሲጀምር መልዕክት ማሳያ
                document.getElementById("chat-box").innerHTML = "";
                appendChat("Mela System", ` እንኳን ወደዚህ ክፍል በሰላም መጡ!`, "color:#25f4ee; font-weight:bold;");
                
                renderSeats();
                initAgora(currentRoomName);
            }}

            // 🎁 በእያንዳንዱ ክፍል ውስጥ የሚሰራው የስጦታ ተግባር (Gift System Logic)
            function sendRoomGift() {{
                if (myCoins < 20) {{
                    alert("ለማቅረብ በቂ ኮይን የለዎትም! እባክዎ ዋሌትዎ ውስጥ ገብተው ይሙሉ አስፈላጊ ከሆነ።");
                    return;
                }}
                
                // ኮይኑን ቀንሰው
                myCoins -= 20;
                document.getElementById("wallet-coin-balance").innerText = myCoins;
                
                // ሩም ውስጥ ላለው ቻት በሙሉ አሳይ
                appendChat("🎁 ስጦታ", `${{myUsername}} ለክፍሉ አስተናጋጅ [የአበባ እቅፍ 🌹] በ 20 ኮይን ጋብዘዋል!`, "color:#00cd63; font-weight:bold; background:rgba(0,205,99,0.1); padding:5px; border-radius:5px;");
                alert("ስጦታዎ በተሳካ ሁኔታ ተልኳል! 🌹");
            }}

            async function exitRoom() {{
                if(localAudioTrack) {{ localAudioTrack.stop(); localAudioTrack.close(); localAudioTrack = null; }}
                stopVoiceWave();
                await client.leave();
                currentSeat = null;
                for(let i=1; i<=6; i++) seatsData[i] = {{ name: "ባዶ", active: false }};
                
                document.getElementById("room-screen").style.display = "none";
                document.getElementById("main-nav-bar").style.display = "flex";
                switchTab('home');
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
                    await client.join(AGORA_APP_ID, channelName, null, null);
                    client.on("user-published", async (user, mediaType) => {{
                        await client.subscribe(user, mediaType);
                        if (mediaType === "audio") user.audioTrack.play();
                    }});
                }} catch(e) {{ console.log(e); }}
            }}

            async function claimSeat(seatId) {{
                if (seatsData[seatId].active) return;
                if (currentSeat) seatsData[currentSeat] = {{ name: "ባዶ", active: false }};
                currentSeat = seatId;
                seatsData[seatId] = {{ name: myUsername, active: true }};
                renderSeats();
                try {{
                    await client.setClientRole("host");
                    if (!localAudioTrack) {{
                        localAudioTrack = await AgoraRTC.createMicrophoneAudioTrack();
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
                    await localAudioTrack.setMuted(false); btn.innerText = "🔊";
                    document.getElementById("wave-visualizer-box").style.display = "block";
                }} else {{
                    await localAudioTrack.setMuted(true); btn.innerText = "🔇";
                    document.getElementById("wave-visualizer-box").style.display = "none";
                }}
            }}

            function startVoiceWave(mediaStreamTrack) {{
                document.getElementById("wave-visualizer-box").style.display = "block";
                const stream = new MediaStream([mediaStreamTrack]);
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
                const source = audioContext.createMediaStreamSource(stream);
                analyser = audioContext.createAnalyser(); analyser.fftSize = 64;
                source.connect(analyser);
                dataArray = new Uint8Array(analyser.frequencyBinCount);
                const canvas = document.getElementById("wave-canvas");
                const canvasCtx = canvas.getContext("2d");
                
                function drawWave() {{
                    animationFrameId = requestAnimationFrame(drawWave);
                    analyser.getByteFrequencyData(dataArray);
                    canvasCtx.fillStyle = "#161722"; canvasCtx.fillRect(0, 0, canvas.width, canvas.height);
                    const barWidth = (canvas.width / analyser.frequencyBinCount) * 1.5;
                    let barHeight; let x = 0;
                    for(let i = 0; i < analyser.frequencyBinCount; i++) {{
                        barHeight = dataArray[i] * 0.4;
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

            function copyRefLink() {{
                const linkText = document.getElementById("my-ref-link").innerText;
                navigator.clipboard.writeText(linkText);
                alert("የሪፈራል ሊንክዎ በተሳካ ሁኔታ ኮፒ ሆኗል!");
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
