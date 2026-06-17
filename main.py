import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Mela Space - Ultimate Cinematic Edition")

# 📱 የአንተ መረጃ
MY_TELEBIRR_NUMBER = "0913064239"  
MY_NAME = "Melaku Mebrate"         

# 🤖 የቴሌግราม መረጃህ
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
        <title>Mela Ultimate Space</title>
        <script src="https://download.agora.io/sdk/release/AgoraRTC_N-4.18.0.js"></script>
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
            body, html {{ width: 100%; height: 100%; overflow: hidden; background: #060713; color: #fff; }}
            
            /* ✨ Ambient Neon Glows */
            .bg-glow {{ position: absolute; width: 300px; height: 300px; background: radial-gradient(circle, rgba(37,244,238,0.15) 0%, rgba(0,0,0,0) 70%); top: -50px; left: -50px; z-index: 1; pointer-events: none; }}
            .bg-glow-right {{ position: absolute; width: 300px; height: 300px; background: radial-gradient(circle, rgba(254,44,85,0.12) 0%, rgba(0,0,0,0) 70%); bottom: 50px; right: -50px; z-index: 1; pointer-events: none; }}

            /* 🚪 ሎቢ */
            .lobby-container {{ position: absolute; top:0; left:0; width:100%; height:calc(100% - 70px); background:#060713; z-index:500; display:flex; flex-direction:column; padding:25px 20px; overflow-y:auto; }}
            .lobby-header {{ text-align:center; margin: 20px 0; z-index: 2; }}
            .lobby-title {{ color:#25f4ee; font-size:26px; font-weight:900; letter-spacing: 1px; text-shadow: 0 0 20px rgba(37,244,238,0.6); }}
            
            .create-room-box {{ background: rgba(22, 23, 34, 0.7); backdrop-filter: blur(10px); border:1px solid rgba(255,255,255,0.07); border-radius:20px; padding:22px; margin-bottom:25px; box-shadow: 0 8px 32px rgba(0,0,0,0.3); z-index: 2; }}
            .input-field {{ width:100%; background: rgba(47, 48, 61, 0.6); border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:14px; color:white; font-size:14px; margin-bottom:14px; outline:none; }}
            .input-field:focus {{ border-color:#25f4ee; box-shadow: 0 0 10px rgba(37,244,238,0.3); }}
            
            .btn-create {{ width:100%; background: linear-gradient(45deg, #fe2c55, #ff5574); border:none; color:white; padding:15px; border-radius:12px; font-weight:bold; font-size:16px; cursor:pointer; box-shadow: 0 4px 15px rgba(254,44,85,0.4); }}
            
            .room-list-title {{ font-size:15px; color:#888; margin-bottom:15px; font-weight:bold; z-index: 2; }}
            .room-item {{ background: rgba(22, 23, 34, 0.6); border:1px solid rgba(255,255,255,0.05); padding:18px; border-radius:16px; display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; cursor:pointer; transition: all 0.3s; z-index: 2; }}
            .room-item:hover {{ background: rgba(37,244,238,0.05); border-color: rgba(37,244,238,0.2); }}

            /* 🗂️ ታቦች */
            .tab-screen {{ display:none; position:absolute; top:0; left:0; width:100%; height:calc(100% - 70px); background:#060713; z-index:400; padding:25px 20px; overflow-y:auto; }}
            .page-title {{ font-size:24px; font-weight:800; color:#25f4ee; margin-bottom:25px; text-align:center; }}
            .info-card {{ background: rgba(22, 23, 34, 0.7); border:1px solid rgba(255,255,255,0.06); border-radius:20px; padding:25px; margin-bottom:20px; text-align:center; }}
            
            /* 🎙️ የውስጥ ሩም */
            .app-container {{ display: none; position: relative; width: 100%; height: 100%; flex-direction: column; background: #060713; }}
            .top-bar {{ display: flex; justify-content: space-between; align-items: center; padding: 15px 20px; border-bottom: 1px solid rgba(255,255,255,0.05); z-index: 10; }}
            .live-tag {{ background: linear-gradient(45deg, #fe2c55, #ff0033); padding: 5px 14px; border-radius: 20px; font-weight: 800; font-size: 11px; box-shadow: 0 0 10px rgba(254,44,85,0.5); }}
            .room-name-display {{ font-size:13px; font-weight:bold; color:#25f4ee; background:rgba(37,244,238,0.15); border: 1px solid rgba(37,244,238,0.2); padding:5px 14px; border-radius:20px; }}
            
            /* 🌊 የድምፅ ሞገድ */
            .wave-container {{ width:90%; height:40px; background:rgba(0,0,0,0.4); margin: 0 auto 10px auto; display:none; border-radius:12px; overflow:hidden; border: 1px solid rgba(37,244,238,0.1); }}
            .wave-canvas {{ width:100%; height:100%; }}

            .stage-area {{ flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 10px; z-index: 5; overflow-y: auto; }}
            .host-section {{ text-align: center; margin-bottom: 15px; position: relative; }}
            
            .host-avatar {{ width: 80px; height: 80px; border-radius: 50%; background: #111; border: 3px solid #fe2c55; display: flex; align-items: center; justify-content: center; font-size: 36px; margin: 0 auto 5px auto; box-shadow: 0 0 20px rgba(254,44,85,0.4); }}

            .seats-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; width: 100%; max-width: 360px; margin-bottom: 10px; }}
            .seat-circle {{ width: 55px; height: 55px; border-radius: 50%; background: #161722; border: 2px solid #25f4ee; display: flex; align-items: center; justify-content: center; font-size: 22px; margin: 0 auto 4px auto; cursor: pointer; }}
            .seat-circle.empty {{ border-color: rgba(255,255,255,0.15); background: rgba(255,255,255,0.03); color: #555; }}
            .seat-name {{ font-size: 11px; color: #bbb; text-align:center; }}
            
            /* 🎛️ Soundboard & Lucky Draw Panel */
            .utility-bar {{ display: flex; justify-content: space-around; width: 100%; background: rgba(255,255,255,0.02); padding: 8px; border-top: 1px solid rgba(255,255,255,0.05); border-bottom: 1px solid rgba(255,255,255,0.05); z-index: 10; }}
            .util-btn {{ background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: white; padding: 6px 12px; border-radius: 15px; font-size: 11px; font-weight: bold; cursor: pointer; }}
            .util-btn:active {{ background: #25f4ee; color: #000; }}

            /* 💬 የላይቭ ቻት ክልል */
            .chat-area {{ height: 130px; width: 100%; padding: 12px; background: linear-gradient(transparent, rgba(6,7,19,0.98)); overflow-y: auto; font-size: 12px; display: flex; flex-direction: column; gap: 5px; z-index: 10; }}
            
            /* ✍️ የፅሁፍ መፃፊያ ባር */
            .chat-input-container {{ display: flex; padding: 10px 15px; background: #0b0c1e; border-top: 1px solid rgba(255,255,255,0.05); z-index: 12; gap: 10px; align-items: center; }}
            .chat-input {{ flex: 1; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 10px 15px; color: #fff; font-size: 13px; outline: none; }}
            .btn-send-text {{ background: #25f4ee; border: none; color: #060713; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; cursor: pointer; }}

            .bottom-controls {{ display: flex; justify-content: space-between; align-items: center; padding: 12px 20px; background: #060713; z-index: 10; border-top: 1px solid rgba(255,255,255,0.05); }}
            
            /* 🧭 የታችኛው ሜኑ */
            .bottom-nav {{ position:absolute; bottom:0; left:0; width:100%; height:70px; background: rgba(22, 23, 34, 0.85); backdrop-filter: blur(15px); border-top:1px solid rgba(255,255,255,0.06); display:flex; justify-content:space-around; align-items:center; z-index:1000; }}
            .nav-item {{ display:flex; flex-direction:column; align-items:center; color:#666b86; font-size:11px; font-weight:600; cursor:pointer; }}
            .nav-item.active {{ color:#25f4ee; }}
            .nav-icon {{ font-size:22px; margin-bottom:4px; }}

            /* 🎁 የስጦታዎች መምረጫ ፓናል */
            .gift-overlay {{ display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.6); z-index:2000; align-items:flex-end; }}
            .gift-tray {{ width:100%; background:#10111e; border-top: 2px solid rgba(255,255,255,0.1); border-radius:24px 24px 0 0; padding:20px; display:grid; grid-template-columns: repeat(4, 1fr); gap:12px; }}
            .gift-card {{ background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05); border-radius:16px; padding:12px 5px; text-align:center; cursor:pointer; }}
            .gift-emoji {{ font-size:30px; margin-bottom:5px; }}
            .gift-title {{ font-size:11px; color:#fff; font-weight:bold; }}
            .gift-price {{ font-size:10px; color:#00cd63; margin-top:3px; font-weight:bold; }}

            /* 🎬 ሲኒማቲክ የስጦታ አኒሜሽን ማሳያ */
            .cinematic-stage {{ display:none; position:fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:2500; align-items:center; justify-content:center; }}
            .big-gift-anim {{ font-size:120px; animation: cinematicBlast 1.5s forwards cubic-bezier(0.175, 0.885, 0.32, 1.275); }}
            @keyframes cinematicBlast {{
                0% {{ transform: scale(0) rotate(-45deg); opacity: 0; }}
                30% {{ transform: scale(1.3) rotate(10deg); opacity: 1; }}
                50% {{ transform: scale(1) rotate(0deg); }}
                100% {{ opacity: 0; transform: scale(0.6) translateY(-150px); }}
            }}
        </style>
    </head>
    <body>

        <div class="bg-glow"></div>
        <div class="bg-glow-right"></div>

        <audio id="bg-kirar-audio" loop>
            <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mp3">
        </audio>
        <audio id="snd-applause"><source src="https://actions.google.com/sounds/v1/human/applause.ogg" type="audio/ogg"></audio>
        <audio id="snd-laughter"><source src="https://actions.google.com/sounds/v1/human/laughter.ogg" type="audio/ogg"></audio>

        <div class="bottom-nav" id="main-nav-bar">
            <div class="nav-item active" id="nav-home" onclick="switchTab('home')">
                <div class="nav-icon">🎙️</div>
                <div>ክфሎች</div>
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
                <div class="room-item" onclick="joinExistingRoom('🌍 የስደት ወግ (Diaspora Lounge)')">
                    <div>
                        <div style="font-weight:bold; color:#ffdd67; font-size:15px;">🌍 የስደት ወግ (Diaspora Lounge) ⭐</div>
                        <div style="font-size:12px; color:#aaa; margin-top:3px;">በአረብ ሀገር ያሉ እህት ወንድሞች የናፍቆትና የህይወት ወግ መጋሪያ</div>
                    </div>
                    <div style="color:#25f4ee; font-size:12px; font-weight:bold; background:rgba(37,244,238,0.1); padding:6px 12px; border-radius:12px;">🎙️ ግባ</div>
                </div>

                <div class="room-item" onclick="joinExistingRoom('⚽ የኳስ ሜዳ (Football Fan Zone)')">
                    <div>
                        <div style="font-weight:bold; color:#00ff7f; font-size:15px;">⚽ የኳስ ሜዳ (Football Fan Zone) 🔥</div>
                        <div style="font-size:12px; color:#aaa; margin-top:3px;">የእግር ኳስ ጨዋታዎች፣ ትንታኔዎች እና የደጋፊዎች ሙቅ ክርክር</div>
                    </div>
                    <div style="color:#25f4ee; font-size:12px; font-weight:bold; background:rgba(37,244,238,0.1); padding:6px 12px; border-radius:12px;">🎙️ ግባ</div>
                </div>

                <div class="room-item" onclick="joinExistingRoom('👵 የእናቶች ወግ (Mela Lounge)')">
                    <div>
                        <div style="font-weight:bold; color:#fff; font-size:15px;">👵 የእናቶች ወግ (Mela Lounge)</div>
                        <div style="font-size:12px; color:#888; margin-top:3px;">የባህል ወጎች፣ ምክሮች እና ማህበራዊ ጨዋታዎች</div>
                    </div>
                    <div style="color:#25f4ee; font-size:12px; font-weight:bold; background:rgba(37,244,238,0.1); padding:6px 12px; border-radius:12px;">🎙️ ግባ</div>
                </div>

                <div class="room-item" onclick="joinExistingRoom('📚 የተማሪዎች መወያያ (Mela Room)')">
                    <div>
                        <div style="font-weight:bold; color:#fff; font-size:15px;">📚 የተማሪዎች መወያያ (Mela Room)</div>
                        <div style="font-size:12px; color:#888; margin-top:3px;">ለትምህርት፣ ለዕውቀት እና ለክህሎት ማሳደጊያ ውይይት</div>
                    </div>
                    <div style="color:#25f4ee; font-size:12px; font-weight:bold; background:rgba(37,244,238,0.1); padding:6px 12px; border-radius:12px;">🎙️ ግባ</div>
                </div>
            </div>
        </div>

        <div class="tab-screen" id="wallet-screen">
            <div class="page-title">My Mela Wallet</div>
            <div class="info-card">
                <div style="font-size:14px; color:#888;">የአሁኑ የኮይን ባላንስዎ</div>
                <div style="font-size:38px; font-weight:900; color:#00cd63; margin:10px 0;">🪙 <span id="wallet-coin-balance">350</span></div>
                <div style="font-size:12px; color:#888;">( 10 ኮይን = 1 የኢትዮጵያ ብር )</div>
            </div>
            <button class="btn-create" style="background: linear-gradient(45deg, #00cd63, #00ff7f); margin-bottom:14px;" onclick="alert('በቴሌብር ኮይን መግዣ ሲስተም በቅርቡ ይበራል።')">💳 በቴሌብር ኮይን ግዛ (Top Up)</button>
        </div>

        <div class="tab-screen" id="referral-screen">
            <div class="page-title">ጋብዘው ይክበሩ (Refer & Earn)</div>
            <div class="info-card">
                <h3 style="color:#fff; margin-bottom:10px;">ለእያንዳንዱ ሰው 20 ነፃ ኮይን!</h3>
                <p style="font-size:13px; color:#888;">የእርስዎን መለያ ሊንክ ለጓደኞችዎ ያጋሩ፤ እነሱ ሲቀላቀሉ ለእርስዎ ኮይን እንሰጣለን!</p>
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
                <div class="wave-container" id="wave-visualizer-box"><canvas id="wave-canvas" class="wave-canvas"></canvas></div>
                <div class="host-section">
                    <div class="host-avatar">🎙️</div>
                    <div style="font-size:13px; font-weight:bold; color:#fff;" id="room-host-name">---</div>
                </div>
                <div class="seats-grid" id="seats-container"></div>
            </div>

            <div class="utility-bar">
                <button class="util-btn" style="border-color:#ffdd67; color:#ffdd67;" onclick="runLuckyDraw()">🎰 Lucky Draw (10 🪙)</button>
                <button class="util-btn" onclick="playEffect('applause')">👏 ጭብጨባ</button>
                <button class="util-btn" onclick="playEffect('laughter')">😂 ሳቅ</button>
            </div>

            <div class="chat-area" id="chat-box"></div>

            <div class="chat-input-container">
                <input type="text" id="text-msg-input" class="chat-input" placeholder="ሀሳብዎን እዚህ ይፃፉ..." onkeypress="if(event.key==='Enter') sendTextMessage()">
                <button class="btn-send-text" onclick="sendTextMessage()">➔</button>
            </div>
            
            <div class="bottom-controls">
                <button class="action-btn" style="background: linear-gradient(45deg, #25f4ee, #00bfff); color:#060713; border:none; padding:11px 18px; border-radius:25px; font-weight:800; font-size:13px; cursor:pointer;" onclick="requestSeatAuto()">🎙️ መቀመጫ ያዝ</button>
                <div style="display:flex; align-items:center;">
                    <button class="action-btn" style="background: linear-gradient(45deg, #fe2c55, #ff5574); padding:11px 18px; font-weight:800; font-size:13px; border-radius:25px;" onclick="openGiftTray()">🎁 ስጦታ</button>
                    <div class="nav-icon" style="background: rgba(255,255,255,0.06); width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; cursor: pointer; margin-left:10px;" id="mic-toggle-btn" onclick="toggleMic()">🔊</div>
                </div>
            </div>
        </div>

        <div class="gift-overlay" id="gift-modal-overlay" onclick="closeGiftTray()">
            <div class="gift-tray" onclick="event.stopPropagation()">
                <div class="gift-card" onclick="processGiftSend('🌹 ጽጌረዳ', 10, '🌹')">
                    <div class="gift-emoji">🌹</div><div class="gift-title">ጽጌረዳ</div><div class="gift-price">🪙 10</div>
                </div>
                <div class="gift-card" onclick="processGiftSend('☕ የጀበና ቡና', 50, '☕')">
                    <div class="gift-emoji">☕</div><div class="gift-title">ጀበና ቡና</div><div class="gift-price">🪙 50</div>
                </div>
                <div class="gift-card" onclick="processGiftSend('🦁 አንበሳ', 200, '🦁')">
                    <div class="gift-emoji">🦁</div><div class="gift-title">አንበሳ</div><div class="gift-price">🪙 200</div>
                </div>
                <div class="gift-card" onclick="processGiftSend('👑 የMela አክሊል', 500, '👑')">
                    <div class="gift-emoji">👑</div><div class="gift-title">የMela አክሊል</div><div class="gift-price">🪙 500</div>
                </div>
            </div>
        </div>

        <div class="cinematic-stage" id="animation-stage-layer"><div class="big-gift-anim" id="big-gift-emoji-element">👑</div></div>

        <script>
            const AGORA_APP_ID = "ea7dfdf9926d400fb8a54d31be0bd44c"; 
            let client = AgoraRTC.createClient({{ mode: "rtc", codec: "vp8" }});
            let localAudioTrack = null;
            let currentSeat = null;
            let myUsername = "እንግዳ";
            let currentRoomName = "";
            let myCoins = 350; 
            
            let audioContext = null; let analyser = null; let dataArray = null; let animationFrameId = null;
            let seatsData = {{ 1:{{name:"ባዶ",active:false}}, 2:{{name:"ባዶ",active:false}}, 3:{{name:"ባዶ",active:false}}, 4:{{name:"ባዶ",active:false}}, 5:{{name:"ባዶ",active:false}}, 6:{{name:"ባዶ",active:false}} }};

            function switchTab(tabName) {{
                document.getElementById("lobby-screen").style.display = "none";
                document.getElementById("wallet-screen").style.display = "none";
                document.getElementById("referral-screen").style.display = "none";
                document.getElementById("nav-home").classList.remove("active");
                document.getElementById("nav-wallet").classList.remove("active");
                document.getElementById("nav-ref").classList.remove("active");
                
                if(tabName === 'home') {{ document.getElementById("lobby-screen").style.display = "flex"; document.getElementById("nav-home").classList.add("active"); }}
                else if(tabName === 'wallet') {{ document.getElementById("wallet-screen").style.display = "block"; document.getElementById("nav-wallet").classList.add("active"); }}
                else if(tabName === 'referral') {{ document.getElementById("referral-screen").style.display = "block"; document.getElementById("nav-ref").classList.add("active"); }}
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
                document.getElementById("room-screen").style.display = "flex";
                document.getElementById("active-room-title").innerText = currentRoomName;
                document.getElementById("room-host-name").innerText = currentRoomName + " (Host)";
                document.getElementById("chat-box").innerHTML = "";
                
                // 🎵 አውቶሜትድ ክራር ማጫወቻ
                const audio = document.getElementById("bg-kirar-audio");
                audio.volume = 0.15; // ረጭ ያለ የጀርባ ድምፅ
                audio.play().catch(e => console.log("Autoplay prevented, will play on user action."));

                appendChat("🚀 Mela System", ` ወደ "${{currentRoomName}}" ክፍል በሰላም መጡ!`, "color:#25f4ee; font-weight:bold;");
                
                // 👑 ቪአይፒ መግቢያ ማስታወቂያ (በራሱ ጊዜ የሚሰራ)
                if(myCoins >= 300) {{
                    setTimeout(() => {{
                        appendChat("👑 Mela VIP", ` ትልቁ ባለክብር [${{myUsername}}] በታላቅ ክብር ክፍሉን ተቀላቅለዋል!`, "color:#ffdd67; font-weight:bold; text-shadow:0 0 8px #ffdd67; background:rgba(255,221,103,0.05); padding:6px; border-radius:6px;");
                    }}, 1000);
                }}

                renderSeats();
                initAgora(currentRoomName);
            }}

            function sendTextMessage() {{
                const inputEl = document.getElementById("text-msg-input");
                const msgText = inputEl.value.trim();
                if(!msgText) return;
                appendChat(myUsername, msgText, "color: #fff; background: rgba(255,255,255,0.02); padding: 4px 8px; border-radius: 6px;");
                inputEl.value = ""; 
            }}

            // 🎰 አውቶሜትድ የእድል ቁጥር ጨዋታ (Lucky Draw Engine)
            function runLuckyDraw() {{
                if(myCoins < 10) {{ alert("ለቲኬት የሚሆን በቂ ኮይን የለዎትም!"); return; }}
                myCoins -= 10;
                document.getElementById("wallet-coin-balance").innerText = myCoins;
                
                appendChat("🎰 ሎተሪ", `[${{myUsername}}] የዕድል ቁጥር ቲኬት በ 10 ኮይን ገዝተዋል። እጣው እየወጣ ነው...`, "color:#ffdd67; font-weight:bold;");
                
                setTimeout(() => {{
                    const win = Math.random() > 0.5;
                    if(win) {{
                        myCoins += 50;
                        document.getElementById("wallet-coin-balance").innerText = myCoins;
                        appendChat("🎉 ጃክፖት", ` እንኳን ደስ አለዎት! [${{myUsername}}] የእድል ቁጥር እጣው ደርሶዎት 50 ኮይን 🪙 ዋሌትዎ ላይ ተጨምሯል!`, "color:#00cd63; font-weight:bold; background:rgba(0,205,99,0.1); padding:6px; border-radius:6px;");
                        playEffect('applause');
                    }} else {{
                        appendChat("🎰 ሎተሪ", `ይቅርታ እጣው አልደረሶትም። በድጋሚ ይሞክሩ!`, "color:#888;");
                    }}
                }}, 2500);
            }}

            // 👏 የድምፅ ተፅዕኖዎች ማጫወቻ
            function playEffect(type) {{
                const aud = document.getElementById(type === 'applause' ? 'snd-applause' : 'snd-laughter');
                aud.currentTime = 0; aud.play();
                appendChat("🎙️ Soundboard", ` [${{myUsername}}] የ${{type === 'applause'?'ጭብጨባ':'ሳቅ'}} ድምፅ ተፅዕኖ ተጠቅመዋል`, "color:#aaa; font-size:11px;");
            }}

            function openGiftTray() {{ document.getElementById("gift-modal-overlay").style.display = "flex"; }}
            function closeGiftTray() {{ document.getElementById("gift-modal-overlay").style.display = "none"; }}

            function processGiftSend(giftName, price, emoji) {{
                if (myCoins < price) {{ alert(`ይቅርታ! ባላንስዎ በቂ አይደለም።`); closeGiftTray(); return; }}
                myCoins -= price;
                document.getElementById("wallet-coin-balance").innerText = myCoins;
                closeGiftTray();

                const stage = document.getElementById("animation-stage-layer");
                const emojiEl = document.getElementById("big-gift-emoji-element");
                emojiEl.innerText = emoji; stage.style.display = "flex";
                setTimeout(() => {{ stage.style.display = "none"; }}, 1500);

                appendChat("🎁 GIFT", `${{myUsername}} ለክፍሉ ${{giftName}} ${{emoji}} (በ ${{price}} ኮይን) በክብር አበርክተዋል!`, "color:#ff5574; font-weight:bold; background:rgba(254,44,85,0.05); padding:6px;");
            }}

            async function exitRoom() {{
                document.getElementById("bg-kirar-audio").pause();
                if(localAudioTrack) {{ localAudioTrack.stop(); localAudioTrack.close(); localAudioTrack = null; }}
                stopVoiceWave(); await client.leave(); currentSeat = null;
                for(let i=1; i<=6; i++) seatsData[i] = {{ name: "ባዶ", active: false }};
                document.getElementById("room-screen").style.display = "none";
                document.getElementById("main-nav-bar").style.display = "flex";
                switchTab('home');
            }}

            function renderSeats() {{
                const container = document.getElementById("seats-container"); container.innerHTML = "";
                for (let i = 1; i <= 6; i++) {{
                    const seat = seatsData[i]; const node = document.createElement("div");
                    node.innerHTML = `<div class="seat-circle ${{seat.active ? '' : 'empty'}}" onclick="claimSeat(${{i}})">${{seat.active?'👤':'➕'}}</div><div class="seat-name">${{seat.name}}</div>`;
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
                currentSeat = seatId; seatsData[seatId] = {{ name: myUsername, active: true }}; renderSeats();
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
                if (localAudioTrack.muted) {{ await localAudioTrack.setMuted(false); btn.innerText = "🔊"; }} 
                else {{ await localAudioTrack.setMuted(true); btn.innerText = "🔇"; }}
            }}

            function startVoiceWave(mediaStreamTrack) {{
                document.getElementById("wave-visualizer-box").style.display = "block";
                const stream = new MediaStream([mediaStreamTrack]);
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
                const source = audioContext.createMediaStreamSource(stream);
                analyser = audioContext.createAnalyser(); analyser.fftSize = 64; source.connect(analyser);
                dataArray = new Uint8Array(analyser.frequencyBinCount);
                const canvas = document.getElementById("wave-canvas"); const canvasCtx = canvas.getContext("2d");
                function drawWave() {{
                    animationFrameId = requestAnimationFrame(drawWave); analyser.getByteFrequencyData(dataArray);
                    canvasCtx.fillStyle = "#060713"; canvasCtx.fillRect(0, 0, canvas.width, canvas.height);
                    const barWidth = (canvas.width / analyser.frequencyBinCount) * 1.5; let barHeight; let x = 0;
                    for(let i = 0; i < analyser.frequencyBinCount; i++) {{
                        barHeight = dataArray[i] * 0.4; canvasCtx.fillStyle = `rgb(${{barHeight+50}}, 244, 238)`;
                        canvasCtx.fillRect(x, canvas.height - barHeight, barWidth - 2, barHeight); x += barWidth;
                    }}
                }}
                drawWave();
            }}

            function stopVoiceWave() {{ if(animationFrameId) cancelAnimationFrame(animationFrameId); if(audioContext) audioContext.close(); }}
            function appendChat(user, msg, style = "") {{
                const box = document.getElementById("chat-box"); const div = document.createElement("div");
                div.style = style; div.innerHTML = `<b>${{user}}:</b> ${{msg}}`; box.appendChild(div); box.scrollTop = box.scrollHeight;
            }}
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
