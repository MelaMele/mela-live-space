import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Mela Space - Ultimate 3D Live Video Masterpiece")

# 📱 ያንተ መረጃ
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
        <title>Mela Space - Live Video & Interactive Hub</title>
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
                width:100%; background: linear-gradient(180deg, #fe2c55, #d2143a); border: none; color: white; padding: 14px; border-radius: 14px; font-weight: bold; font-size: 16px; cursor: pointer; position: relative;
                box-shadow: 0 5px 0 #990b24, 0 8px 15px rgba(0,0,0,0.4), 0 0 15px rgba(254,44,85,0.3); transition: all 0.1s ease; transform: translateY(0);
            }}
            .btn-3d:active {{ transform: translateY(4px); box-shadow: 0 1px 0 #990b24, 0 2px 5px rgba(0,0,0,0.4); }}
            .btn-3d-green {{ background: linear-gradient(180deg, #00cd63, #009647); box-shadow: 0 5px 0 #00632f, 0 8px 15px rgba(0,0,0,0.4), 0 0 15px rgba(0,205,99,0.3); }}
            .btn-3d-green:active {{ box-shadow: 0 1px 0 #00632f, 0 2px 5px rgba(0,0,0,0.4); }}

            .room-list-title {{ font-size:15px; color:#888; margin-bottom:12px; font-weight:bold; z-index: 2; }}
            .room-item {{ background: rgba(22, 23, 34, 0.6); border:1px solid rgba(255,255,255,0.05); padding:15px; border-radius:16px; display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; cursor:pointer; transition: transform 0.2s; z-index: 2; }}
            
            /* 🗂️ የታብ ገፆች */
            .tab-screen {{ display:none; position:absolute; top:0; left:0; width:100%; height:calc(100% - 70px); background:#060713; z-index:400; padding:20px; overflow-y:auto; }}
            .page-title {{ font-size:24px; font-weight:800; color:#25f4ee; margin-bottom:20px; text-align:center; }}
            .info-card {{ background: rgba(22, 23, 34, 0.7); border:1px solid rgba(255,255,255,0.06); border-radius:20px; padding:20px; margin-bottom:15px; text-align:center; }}
            
            /* 🎙️ ዋናው የውስጥ የቪዲዮ ሩም */
            .app-container {{ display: none; position: relative; width: 100%; height: 100%; flex-direction: column; background: #060713; }}
            .top-bar {{ display: flex; justify-content: space-between; align-items: center; padding: 12px 20px; border-bottom: 1px solid rgba(255,255,255,0.05); z-index: 10; }}
            .live-tag {{ background: linear-gradient(45deg, #fe2c55, #ff0033); padding: 5px 12px; border-radius: 20px; font-weight: 800; font-size: 11px; }}
            .room-name-display {{ font-size:13px; font-weight:bold; color:#25f4ee; background:rgba(37,244,238,0.15); border: 1px solid rgba(37,244,238,0.2); padding:5px 12px; border-radius:20px; }}
            
            .time-reward-badge {{ font-size:11px; color:#ffdd67; background: rgba(255,221,103,0.1); padding: 4px 10px; border-radius: 10px; font-weight: bold; margin-top: 4px; display: none; text-shadow: 0 0 5px rgba(255,221,103,0.5); }}

            .stage-area {{ flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; padding: 8px; z-index: 5; overflow-y: auto; }}
            
            /* 📺 Video Grid Layout (Zoom / TikTok Style) */
            .video-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; width: 100%; max-width: 380px; margin-bottom: 10px; }}
            .video-tile {{ width: 100%; height: 120px; background: #161722; border: 2px solid rgba(37,244,238,0.3); border-radius: 14px; overflow: hidden; position: relative; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }}
            .video-tile.empty {{ border: 1px dashed rgba(255,255,255,0.1); background: rgba(255,255,255,0.01); }}
            .video-placeholder {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 24px; color: #444; }}
            .video-label {{ position: absolute; bottom: 6px; left: 8px; background: rgba(0,0,0,0.6); padding: 2px 8px; border-radius: 6px; font-size: 11px; color: #fff; max-width: 85%; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}

            /* 🎛️ Control Panel Buttons with 3D Micro-style */
            .utility-bar {{ display: flex; flex-direction: column; gap: 8px; width: 100%; background: rgba(255,255,255,0.02); padding: 10px; border-top: 1px solid rgba(255,255,255,0.05); border-bottom: 1px solid rgba(255,255,255,0.05); z-index: 10; }}
            .button-row {{ display: flex; justify-content: space-around; width: 100%; gap: 6px; flex-wrap: wrap; }}
            
            .btn-3d-sm {{
                background: linear-gradient(180deg, rgba(255,255,255,0.1), rgba(255,255,255,0.03)); border: 1px solid rgba(255,255,255,0.12);
                color: white; padding: 7px 10px; border-radius: 10px; font-size: 11px; font-weight: bold; cursor: pointer;
                box-shadow: 0 3px 0 rgba(0,0,0,0.3); transition: all 0.1s; text-align: center; flex: 1; min-width: 72px;
            }}
            .btn-3d-sm:active {{ transform: translateY(2px); box-shadow: 0 1px 0 rgba(0,0,0,0.3); }}

            .slider-fx-container {{ display: flex; flex-direction: column; gap: 6px; width: 95%; margin: 0 auto; }}
            .volume-control-box {{ display: flex; align-items: center; justify-content: center; gap: 10px; font-size: 11px; color: #aaa; }}
            .volume-slider {{ flex: 1; -webkit-appearance: none; background: rgba(255,255,255,0.1); height: 5px; border-radius: 3px; outline: none; }}
            .volume-slider::-webkit-slider-thumb {{ -webkit-appearance: none; appearance: none; width: 14px; height: 14px; border-radius: 50%; background: #25f4ee; cursor: pointer; }}
            
            .fx-box {{ display: flex; justify-content: space-between; gap: 5px; align-items: center; font-size: 11px; color: #888; }}
            .fx-select {{ background: #161722; border: 1px solid rgba(255,255,255,0.1); color: white; border-radius: 8px; padding: 3px 6px; font-size: 11px; outline: none; }}

            /* 💬 የላይቭ ቻት ክልል */
            .chat-area {{ height: 110px; width: 100%; padding: 10px; background: linear-gradient(transparent, rgba(6,7,19,0.98)); overflow-y: auto; font-size: 12px; display: flex; flex-direction: column; gap: 5px; z-index: 10; scroll-behavior: smooth; }}
            
            /* ✍️ የፅሁፍ መፃፊያ ባር */
            .chat-input-container {{ display: flex; padding: 10px 15px; background: #0b0c1e; border-top: 1px solid rgba(255,255,255,0.05); z-index: 12; gap: 10px; align-items: center; }}
            .chat-input {{ flex: 1; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 10px 15px; color: #fff; font-size: 13px; outline: none; }}
            .btn-send-text {{ background: #25f4ee; border: none; color: #060713; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; cursor: pointer; box-shadow: 0 3px 0 #1bcfca; transition: all 0.1s; }}
            .btn-send-text:active {{ transform: translateY(2px); box-shadow: 0 1px 0 #1bcfca; }}

            .bottom-controls {{ display: flex; justify-content: space-between; align-items: center; padding: 10px 20px; background: #060713; z-index: 10; border-top: 1px solid rgba(255,255,255,0.05); }}
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
                <div class="nav-icon">📹</div>
                <div>ቪዲዮ ክፍሎች</div>
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
            <div class="lobby-header"><div class="lobby-title">Mela Live Video Rooms</div></div>

            <div class="create-room-box">
                <input type="text" id="lobby-username" class="input-field" placeholder="የእርስዎን ስም ያስገቡ...">
                <input type="text" id="lobby-roomname" class="input-field" placeholder="የቪዲዮ ክፍሉን ስም ያስገቡ...">
                <div class="checkbox-container">
                    <input type="checkbox" id="lobby-is-vip">
                    <label for="lobby-is-vip">🔒 እንደ VIP (የግል ሚስጥራዊ ክፍል) ፍጠር</label>
                </div>
                <button class="btn-3d" style="margin-bottom:12px;" onclick="createNewRoomAction()">📹 አዲስ የቪዲዮ ክፍል ጀምር</button>
                <button class="btn-3d btn-3d-green" onclick="openWheelModal()">🎡 ዕለታዊ ዕድል ማሽከርከሪያ</button>
            </div>

            <div class="room-list-title">🟢 የቀጥታ ቪዲዮ ስርጭቶች</div>
            <div id="active-rooms-list">
                <div class="room-item" onclick="joinExistingRoom('🌍 የስደት ወግ (Diaspora Lounge)')">
                    <div>
                        <div style="font-weight:bold; color:#ffdd67; font-size:15px;">🌍 የስደት ወግ (Diaspora Video Lounge) ⭐</div>
                        <div style="font-size:12px; color:#aaa; margin-top:3px;">በአረብ ሀገር ያሉ እህት ወንድሞች የቪዲዮ ስርጭት መድረክ</div>
                    </div>
                    <div style="color:#25f4ee; font-size:12px; font-weight:bold; background:rgba(37,244,238,0.1); padding:6px 12px; border-radius:12px;">📹 ግባ</div>
                </div>
                <div class="room-item" onclick="joinExistingRoom('⚽ የኳስ ሜዳ (Football Fan Zone)')">
                    <div>
                        <div style="font-weight:bold; color:#00ff7f; font-size:15px;">⚽ የኳስ ሜዳ (Football Live Streaming) 🔥</div>
                        <div style="font-size:12px; color:#aaa; margin-top:3px;">የእግር ኳስ ጨዋታዎች በቪዲዮ ትንታኔና የደጋፊዎች ሙቅ ክርክር</div>
                    </div>
                    <div style="color:#25f4ee; font-size:12px; font-weight:bold; background:rgba(37,244,238,0.1); padding:6px 12px; border-radius:12px;">📹 ግባ</div>
                </div>
            </div>
        </div>

        <div class="tab-screen" id="wallet-screen">
            <div class="page-title">My Mela Wallet</div>
            <div class="info-card">
                <div style="font-size:14px; color:#888;">የአሁኑ የኮይን ባላንስዎ</div>
                <div style="font-size:38px; font-weight:900; color:#00cd63; margin:10px 0;">🪙 <span id="wallet-coin-balance">350</span></div>
            </div>
            <button class="btn-3d btn-3d-green" onclick="alert('የአውቶማቲክ ቴሌብር ሲስተም በቅርቡ ይበራል!')">💳 በቴሌብር ኮይን ግዛ</button>
        </div>

        <div class="tab-screen" id="referral-screen">
            <div class="page-title">ጋብዘው ይክበሩ (Refer & Earn)</div>
            <div class="info-card">
                <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px; font-size:11px; color:#25f4ee;" id="ref-link-text">
                    https://t.me/MelaSpaceBot?start=ref_{ADMIN_CHAT_ID}
                </div>
            </div>
            <button class="btn-3d" onclick="copyRefLink()">📋 ሊንኩን ኮፒ አድርግ</button>
        </div>

        <div class="app-container" id="room-screen">
            <div class="top-bar">
                <div class="live-tag" id="room-badge-type">🔴 LIVE VIDEO</div>
                <div class="room-name-display" id="active-room-title">ክፍል: ---</div>
                <div style="font-size:13px; color:#fe2c55; cursor:pointer; font-weight:bold;" onclick="exitRoom()">🚪 ውጣ</div>
            </div>
            
            <div class="stage-area">
                <div class="time-reward-badge" id="mic-timer-badge">📹 መድረክ ላይ፦ 0 ሰከንድ (🪙 +0)</div>
                <div style="height:5px;"></div>
                
                <div class="video-grid" id="video-tiles-grid">
                    <div class="video-tile empty" id="v-tile-1"><div class="video-placeholder">👤</div><div class="video-label" id="v-label-1">መቀመጫ 1 (ባዶ)</div></div>
                    <div class="video-tile empty" id="v-tile-2"><div class="video-placeholder">👤</div><div class="video-label" id="v-label-2">መቀመጫ 2 (ባዶ)</div></div>
                    <div class="video-tile empty" id="v-tile-3"><div class="video-placeholder">👤</div><div class="video-label" id="v-label-3">መቀመጫ 3 (ባዶ)</div></div>
                    <div class="video-tile empty" id="v-tile-4"><div class="video-placeholder">👤</div><div class="video-label" id="v-label-4">መቀመጫ 4 (ባዶ)</div></div>
                </div>
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
                </div>
            </div>

            <div class="chat-area" id="chat-box"></div>

            <div class="chat-input-container">
                <input type="text" id="text-msg-input" class="chat-input" placeholder="ለሹክሹክታ /w @username መልእክት ወይም መደበኛ ፅሁፍ...">
                <button class="btn-send-text" onclick="sendTextMessage()">➔</button>
            </div>
            
            <div class="bottom-controls">
                <button class="btn-3d" style="max-width:140px; padding:10px;" onclick="requestVideoSeatAuto()">📹 ካሜራ አብራ / ግባ</button>
                <div style="display:flex; align-items:center;">
                    <button class="btn-3d btn-3d-green" style="max-width:100px; padding:10px; margin-right:10px;" onclick="openGiftTray()">🎁 ስጦታ</button>
                    <div class="nav-icon" style="background: rgba(255,255,255,0.06); width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; cursor: pointer;" id="mic-toggle-btn" onclick="toggleMic()">🔊</div>
                </div>
            </div>
        </div>

        <div class="gift-overlay" id="gift-modal-overlay" onclick="closeGiftTray()">
            <div class="gift-tray" id="gift-tray-zone" onclick="event.stopPropagation()">
                <div class="gift-card" onclick="processGiftSend('🌹 ጽጌረዳ', 10, '🌹')"><div class="gift-emoji">🌹</div></div>
                <div class="gift-card" onclick="processGiftSend('☕ የጀበና ቡና', 50, '☕')"><div class="gift-emoji">☕</div></div>
                <div class="gift-card" onclick="processGiftSend('👑 የMela አክሊል', 500, '👑')"><div class="gift-emoji">👑</div></div>
            </div>
            <div class="wheel-box" id="wheel-zone" style="display:none;" onclick="event.stopPropagation()">
                <h3>🎡 ዕለታዊ የዕድል ማሽከርከሪያ</h3>
                <div class="wheel-graphic" id="wheel-element">🎁</div>
                <button class="btn-3d btn-3d-green" onclick="spinTheWheelAction()">🎰 አሽከርክር</button>
            </div>
        </div>

        <div class="cinematic-stage" id="animation-stage-layer"><div class="big-gift-anim" id="big-gift-emoji-element">👑</div></div>

        <script>
            const AGORA_APP_ID = "ea7dfdf9926d400fb8a54d31be0bd44c"; 
            let client = AgoraRTC.createClient({{ mode: "rtc", codec: "vp8" }});
            let localTracks = {{ audioTrack: null, videoTrack: null }};
            let currentSeat = null; let myUsername = "እንግዳ"; let currentRoomName = ""; let myCoins = 350;
            
            // ⏱️ የላቁ ስልቶች መከታተያ ቫሪያብልስ
            let micTimerInterval = null; let secondsOnMic = 0;
            let lastGiftTime = 0; let giftComboCount = 0;

            let seatsData = {{ 1:{{name:"ባዶ",active:false}}, 2:{{name:"ባዶ",active:false}}, 3:{{name:"ባዶ",active:false}}, 4:{{name:"ባዶ",active:false}} }};

            function switchTab(tabName) {{
                document.getElementById("lobby-screen").style.display = "none";
                document.getElementById("wallet-screen").style.display = "none";
                document.getElementById("referral-screen").style.display = "none";
                if(tabName === 'home') document.getElementById("lobby-screen").style.display = "flex";
                else if(tabName === 'wallet') {{ document.getElementById("wallet-screen").style.display = "block"; document.getElementById("wallet-coin-balance").innerText = myCoins; }}
                else if(tabName === 'referral') document.getElementById("referral-screen").style.display = "block";
            }}

            function createNewRoomAction() {{
                const uName = document.getElementById("lobby-username").value.trim();
                const rName = document.getElementById("lobby-roomname").value.trim();
                if(!uName || !rName) {{ alert("እባክዎ መረጃዎችን በትክክል ያስገቡ!"); return; }}
                myUsername = uName; currentRoomName = rName;
                sendBotNotification(`🚨 አዲስ የቪዲዮ ውይይት አዳራሽ ተከፈተ!\\n📹 ክፍል፦ ${{currentRoomName}}\\n👤 ፈጣሪ፦ ${{myUsername}}`);
                launchRoom();
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
                document.getElementById("chat-box").innerHTML = "";

                const audio = document.getElementById("bg-kirar-audio");
                audio.volume = 0.15; audio.play().catch(e => console.log("Audio playing."));

                appendChat("🚀 Mela System", ` ወደ የቪዲዮ የቀጥታ ስርጭት ክፍል በሰላም መጡ!`, "color:#25f4ee; font-weight:bold;");
                initAgora(currentRoomName);
            }}

            // 🤫 የሹክሹክታ (Secret Whisper) እና መደበኛ ፅሁፍ ሲስተም
            function sendTextMessage() {{
                const inputEl = document.getElementById("text-msg-input");
                const msgText = inputEl.value.trim();
                if(!msgText) return;
                
                if(msgText.startsWith("/w ")) {{
                    const parts = msgText.split(" ");
                    if(parts.length >= 3 && parts[1].startsWith("@")) {{
                        const targetUser = parts[1].replace("@", "");
                        const secretMsg = parts.slice(2).join(" ");
                        appendChat("🤫 ሹክሹክታ ለ [" + targetUser + "]", secretMsg, "color: #ffaa00; background: rgba(255,170,0,0.08); padding: 5px 10px; border-radius: 8px; border-left: 3px solid #ffaa00;");
                        inputEl.value = ""; return;
                    }}
                }}

                appendChat(myUsername, msgText, "color: #fff; background: rgba(255,255,255,0.02); padding: 5px 10px; border-radius: 8px;");
                inputEl.value = "";
            }}

            function appendChat(user, msg, style = "") {{
                const box = document.getElementById("chat-box");
                const div = document.createElement("div"); div.style = style;
                div.innerHTML = `<b>${{user}}:</b> ${{msg}}`; box.appendChild(div);
                box.scrollTop = box.scrollHeight;
            }}

            // ⏱️ የ"አየር ሰዓት" ኮይን መቁጠሪያ (Voice/Video-Time Reward)
            function startMicTimer() {{
                secondsOnMic = 0;
                const badge = document.getElementById("mic-timer-badge");
                badge.style.display = "inline-block";
                
                micTimerInterval = setInterval(() => {{
                    secondsOnMic++;
                    if(secondsOnMic % 60 === 0) {{
                        myCoins += 5; // በቪዲዮ መድረክ ላይ ለቆየ 1 ደቂቃ 5 ኮይን ሽልማት
                        appendChat("🎁 የቪዲዮ ሽልማት", ` 🎉 መድረክ ላይ 1 ደቂቃ በመቆየትዎ 5 ነፃ ኮይን አግኝተዋል!`, "color:#ffdd67; font-weight:bold;");
                    }}
                    badge.innerText = `📹 መድረክ ላይ፦ ${{secondsOnMic}} ሰከንድ (🪙 +${{Math.floor(secondsOnMic/60) * 5}})`;
                }}, 1000);
            }}

            function stopMicTimer() {{
                if(micTimerInterval) {{ clearInterval(micTimerInterval); micTimerInterval = null; }}
                document.getElementById("mic-timer-badge").style.display = "none";
            }}

            // 🎁 የስጦታ "ማዕበል" (Gift Multiplier / Combo) ሎጂክ
            function processGiftSend(giftName, price, emoji) {{
                if (myCoins < price) {{ alert(`ይቅርታ! ባላንስዎ በቂ አይደለም።`); closeGiftTray(); return; }}
                myCoins -= price; closeGiftTray();
                
                let now = Date.now();
                if (now - lastGiftTime <= 10000) {{ giftComboCount++; }} 
                else {{ giftComboCount = 1; }}
                lastGiftTime = now;

                let multiplier = 1;
                if (giftComboCount >= 10) multiplier = 10;
                else if (giftComboCount >= 5) multiplier = 5;
                else if (giftComboCount >= 3) multiplier = 2;

                const stage = document.getElementById("animation-stage-layer");
                document.getElementById("big-gift-emoji-element").innerText = emoji;
                stage.style.display = "flex"; setTimeout(() => {{ stage.style.display = "none"; }}, 1500);

                if (multiplier > 1) {{
                    appendChat("🔥 GIFT COMBO x" + giftComboCount, ` ${{myUsername}} የስጦታ ማዕበል አቀጣጠለ! ${{giftName}} (ነጥብ በ x${{multiplier}} ተባዝቷል!)`, "color:#fe2c55; font-weight:bold;");
                }} else {{
                    appendChat("🎁 GIFT", `${{myUsername}} ለክፍሉ ${{giftName}} ${{emoji}} አበርክተዋል!`, "color:#ff5574; font-weight:bold;");
                }}
            }}

            async function initAgora(channelName) {{
                try {{
                    await client.join(AGORA_APP_ID, channelName, null, null);
                    client.on("user-published", async (user, mediaType) => {{
                        await client.subscribe(user, mediaType);
                        if (mediaType === "video") {{
                            let remoteVideoTrack = user.videoTrack;
                            for (let i = 1; i <= 4; i++) {{
                                if (!seatsData[i].active) {{
                                    seatsData[i] = {{ name: "ተጠቃሚ " + user.uid, active: true }};
                                    let tile = document.getElementById(`v-tile-${{i}}`);
                                    tile.classList.remove("empty"); tile.innerHTML = "";
                                    remoteVideoTrack.play(tile);
                                    document.getElementById(`v-label-${{i}}`).innerText = "ተጠቃሚ " + user.uid;
                                    break;
                                }}
                            }}
                        }}
                        if (mediaType === "audio") user.audioTrack.play();
                    }});
                }} catch(e) {{ console.log(e); }}
            }}

            async function claimVideoSeat(seatId) {{
                if (seatsData[seatId].active) return;
                if (currentSeat) {{ stopMicTimer(); }}
                currentSeat = seatId; seatsData[seatId] = {{ name: myUsername, active: true }};
                
                let tile = document.getElementById(`v-tile-${{seatId}}`);
                tile.classList.remove("empty"); tile.innerHTML = "";
                document.getElementById(`v-label-${{seatId}}`).innerText = myUsername;

                startMicTimer();

                try {{
                    await client.setClientRole("host");
                    localTracks.audioTrack = await AgoraRTC.createMicrophoneAudioTrack();
                    localTracks.videoTrack = await AgoraRTC.createCameraTrack();
                    
                    localTracks.videoTrack.play(tile);
                    await client.publish([localTracks.audioTrack, localTracks.videoTrack]);
                }} catch (err) {{ console.error(err); }}
            }}

            function requestVideoSeatAuto() {{
                for (let i = 1; i <= 4; i++) {{ if (!seatsData[i].active) {{ claimVideoSeat(i); break; }} }}
            }}

            async function toggleMic() {{
                if (localTracks.audioTrack) {{
                    if (localTracks.audioTrack.muted) {{ await localTracks.audioTrack.setMuted(false); document.getElementById("mic-toggle-btn").innerText = "🔊"; }}
                    else {{ await localTracks.audioTrack.setMuted(true); document.getElementById("mic-toggle-btn").innerText = "🔇"; }}
                }}
            }}

            async function exitRoom() {{
                document.getElementById("bg-kirar-audio").pause();
                if(localTracks.audioTrack) {{ localTracks.audioTrack.stop(); localTracks.audioTrack.close(); }}
                if(localTracks.videoTrack) {{ localTracks.videoTrack.stop(); localTracks.videoTrack.close(); }}
                stopMicTimer(); await client.leave(); currentSeat = null;
                document.getElementById("room-screen").style.display = "none";
                document.getElementById("main-nav-bar").style.display = "flex";
                switchTab('home');
            }}

            function sendBotNotification(text) {{
                const token = "{TELEGRAM_BOT_TOKEN}"; const chat_id = "{ADMIN_CHAT_ID}";
                fetch(`https://api.telegram.org/bot${{token}}/sendMessage?chat_id=${{chat_id}}&text=${{encodeURIComponent(text)}}`).catch(e => console.log(e));
            }}
            function openGiftTray() {{ document.getElementById("gift-modal-overlay").style.display = "flex"; document.getElementById("gift-tray-zone").style.display = "grid"; document.getElementById("wheel-zone").style.display = "none"; }}
            function closeGiftTray() {{ document.getElementById("gift-modal-overlay").style.display = "none"; }}
            function openWheelModal() {{ document.getElementById("gift-modal-overlay").style.display = "flex"; document.getElementById("gift-tray-zone").style.display = "none"; document.getElementById("wheel-zone").style.display = "block"; }}
            function startBingoGame() {{ appendChat("🎲 BINGO", ` አዲስ ጨዋታ ተጀምሯል!`, "color:#00ff7f; font-weight:bold;"); }}
            function runLuckyDraw() {{ appendChat("🎰 ሎተሪ", `እጣው እየወጣ ነው...`, "color:#ffdd67;"); }}
            function adjustMusicVolume(v) {{ document.getElementById("bg-kirar-audio").volume = v / 100; }}
            function playRealSound(t) {{ document.getElementById(t === 'applause' ? 'snd-applause' : 'snd-laughter').play().catch(e=>v=0); }}
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
