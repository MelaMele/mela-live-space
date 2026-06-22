@app.get("/", response_class=HTMLResponse)
async def get_index():
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Mela Ultimate Pro Space - Created by Melaku Mebrate Tekle</title>
        
        <!-- 📱 የቴሌግራም ሚኒ አፕ ስክሪፕት እና Agora RTC -->
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
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

            /* 🗂️ የታብ ገፆች */
            .tab-screen {{ display:none; position:absolute; top:0; left:0; width:100%; height:calc(100% - 70px); background:#060713; z-index:400; padding:20px; overflow-y:auto; }}
            .page-title {{ font-size:24px; font-weight:800; color:#25f4ee; margin-bottom:20px; text-align:center; }}
            .info-card {{ background: rgba(22, 23, 34, 0.7); border:1px solid rgba(255,255,255,0.06); border-radius:20px; padding:20px; margin-bottom:15px; text-align:center; }}
            
            /* 🎙️ 🎬 ዋናው የውስጥ ሩም */
            .app-container {{ display: none; position: relative; width: 100%; height: 100%; flex-direction: column; background: #060713; }}
            .top-bar {{ display: flex; justify-content: space-between; align-items: center; padding: 12px 20px; border-bottom: 1px solid rgba(255,255,255,0.05); z-index: 10; }}
            .live-tag {{ background: linear-gradient(45deg, #fe2c55, #ff0033); padding: 5px 12px; border-radius: 20px; font-weight: 800; font-size: 11px; }}
            .room-name-display {{ font-size:13px; font-weight:bold; color:#25f4ee; background:rgba(37,244,238,0.15); border: 1px solid rgba(37,244,238,0.2); padding:5px 12px; border-radius:20px; }}
            
            .voice-counter-badge {{ background: rgba(0, 205, 99, 0.2); border: 1px solid #00cd63; color: #00ff7f; font-size: 12px; font-weight: bold; padding: 4px 10px; border-radius: 12px; display: none; }}

            /* 📺 የቪዲዮ ማሳያ መስኮት */
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

            /* 💬 ቀጥታ ቻት ክልል */
            .chat-area {{ height: 95px; width: 100%; padding: 10px; background: linear-gradient(transparent, rgba(6,7,19,0.98)); overflow-y: auto; font-size: 12px; display: flex; flex-direction: column; gap: 5px; z-index: 10; scroll-behavior: smooth; }}
            
            /* ✍️ የፅሁፍ መፃፊያ ባር */
            .chat-input-container {{ display: flex; padding: 8px 15px; background: #0b0c1e; border-top: 1px solid rgba(255,255,255,0.05); z-index: 12; gap: 10px; align-items: center; }}
            .chat-input {{ flex: 1; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 10px 15px; color: #fff; font-size: 13px; outline: none; }}
            .btn-send-text {{ background: #25f4ee; border: none; color: #060713; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; cursor: pointer; }}

            /* 🧭 የታችኛው ዋና ሜኑ */
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

        <!-- 🎵 የጀርባ ክራር ሙዚቃ ማጫወቻ -->
        <audio id="bg-kirar-audio" loop crossOrigin="anonymous">
            <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mp3">
        </audio>

        <!-- 🧭 የታችኛው ዋና ሜኑ -->
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

        <!-- 🚪 ሎቢ ገጽ -->
        <div class="lobby-container" id="lobby-screen">
            <div class="lobby-header">
                <div class="lobby-title">Mela Live Rooms</div>
            </div>

            <div class="create-room-box">
                <input type="text" id="lobby-tg-id" class="input-field" placeholder="የቴሌግራም መለያ ቁጥር (ID) ያስገቡ...">
                <input type="text" id="lobby-username" class="input-field" placeholder="የእርስዎን ስም ያስገቡ...">
                <input type="text" id="lobby-roomname" class="input-field" placeholder="የክፍሉን ስም ያስገቡ...">
                <div class="checkbox-container">
                    <input type="checkbox" id="lobby-is-vip">
                    <label for="lobby-is-vip">🔒 እንደ VIP (የግል ሚስጥራዊ ክፍል) ፍጠር</label>
                </div>
                <button class="btn-3d" onclick="createNewRoomAction()">🚀 አዲስ ክፍል ፍጠር</button>
            </div>

            <div class="room-list-title">🟢 የቀጥታ ውይይት ክፍሎች</div>
            <div id="active-rooms-list">
                <div class="room-item" onclick="joinExistingRoom('🌍 የስደት ወግ')">
                    <div>
                        <div style="font-weight:bold; color:#ffdd67; font-size:15px;">🌍 የስደት ወግ (Diaspora Lounge) ⭐</div>
                    </div>
                    <div style="color:#25f4ee; font-size:12px; font-weight:bold;">🎙️ ግባ</div>
                </div>
            </div>
            <div class="meta-tag">Created by: Melaku Mebrate Tekle</div>
        </div>

        <!-- 👛 ዋሌት ገጽ -->
        <div class="tab-screen" id="wallet-screen">
            <div class="page-title">My Mela Wallet</div>
            <div class="info-card">
                <div style="font-size:14px; color:#888;">የአሁኑ የኮይን ባላንስዎ</div>
                <div style="font-size:38px; font-weight:900; color:#00cd63; margin:10px 0;">🪙 <span id="wallet-coin-balance">0</span></div>
            </div>
        </div>

        <!-- 🔗 ሪፈራል ገጽ -->
        <div class="tab-screen" id="referral-screen">
            <div class="page-title">ጋብዘው ይክበሩ (Refer & Earn)</div>
            <div class="info-card">
                <h3 style="color:#ffdd67; margin-bottom:12px;">🎉 ለእያንዳንዱ ሰው 20 ነፃ ኮይን!</h3>
                <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px;" id="referral-link-box">ሊንክ በመጫን ላይ...</div>
            </div>
        </div>

        <!-- 🎙️ የውስጥ ሩም ገጽ -->
        <div class="app-container" id="room-screen">
            <div class="top-bar">
                <div class="live-tag">🔴 LIVE</div>
                <div class="room-name-display" id="active-room-title">ክፍል: ---</div>
                <div style="font-size:13px; color:#fe2c55; cursor:pointer;" onclick="exitRoom()">🚪 ውጣ</div>
            </div>
            
            <!-- 📺 የቪዲዮ ማሳያ መስኮት -->
            <div class="video-stage-container">
                <div id="local-video-stream-box" class="video-stream-view"></div>
                <div class="video-placeholder-text" id="video-status-text">ካሜራ ጠፍቷል</div>
            </div>
            
            <div class="stage-area">
                <div class="host-section">
                    <div class="host-avatar">🎙️</div>
                    <div class="host-badge">HOST</div>
                    <div style="font-size:12px; margin-top:4px;" id="host-name-display">አስተናጋጅ</div>
                </div>
                
                <div class="voice-counter-badge" id="voice-users-count">🔊 1 ሰው እየተናገረ ነው</div>
                
                <!-- 🪑 የመቀመጫዎች ግሪድ -->
                <div class="seats-grid">
                    <div class="seat-container">
                        <div class="seat-circle empty" onclick="occupySeat(1)">1</div>
                        <div class="seat-name">ባዶ</div>
                    </div>
                    <div class="seat-container">
                        <div class="seat-circle empty" onclick="occupySeat(2)">2</div>
                        <div class="seat-name">ባዶ</div>
                    </div>
                    <div class="seat-container">
                        <div class="seat-circle empty" onclick="occupySeat(3)">3</div>
                        <div class="seat-name">ባዶ</div>
                    </div>
                    <div class="seat-container">
                        <div class="seat-circle empty" onclick="occupySeat(4)">4</div>
                        <div class="seat-name">ባዶ</div>
                    </div>
                    <div class="seat-container">
                        <div class="seat-circle empty" onclick="occupySeat(5)">5</div>
                        <div class="seat-name">ባዶ</div>
                    </div>
                    <div class="seat-container">
                        <div class="seat-circle empty" onclick="occupySeat(6)">6</div>
                        <div class="seat-name">ባዶ</div>
                    </div>
                </div>
            </div>
            
            <!-- 🎛️ የመቆጣጠሪያ ቁልፎች -->
            <div class="utility-bar">
                <div class="button-row">
                    <button class="util-btn-3d" id="btn-toggle-mic" onclick="toggleMicAction()">🔇 ማይክ ዝጋ</button>
                    <button class="util-btn-3d" id="btn-toggle-video" onclick="toggleVideoAction()">📷 ካሜራ ክፈት</button>
                    <button class="util-btn-3d" onclick="triggerClapEffect()">👏 አጨብጭብ</button>
                    <button class="util-btn-3d" onclick="triggerFireEffect()">🔥 እሳት</button>
                </div>
                
                <div class="slider-fx-container">
                    <div class="volume-control-box">
                        <span>🔇 ዜማ</span>
                        <input type="range" min="0" max="100" value="15" class="volume-slider" id="kirar-vol" oninput="adjustVolume(this.value)">
                    </div>
                </div>
            </div>
            
            <!-- 💬 ቀጥታ ቻት ክልል -->
            <div class="chat-area" id="room-chat-messages">
                <div style="color:#888; font-style:italic;">እንኳን ወደ ቀጥታ ውይይት በሰላም መጡ!</div>
            </div>
            
            <!-- ✍️ የፅሁፍ መፃፊያ ባር -->
            <div class="chat-input-container">
                <input type="text" id="chat-msg-input" class="chat-input" placeholder="መልእክት ይጻፉ...">
                <button class="btn-send-text" onclick="sendChatMessageAction()">➔</button>
            </div>
        </div>

        <!-- ⚙️ ጃቫስክሪፕት ሎጂክ -->
        <script>
            const tg = window.Telegram.WebApp;
            tg.ready();
            tg.expand();

            let isMicOn = true;
            let isVideoOn = false;

            // 🤖 የቴሌግራም ዳታ በራስ-ሰር መሳቢያ
            window.onload = function() {{
                if (tg.initDataUnsafe && tg.initDataUnsafe.user) {{
                    const user = tg.initDataUnsafe.user;
                    document.getElementById('lobby-tg-id').value = user.id || '';
                    document.getElementById('lobby-username').value = (user.first_name || '') + ' ' + (user.last_name || '');
                    
                    document.getElementById('referral-link-box').innerText = `https://t.me/MelaSpaceBot?start=ref_${{user.id}}`;
                    fetchWalletBalance(user.id);
                }}
            }};

            function switchTab(tab) {{
                document.getElementById('lobby-screen').style.display = tab === 'home' ? 'flex' : 'none';
                document.getElementById('wallet-screen').style.display = tab === 'wallet' ? 'block' : 'none';
                document.getElementById('referral-screen').style.display = tab === 'referral' ? 'block' : 'none';
                
                document.getElementById('nav-home').classList.toggle('active', tab === 'home');
                document.getElementById('nav-wallet').classList.toggle('active', tab === 'wallet');
                document.getElementById('nav-ref').classList.toggle('active', tab === 'referral');
            }}

            function createNewRoomAction() {{
                const roomName = document.getElementById('lobby-roomname').value || "Mela Space Room";
                const username = document.getElementById('lobby-username').value || "አባል";
                
                document.getElementById('lobby-screen').style.display = 'none';
                document.getElementById('main-nav-bar').style.display = 'none';
                document.getElementById('room-screen').style.display = 'flex';
                
                document.getElementById('active-room-title').innerText = "ክፍል: " + roomName;
                document.getElementById('host-name-display').innerText = username;
                
                document.getElementById('bg-kirar-audio').play();
            }}

            function joinExistingRoom(roomName) {{
                document.getElementById('lobby-roomname').value = roomName;
                createNewRoomAction();
            }}

            function exitRoom() {{
                document.getElementById('room-screen').style.display = 'none';
                document.getElementById('lobby-screen').style.display = 'flex';
                document.getElementById('main-nav-bar').style.display = 'flex';
                document.getElementById('bg-kirar-audio').pause();
            }}

            function toggleMicAction() {{
                isMicOn = !isMicOn;
                const btn = document.getElementById('btn-toggle-mic');
                btn.innerText = isMicOn ? "🔇 ማይክ ዝጋ" : "🔊 ማይክ ክፈት";
                btn.style.background = isMicOn ? "" : "#333";
            }}

            function toggleVideoAction() {{
                isVideoOn = !isVideoOn;
                const btn = document.getElementById('btn-toggle-video');
                const statusText = document.getElementById('video-status-text');
                const videoBox = document.getElementById('local-video-stream-box');
                
                btn.innerText = isVideoOn ? "📷 ካሜራ ዝጋ" : "📷 ካሜራ ክፈት";
                statusText.innerText = isVideoOn ? "ካሜራው እየሰራ ነው..." : "ካሜራ ጠፍቷል";
                videoBox.style.background = isVideoOn ? "#222" : "#000";
            }}

            function sendChatMessageAction() {{
                const input = document.getElementById('chat-msg-input');
                const chatArea = document.getElementById('room-chat-messages');
                const username = document.getElementById('lobby-username').value || "እኔ";
                
                if(input.value.trim() !== "") {{
                    const msgDiv = document.createElement('div');
                    msgDiv.innerHTML = `<span style="color:#25f4ee; font-weight:bold;">${{username}}:</span> ${{input.value}}`;
                    chatArea.appendChild(msgDiv);
                    input.value = "";
                    chatArea.scrollTop = chatArea.scrollHeight;
                }}
            }}

            function occupySeat(num) {{
                alert(num + " ቁጥር መቀመጫን ይዘዋል!");
            }}

            function triggerClapEffect() {{
                const chatArea = document.getElementById('room-chat-messages');
                chatArea.innerHTML += `<div>👏 <em>አጨበጨቡ!</em></div>`;
                chatArea.scrollTop = chatArea.scrollHeight;
            }}

            function triggerFireEffect() {{
                const chatArea = document.getElementById('room-chat-messages');
                chatArea.innerHTML += `<div>🔥 <em>እሳት ላኩ!</em></div>`;
                chatArea.scrollTop = chatArea.scrollHeight;
            }}

            function fetchWalletBalance(tgId) {{
                fetch(`/api/wallet/${{tgId}}`)
                    .then(res => res.json())
                    .then(data => {{
                        document.getElementById('wallet-coin-balance').innerText = data.coins || 0;
                    }}).catch(e => console.log("Wallet fetch error"));
            }}

            function adjustVolume(val) {{
                document.getElementById('bg-kirar-audio').volume = val / 100;
            }}
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
