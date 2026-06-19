import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Mela Space - Ultimate 3D Masterpiece")

# 📱 ያንተ መረጃ
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
        <title>Mela Space - Ultimate 3D Edition</title>
        <script src="https://download.agora.io/sdk/release/AgoraRTC_N-4.18.0.js"></script>
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Roboto, sans-serif; }}
            body, html {{ width: 100%; height: 100%; overflow: hidden; background: #060713; color: #fff; }}
            
            /* ✨ Neon Background Glows */
            .bg-glow {{ position: absolute; width: 300px; height: 300px; background: radial-gradient(circle, rgba(37,244,238,0.15) 0%, rgba(0,0,0,0) 70%); top: -50px; left: -50px; z-index: 1; pointer-events: none; }}
            .bg-glow-right {{ position: absolute; width: 300px; height: 300px; background: radial-gradient(circle, rgba(254,44,85,0.12) 0%, rgba(0,0,0,0) 70%); bottom: 50px; right: -50px; z-index: 1; pointer-events: none; }}

            /* 🚪 ሎቢ ገጽ */
            .lobby-container {{ position: absolute; top:0; left:0; width:100%; height:calc(100% - 70px); background:#060713; z-index:500; display:flex; flex-direction:column; padding:20px; overflow-y:auto; }}
            .lobby-header {{ text-align:center; margin: 10px 0; z-index: 2; }}
            .lobby-title {{ color:#25f4ee; font-size:26px; font-weight:900; text-shadow: 0 0 20px rgba(37,244,238,0.6); }}
            
            .create-room-box {{ background: rgba(22, 23, 34, 0.7); backdrop-filter: blur(10px); border:1px solid rgba(255,255,255,0.07); border-radius:20px; padding:20px; margin-bottom:20px; box-shadow: 0 8px 32px rgba(0,0,0,0.3); z-index: 2; }}
            .input-field {{ width:100%; background: rgba(47, 48, 61, 0.6); border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:12px; color:white; font-size:14px; margin-bottom:12px; outline:none; transition: all 0.3s; }}
            .input-field:focus {{ border-color: #25f4ee; box-shadow: 0 0 10px rgba(37,244,238,0.3); }}
            
            .checkbox-container {{ display: flex; align-items: center; gap: 8px; margin-bottom: 12px; font-size: 13px; color: #aaa; }}
            
            /* 🚀 3D Animated Buttons */
            .btn-3d {{ 
                width:100%; 
                background: linear-gradient(180deg, #fe2c55, #d2143a); 
                border: none; 
                color: white; 
                padding: 14px; 
                border-radius: 14px; 
                font-weight: bold; 
                font-size: 16px; 
                cursor: pointer; 
                position: relative;
                box-shadow: 0 5px 0 #990b24, 0 8px 15px rgba(0,0,0,0.4), 0 0 15px rgba(254,44,85,0.3);
                transition: all 0.1s ease;
                transform: translateY(0);
            }}
            .btn-3d:active {{
                transform: translateY(4px);
                box-shadow: 0 1px 0 #990b24, 0 2px 5px rgba(0,0,0,0.4);
            }}
            
            .btn-3d-green {{ 
                background: linear-gradient(180deg, #00cd63, #009647); 
                box-shadow: 0 5px 0 #00632f, 0 8px 15px rgba(0,0,0,0.4), 0 0 15px rgba(0,205,99,0.3); 
            }}
            .btn-3d-green:active {{ box-shadow: 0 1px 0 #00632f, 0 2px 5px rgba(0,0,0,0.4); }}

            .room-list-title {{ font-size:15px; color:#888; margin-bottom:12px; font-weight:bold; z-index: 2; }}
            .room-item {{ background: rgba(22, 23, 34, 0.6); border:1px solid rgba(255,255,255,0.05); padding:15px; border-radius:16px; display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; cursor:pointer; transition: transform 0.2s; z-index: 2; }}
            .room-item:active {{ transform: scale(0.97); }}

            /* 🗂️ የታብ ገፆች */
            .tab-screen {{ display:none; position:absolute; top:0; left:0; width:100%; height:calc(100% - 70px); background:#060713; z-index:400; padding:20px; overflow-y:auto; }}
            .page-title {{ font-size:24px; font-weight:800; color:#25f4ee; margin-bottom:20px; text-align:center; }}
            .info-card {{ background: rgba(22, 23, 34, 0.7); border:1px solid rgba(255,255,255,0.06); border-radius:20px; padding:20px; margin-bottom:15px; text-align:center; }}
            
            /* 🎙️ ዋናው የውስጥ ሩም */
            .app-container {{ display: none; position: relative; width: 100%; height: 100%; flex-direction: column; background: #060713; }}
            .top-bar {{ display: flex; justify-content: space-between; align-items: center; padding: 12px 20px; border-bottom: 1px solid rgba(255,255,255,0.05); z-index: 10; }}
            .live-tag {{ background: linear-gradient(45deg, #fe2c55, #ff0033); padding: 5px 12px; border-radius: 20px; font-weight: 800; font-size: 11px; }}
            .room-name-display {{ font-size:13px; font-weight:bold; color:#25f4ee; background:rgba(37,244,238,0.15); border: 1px solid rgba(37,244,238,0.2); padding:5px 12px; border-radius:20px; }}
            
            /* ⏱️ ማይክ ሰዓት ቆጣሪ ቪው */
            .time-reward-badge {{ font-size:12px; color:#ffdd67; background: rgba(255,221,103,0.15); padding: 5px 12px; border-radius: 12px; font-weight: bold; margin-top: 6px; display: inline-block; border: 1px dashed rgba(255,221,103,0.3); }}

            /* 🎬 የቪዲዮ ሲኒማ ቦክስ */
            .video-stage-box {{ width: 90%; max-width: 360px; height: 140px; background: #000; margin: 5px auto; border-radius: 14px; overflow: hidden; border: 2px solid rgba(37,244,238,0.3); box-shadow: 0 0 15px rgba(37,244,238,0.2); position: relative; }}
            .video-element {{ width: 100%; height: 100%; object-fit: cover; }}

            .wave-container {{ width:90%; height:35px; background:rgba(0,0,0,0.4); margin: 5px auto; display:block; border-radius:12px; overflow:hidden; border: 1px solid rgba(37,244,238,0.1); }}
            .wave-canvas {{ width:100%; height:100%; }}

            .stage-area {{ flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; padding: 4px; z-index: 5; overflow-y: auto; }}
            .host-section {{ text-align: center; margin-bottom: 8px; position: relative; }}
            .host-avatar {{ width: 65px; height: 65px; border-radius: 50%; background: #111; border: 3px solid #fe2c55; display: flex; align-items: center; justify-content: center; font-size: 30px; margin: 0 auto 4px auto; box-shadow: 0 0 15px rgba(254,44,85,0.3); }}
            .host-badge {{ position: absolute; top: 0; right: 12px; background: #ffdd67; color: #000; font-size: 10px; padding: 2px 6px; border-radius: 10px; font-weight: bold; }}

            .seats-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; width: 100%; max-width: 360px; margin-bottom: 6px; }}
            .seat-circle {{ width: 48px; height: 48px; border-radius: 50%; background: #161722; border: 2px solid #25f4ee; display: flex; align-items: center; justify-content: center; font-size: 18px; margin: 0 auto 3px auto; cursor: pointer; position: relative; box-shadow: inset 0 0 8px rgba(37,244,238,0.2); }}
            .seat-circle.empty {{ border-color: rgba(255,255,255,0.15); background: rgba(255,255,255,0.03); color: #555; box-shadow: none; }}
            .seat-name {{ font-size: 11px; color: #bbb; text-align:center; }}
            
            .mod-indicator {{ position: absolute; top: -5px; right: -5px; background: #00bfff; color: black; font-size: 8px; padding: 1px 4px; border-radius: 5px; font-weight: bold; display: none; }}

            /* 🗛 Control Panel */
            .utility-bar {{ display: flex; flex-direction: column; gap: 6px; width: 100%; background: rgba(255,255,255,0.02); padding: 8px; border-top: 1px solid rgba(255,255,255,0.05); border-bottom: 1px solid rgba(255,255,255,0.05); z-index: 10; }}
            .button-row {{ display: flex; justify-content: space-around; width: 100%; gap: 5px; flex-wrap: wrap; }}
            
            .btn-3d-sm {{
                background: linear-gradient(180deg, rgba(255,255,255,0.1), rgba(255,255,255,0.03));
                border: 1px solid rgba(255,255,255,0.12);
                color: white; padding: 6px 8px; border-radius: 10px; font-size: 11px; font-weight: bold; cursor: pointer;
                box-shadow: 0 3px 0 rgba(0,0,0,0.3); transition: all 0.1s; text-align: center; flex: 1; min-width: 70px;
            }}
            .btn-3d-sm:active {{ transform: translateY(2px); box-shadow: 0 1px 0 rgba(0,0,0,0.3); }}

            .slider-fx-container {{ display: flex; flex-direction: column; gap: 5px; width: 95%; margin: 0 auto; }}
            .volume-control-box {{ display: flex; align-items: center; justify-content: center; gap: 10px; font-size: 11px; color: #aaa; }}
            .volume-slider {{ flex: 1; -webkit-appearance: none; background: rgba(255,255,255,0.1); height: 5px; border-radius: 3px; outline: none; }}
            .volume-slider::-webkit-slider-thumb {{ -webkit-appearance: none; appearance: none; width: 14px; height: 14px; border-radius: 50%; background: #25f4ee; cursor: pointer; }}
            
            .fx-box {{ display: flex; justify-content: space-between; gap: 5px; align-items: center; font-size: 11px; color: #888; }}
            .fx-select {{ background: #161722; border: 1px solid rgba(255,255,255,0.1); color: white; border-radius: 8px; padding: 4px 8px; font-size: 11px; outline: none; }}

            /* 💬 የላይቭ ቻት ክልል */
            .chat-area {{ height: 95px; width: 100%; padding: 10px; background: linear-gradient(transparent, rgba(6,7,19,0.98)); overflow-y: auto; font-size: 12px; display: flex; flex-direction: column; gap: 5px; z-index: 10; scroll-behavior: smooth; }}
            
            /* ✍️ የፅሁፍ መፃፊያ ባር */
            .chat-input-container {{ display: flex; padding: 8px 15px; background: #0b0c1e; border-top: 1px solid rgba(255,255,255,0.05); z-index: 12; gap: 10px; align-items: center; }}
            .chat-input {{ flex: 1; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 10px 15px; color: #fff; font-size: 13px; outline: none; }}
            .btn-send-text {{ background: #25f4ee; border: none; color: #060713; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; cursor: pointer; box-shadow: 0 3px 0 #1bcfca; transition: all 0.1s; }}
            .btn-send-text:active {{ transform: translateY(2px); box-shadow: 0 1px 0 #1bcfca; }}

            .bottom-controls {{ display: flex; justify-content: space-between; align-items: center; padding: 8px 20px; background: #060713; z-index: 10; border-top: 1px solid rgba(255,255,255,0.05); }}
            
            /* 🧭 የታችኛው ሜኑ */
            .bottom-nav {{ position:absolute; bottom:0; left:0; width:100%; height:70px; background: rgba(22, 23, 34, 0.85); backdrop-filter: blur(15px); border-top:1px solid rgba(255,255,255,0.06); display:flex; justify-content:space-around; align-items:center; z-index:1000; }}
            .nav-item {{ display:flex; flex-direction:column; align-items:center; color:#666b86; font-size:11px; font-weight:600; cursor:pointer; }}
            .nav-item.active {{ color:#25f4ee; }}
            .nav-icon {{ font-size:22px; margin-bottom:4px; }}

            /* Overlays */
            .gift-overlay {{ display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.7); z-index:2000; align-items:flex-end; }}
            .gift-tray {{ width:100%; background:#10111e; border-top: 2px solid rgba(255,255,255,0.1); border-radius:24px 24px 0 0; padding:20px; display:grid; grid-template-columns: repeat(4, 1fr); gap:12px; }}
            .gift-card {{ background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05); border-radius:16px; padding:12px 5px; text-align:center; cursor:pointer; transition: transform 0.2s; }}
            .gift-card:active {{ transform: scale(0.9); }}
            .gift-emoji {{ font-size:30px; margin-bottom:5px; }}

            /* 🎡 Wheel UI */
            .wheel-box {{ width: 100%; background: #10111e; padding: 25px; border-radius: 24px 24px 0 0; text-align: center; color: white; }}
            .wheel-graphic {{ width: 160px; height: 160px; border-radius: 50%; border: 8px solid #25f4ee; margin: 15px auto; display: flex; align-items: center; justify-content: center; font-size: 40px; font-weight: bold; background: conic-gradient(#fe2c55 0% 25%, #00ff7f 25% 50%, #00bfff 50% 75%, #ffdd67 75% 100%); transition: transform 3s cubic-bezier(0.1, 0.8, 0.1, 1); box-shadow: 0 0 20px rgba(37,244,238,0.4); }}

            /* 🎬 ሲኒማቲክ አኒሜሽን */
            .cinematic-stage {{ display:none; position:fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:2500; align-items:center; justify-content:center; }}
            .big-gift-anim {{ font-size:120px; animation: cinematicBlast 1.5s forwards cubic-bezier(0.175, 0.885, 0.32, 1.275); }}
            @keyframes cinematicBlast {{
                0% {{ transform: scale(0) rotate(-45deg); opacity: 0; }}
                30% {{ transform: scale(1.3) rotate(10deg); opacity: 1; }}
                50% {{ transform: scale(1) rotate(0deg); }}
                100% {{ opacity: 0; transform: scale(0.6) translateY(-150px); }}
            }}
            
            .leader-row {{ display: flex; justify-content: space-between; padding: 10px; background: rgba(255,255,255,0.02); margin-bottom: 5px; border-radius: 8px; font-size: 13px; }}
        </style>
    </head>
    <body>

        <div class="bg-glow"></div>
        <div class="bg-glow-right"></div>

        <audio id="bg-kirar-audio" loop crossOrigin="anonymous">
            <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mp3">
        </audio>
        <audio id="snd-applause" crossOrigin="anonymous">
            <source src="https://www.soundjay.com/human/sounds/applause-01.mp3" type="audio/mp3">
        </audio>
        <audio id="snd-laughter" crossOrigin="anonymous">
            <source src="https://www.soundjay.com/human/sounds/laughter-01.mp3" type="audio/mp3">
        </audio>

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
            <div class="lobby-header"><div class="lobby-title">Mela Live Rooms</div></div>

            <div class="create-room-box">
                <input type="text" id="lobby-username" class="input-field" placeholder="የእርስዎን ስም ያስገቡ...">
                <input type="text" id="lobby-roomname" class="input-field" placeholder="የክፍሉን ስም ያስገቡ...">
                <div class="checkbox-container">
                    <input type="checkbox" id="lobby-is-vip">
                    <label for="lobby-is-vip">🔒 እንደ VIP (የግል ሚስጥራዊ ክፍል) ፍጠር</label>
                </div>
                <button class="btn-3d" style="margin-bottom:12px;" onclick="createNewRoomAction()">🚀 አዲስ ክፍል ፍጠር</button>
                <button class="btn-3d btn-3d-green" onclick="openWheelModal()">🎡 ዕለታዊ ዕድል ማሽከርከሪያ</button>
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
            </div>
        </div>

        <div class="tab-screen" id="wallet-screen">
            <div class="page-title">My Mela Wallet</div>
            <div class="info-card">
                <div style="font-size:14px; color:#888;">የአሁኑ የኮይን ባላንስዎ</div>
                <div style="font-size:38px; font-weight:900; color:#00cd63; margin:10px 0;">🪙 <span id="wallet-coin-balance">350</span></div>
                <div style="font-size:12px; color:#aaa; line-height:1.6; text-align:left; background:rgba(0,0,0,0.2); padding:10px; border-radius:10px;">
                    📌 <b>የአካውንት ባለቤት፦</b> {MY_NAME}<br>
                    📌 <b>የቴሌብር ቁጥር፦</b> {MY_TELEBIRR_NUMBER}
                </div>
            </div>
            <button class="btn-3d btn-3d-green" onclick="alert('የአውቶማቲክ ቴሌብር ሲስተም በቅርቡ ይበራል!')">💳 በቴሌብር ኮይን ግዛ</button>
        </div>

        <div class="tab-screen" id="referral-screen">
            <div class="page-title">ጋብዘው ይክበሩ (Refer & Earn)</div>
            <div class="info-card">
                <h3 style="color:#ffdd67; margin-bottom:12px;">🎉 ለእያንዳንዱ ሰው 20 ነፃ ኮይን!</h3>
                <p style="font-size:13px; color:#ccc; margin-bottom:15px; line-height:1.5;">ሊንኩን ተጠቅመው መተግበሪያውን ሲቀላቀሉ ለእርስዎ 20 ኮይን ዋሌትዎ ላይ ይጨመራል።</p>
                <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px; font-size:11px; color:#25f4ee; border:1px dashed rgba(37,244,238,0.3); word-break:break-all;" id="ref-link-text">
                    https://t.me/MelaSpaceBot?start=ref_{ADMIN_CHAT_ID}
                </div>
            </div>
            <button class="📋 ሊንኩን ኮፒ አድርግ" onclick="copyRefLink()">📋 ሊንኩን ኮፒ አድርግ</button>
        </div>

        <div class="app-container" id="room-screen">
            <div class="top-bar">
                <div class="live-tag" id="room-badge-type">🔴 LIVE</div>
                <div class="room-name-display" id="active-room-title">ክፍል: ---</div>
                <div style="font-size:13px; color:#fe2c55; cursor:pointer; font-weight:bold;" onclick="exitRoom()">🚪 ውጣ</div>
            </div>
            
            <div class="stage-area">
                <div class="video-stage-box">
                    <video id="room-video-player" class="video-element" autoplay loop muted playsinline>
                        <source src="https://assets.mixkit.co/videos/preview/mixkit-abstract-laser-lights-background-23232-large.mp4" type="video/mp4">
                    </video>
                </div>

                <div class="wave-container" id="wave-visualizer-box"><canvas id="wave-canvas" class="wave-canvas"></canvas></div>
                
                <div class="host-section">
                    <div class="host-avatar" id="host-crown-zone">🎙️</div>
                    <div class="host-badge">HOST</div>
                    <div style="font-size:13px; font-weight:bold; color:#fff;" id="room-host-name">---</div>
                    
                    <div class="time-reward-badge" id="mic-timer-badge">🎤 መድረክ አልወጡም</div>
                </div>
                <div class="seats-grid" id="seats-container"></div>
            </div>

            <div class="utility-bar">
                <div class="button-row">
                    <button class="btn-3d-sm" style="border-color:#ffdd67; color:#ffdd67;" onclick="runLuckyDraw()">🎰 Lucky Draw</button>
                    <button class="btn-3d-sm" style="border-color:#00ff7f; color:#00ff7f;" onclick="startBingoGame()">🎲 Bingo</button>
                    <button class="btn-3d-sm" onclick="playRealSound('applause')">👏 ጭብጨባ</button>
                    <button class="btn-3d-sm" onclick="playRealSound('laughter')">😂 ሳቅ</button>
                </div>
                
                <div class="slider-fx-container">
                    <div class="volume-control-box">
                        <span>🔇 ዜማ</span>
                        <input type="range" min="0" max="100" value="15" class="volume-slider" id="kirar-vol-slider" oninput="adjustMusicVolume(this.value)">
                        <span>🔊</span>
                    </div>
                    <div class="fx-box">
                        <span>🎬 ቪዲዮ ቀይር፦</span>
                        <select class="fx-select" id="video-selector-combo" onchange="changeRoomVideo(this.value)">
                            <option value="neon">✨ ኔዮን ሌዘር (መደበኛ)</option>
                            <option value="music">🎵 የሙዚቃ ሞገድ</option>
                            <option value="nature">🌌 ድንቅ የሰማይ ከዋክብት</option>
                            <option value="cyber">🤖 ሳይበር ፑንክ ከተማ</option>
                        </select>
                    </div>
                    <div class="fx-box">
                        <span>🎤 ድምፅ ማጣሪያ፦</span>
                        <select class="fx-select" id="voice-fx-mode" onchange="changeVoiceFX(this.value)">
                            <option value="normal">⚙️ መደበኛ ድምፅ</option>
                            <option value="echo">📻 Echo (መድረክ)</option>
                            <option value="robot">🤖 ሮቦት</option>
                        </select>
                        <button class="btn-3d-sm" style="padding:3px 10px; background:#fe2c55; max-width:80px;" onclick="toggleModMode()">🛡️ Mod ሹም</button>
                    </div>
                </div>
            </div>

            <div class="chat-area" id="chat-box"></div>

            <div class="chat-input-container">
                <input type="text" id="text-msg-input" class="chat-input" placeholder="ፅሁፍ ይፃፉ...">
                <button class="btn-send-text" onclick="sendTextMessage()">➔</button>
            </div>
            
            <div class="bottom-controls">
                <button class="btn-3d" style="max-width:140px; padding:10px;" onclick="requestSeatAuto()">🎙️ መቀመጫ ያዝ</button>
                <div style="display:flex; align-items:center;">
                    <button class="btn-3d btn-3d-green" style="max-width:100px; padding:10px; margin-right:10px;" onclick="openGiftTray()">🎁 ስጦታ</button>
                    <div class="nav-icon" style="background: rgba(255,255,255,0.06); width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; cursor: pointer; border:1px solid rgba(255,255,255,0.1);" id="mic-toggle-btn" onclick="toggleMic()">🔊</div>
                </div>
            </div>
        </div>

        <div class="gift-overlay" id="gift-modal-overlay" onclick="closeGiftTray()">
            <div class="gift-tray" id="gift-tray-zone" onclick="event.stopPropagation()">
                <div class="gift-card" onclick="processGiftSend('🌹 ጽጌረዳ', 10, '🌹')"><div class="gift-emoji">🌹</div></div>
                <div class="gift-card" onclick="processGiftSend('👑 የMela አክሊል', 500, '👑')"><div class="gift-emoji">👑</div></div>
            </div>
        </div>

        <script>
            const AGORA_APP_ID = "ea7dfdf9926d400fb8a54d31be0bd44c"; 
            let client = AgoraRTC.createClient({{ mode: "rtc", codec: "vp8" }});
            let localAudioTrack = null; let currentSeat = null;
            let myUsername = "እንግዳ"; let currentRoomName = ""; let myCoins = 350; let isModMode = false;
            
            // ⏱️ የማይክ ሰዓት እና የነፃ ኮይን መቁጠሪያ ሙሉ ሎጂክ
            let micTimerInterval = null; 
            let secondsOnMic = 0;

            let seatsData = {{ 1:{{name:"ባዶ",active:false}}, 2:{{name:"ባዶ",active:false}}, 3:{{name:"ባዶ",active:false}} }};

            function switchTab(tabName) {{
                document.getElementById("lobby-screen").style.display = "none";
                document.getElementById("wallet-screen").style.display = "none";
                document.getElementById("referral-screen").style.display = "none";
                if(tabName === 'home') document.getElementById("lobby-screen").style.display = "flex";
                if(tabName === 'wallet') document.getElementById("wallet-screen").style.display = "block";
                if(tabName === 'referral') document.getElementById("referral-screen").style.display = "block";
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
                document.getElementById("room-host-name").innerText = myUsername;
                renderSeats();
            }}

            // 🎬 ኮምቦ ቦክስ ሲቀየር ቪዲዮ የሚቀይር አዲስ ፈንክሽን
            function changeRoomVideo(videoType) {{
                const videoPlayer = document.getElementById("room-video-player");
                let videoUrl = "";
                
                if(videoType === "neon") {{
                    videoUrl = "https://assets.mixkit.co/videos/preview/mixkit-abstract-laser-lights-background-23232-large.mp4";
                }} else if(videoType === "music") {{
                    videoUrl = "https://assets.mixkit.co/videos/preview/mixkit-music-speaker-bass-membrane-pulsating-43204-large.mp4";
                }} else if(videoType === "nature") {{
                    videoUrl = "https://assets.mixkit.co/videos/preview/mixkit-nebula-in-outer-space-40176-large.mp4";
                }} else if(videoType === "cyber") {{
                    videoUrl = "https://assets.mixkit.co/videos/preview/mixkit-tunnel-of-futuristic-blue-neon-lights-42211-large.mp4";
                }}
                
                videoPlayer.src = videoUrl;
                videoPlayer.play();
                appendChat("🎬 ሲኒማ", ` [${{myUsername}}] የክፍሉን ቪዲዮ ቀይሮታል!`, "color:#00ff7f;");
            }}

            // 🎙️ መቀመጫ ሲይዝ ሰዓት ቆጣሪውን የሚያስጀምር ሎጂክ
            function requestSeatAuto() {{
                if(currentSeat !== null) {{
                    alert("አሁን መድረክ ላይ ነዎት!");
                    return;
                }}
                currentSeat = 1; 
                seatsData[1] = {{name: myUsername, active: true}};
                renderSeats();
                appendChat("🎙️ ሲስተም", `${{myUsername}} መድረክ ላይ ወጣ! ሰዓት መቆጠር ጀምሯል።`, "color:#ffdd67;");
                
                // ⏱️ የሰዓት ቆጣሪ ጅምር (በየሰከንዱ ይጨምራል፣ በየ 5 ሰከንዱ +2 ኮይን ይሰጣል)
                secondsOnMic = 0;
                document.getElementById("mic-timer-badge").style.background = "rgba(0, 205, 99, 0.2)";
                micTimerInterval = setInterval(() => {{
                    secondsOnMic++;
                    let earnedCoins = Math.floor(secondsOnMic / 5) * 2;
                    document.getElementById("mic-timer-badge").innerText = `🎤 ማይክ ላይ፦ ${{secondsOnMic}} ሰከንድ (🪙 +${{earnedCoins}})`;
                    
                    if(secondsOnMic % 5 === 0) {{
                        myCoins += 2;
                        appendChat("🪙 ቦነስ", `🎁 መድረክ ላይ ስለቆዩ 2 ነፃ ኮይን ተሰጥቶዎታል!`, "color:#00cd63; font-size:11px;");
                    }}
                }}, 1000);
            }}

            function renderSeats() {{
                const container = document.getElementById("seats-container");
                container.innerHTML = "";
                for (let i = 1; i <= 3; i++) {{
                    let seat = seatsData[i];
                    let html = `<div class="seat-item">
                        <div class="seat-circle ${{seat.active?'':'empty'}}">${{seat.active?'🎤':'＋'}}</div>
                        <div class="seat-name">${{seat.name}}</div>
                    </div>`;
                    container.innerHTML += html;
                }}
            }}

            function exitRoom() {{
                // ⏱️ ሰዓት ቆጣሪ ማቆሚያ
                if(micTimerInterval) {{
                    clearInterval(micTimerInterval);
                    micTimerInterval = null;
                }}
                currentSeat = null;
                document.getElementById("mic-timer-badge").innerText = "🎤 መድረክ አልወጡም";
                document.getElementById("mic-timer-badge").style.background = "rgba(255,221,103,0.15)";
                
                document.getElementById("room-screen").style.display = "none";
                document.getElementById("main-nav-bar").style.display = "flex";
                document.getElementById("lobby-screen").style.display = "flex";
            }}

            function appendChat(user, msg, style="") {{
                const box = document.getElementById("chat-box");
                box.innerHTML += `<div style="${{style}}"><b>${{user}}:</b> ${{msg}}</div>`;
                box.scrollTop = box.scrollHeight;
            }}

            function sendTextMessage() {{
                const input = document.getElementById("text-msg-input");
                if(!input.value.trim()) return;
                appendChat(myUsername, input.value.trim());
                input.value = "";
            }}
            
            function openGiftTray() {{ document.getElementById("gift-modal-overlay").style.display = "flex"; }}
            function closeGiftTray() {{ document.getElementById("gift-modal-overlay").style.display = "none"; }}
        </script>
    </body>
    </html>
    """
    return html_content
