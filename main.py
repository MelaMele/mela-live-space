import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Mela Space - Ultimate Live Hub")

MY_TELEBIRR_NUMBER = "0913064239"  
MY_NAME = "Melaku Mebrate"         
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
        <title>Mela Space - Live Streaming & Interactive Hub</title>
        <script src="https://download.agora.io/sdk/release/AgoraRTC_N-4.18.0.js"></script>
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Roboto, sans-serif; }}
            body, html {{ width: 100%; height: 100%; overflow: hidden; background: #060713; color: #fff; }}
            
            .bg-glow {{ position: absolute; width: 300px; height: 300px; background: radial-gradient(circle, rgba(37,244,238,0.15) 0%, rgba(0,0,0,0) 70%); top: -50px; left: -50px; z-index: 1; pointer-events: none; }}
            .bg-glow-right {{ position: absolute; width: 300px; height: 300px; background: radial-gradient(circle, rgba(254,44,85,0.12) 0%, rgba(0,0,0,0) 70%); bottom: 50px; right: -50px; z-index: 1; pointer-events: none; }}

            /* 🚪 ሎቢ ገጽ */
            .lobby-container {{ position: absolute; top:0; left:0; width:100%; height:calc(100% - 70px); background:#060713; z-index:500; display:flex; flex-direction:column; padding:20px; overflow-y:auto; }}
            .lobby-title {{ text-align:center; color:#25f4ee; font-size:26px; font-weight:900; text-shadow: 0 0 20px rgba(37,244,238,0.6); margin-bottom: 20px; }}
            
            .create-room-box {{ background: rgba(22, 23, 34, 0.7); backdrop-filter: blur(10px); border:1px solid rgba(255,255,255,0.07); border-radius:20px; padding:20px; margin-bottom:20px; }}
            .input-field {{ width:100%; background: rgba(47, 48, 61, 0.6); border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:12px; color:white; font-size:14px; margin-bottom:12px; outline:none; }}
            
            .btn-3d {{ 
                width:100%; background: linear-gradient(180deg, #fe2c55, #d2143a); border: none; color: white; padding: 14px; border-radius: 14px; font-weight: bold; font-size: 16px; cursor: pointer; position: relative;
                box-shadow: 0 5px 0 #990b24, 0 8px 15px rgba(0,0,0,0.4); transition: all 0.1s ease;
            }}
            .btn-3d:active {{ transform: translateY(4px); box-shadow: 0 1px 0 #990b24; }}
            .btn-3d-green {{ background: linear-gradient(180deg, #00cd63, #009647); box-shadow: 0 5px 0 #00632f; }}
            .btn-3d-green:active {{ box-shadow: 0 1px 0 #00632f; }}

            .room-list-title {{ font-size:15px; color:#888; margin-bottom:12px; font-weight:bold; }}
            .room-item {{ background: rgba(22, 23, 34, 0.6); border:1px solid rgba(255,255,255,0.05); padding:15px; border-radius:16px; display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; cursor:pointer; }}
            
            /* 🗂️ የታብ ገፆች */
            .tab-screen {{ display:none; position:absolute; top:0; left:0; width:100%; height:calc(100% - 70px); background:#060713; z-index:400; padding:20px; overflow-y:auto; }}
            .page-title {{ font-size:24px; font-weight:800; color:#25f4ee; margin-bottom:20px; text-align:center; }}
            .info-card {{ background: rgba(22, 23, 34, 0.7); border:1px solid rgba(255,255,255,0.06); border-radius:20px; padding:20px; margin-bottom:15px; text-align:center; }}
            
            /* 🎙️ ዋናው የውስጥ የቪዲዮ ሩም */
            .app-container {{ display: none; position: relative; width: 100%; height: 100%; flex-direction: column; background: #060713; }}
            .top-bar {{ display: flex; justify-content: space-between; align-items: center; padding: 12px 20px; border-bottom: 1px solid rgba(255,255,255,0.05); z-index: 10; }}
            .live-tag {{ background: linear-gradient(45deg, #fe2c55, #ff0033); padding: 5px 12px; border-radius: 20px; font-weight: 800; font-size: 11px; }}
            
            .time-reward-badge {{ font-size:11px; color:#ffdd67; background: rgba(255,221,103,0.1); padding: 4px 10px; border-radius: 10px; font-weight: bold; margin-top: 4px; display: none; }}

            .stage-area {{ flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; padding: 8px; z-index: 5; overflow-y: auto; }}
            
            /* 📺 Video/Audio Grid Layout */
            .video-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; width: 100%; max-width: 380px; margin-bottom: 10px; }}
            .video-tile {{ width: 100%; height: 120px; background: #161722; border: 2px solid rgba(37,244,238,0.3); border-radius: 14px; overflow: hidden; position: relative; display: flex; align-items: center; justify-content: center; }}
            .video-tile.empty {{ border: 1px dashed rgba(255,255,255,0.1); background: rgba(255,255,255,0.01); }}
            
            /* 👤 Avatar & 🌊 Wave Animation Style */
            .avatar-container {{ position: relative; width: 60px; height: 60px; border-radius: 50%; background: #2f303d; display: flex; align-items: center; justify-content: center; font-size: 28px; z-index: 2; }}
            .audio-wave {{ position: absolute; width: 60px; height: 60px; border-radius: 50%; border: 2px solid #25f4ee; opacity: 0; animation: none; z-index: 1; }}
            
            @keyframes waveExpand {{
                0% {{ transform: scale(1); opacity: 0.8; }}
                100% {{ transform: scale(1.5); opacity: 0; }}
            }}

            .host-badge {{ position: absolute; top: 6px; right: 6px; background: #ffdd67; color: #000; padding: 2px 6px; border-radius: 6px; font-size: 9px; font-weight: bold; z-index: 5; }}
            .video-label {{ position: absolute; bottom: 6px; left: 8px; background: rgba(0,0,0,0.6); padding: 2px 8px; border-radius: 6px; font-size: 11px; color: #fff; z-index: 5; }}

            /* 🎛️ Utility Bar & Controls */
            .utility-bar {{ display: flex; flex-direction: column; gap: 8px; width: 100%; background: rgba(255,255,255,0.02); padding: 10px; border-top: 1px solid rgba(255,255,255,0.05); z-index: 10; }}
            .button-row {{ display: flex; justify-content: space-around; width: 100%; gap: 6px; }}
            
            .btn-3d-sm {{
                background: linear-gradient(180deg, rgba(255,255,255,0.1), rgba(255,255,255,0.03)); border: 1px solid rgba(255,255,255,0.12);
                color: white; padding: 7px 10px; border-radius: 10px; font-size: 11px; font-weight: bold; cursor: pointer; flex: 1; text-align: center;
            }}
            .btn-3d-sm:active {{ transform: translateY(2px); }}

            .volume-control-box {{ display: flex; align-items: center; justify-content: center; gap: 10px; font-size: 11px; color: #aaa; width: 95%; margin: 0 auto; }}
            .volume-slider {{ flex: 1; -webkit-appearance: none; background: rgba(255,255,255,0.1); height: 5px; border-radius: 3px; }}
            .volume-slider::-webkit-slider-thumb {{ -webkit-appearance: none; width: 14px; height: 14px; border-radius: 50%; background: #25f4ee; }}
            
            .fx-select {{ background: #161722; border: 1px solid rgba(255,255,255,0.1); color: white; border-radius: 8px; padding: 3px 6px; font-size: 11px; outline: none; }}

            /* 💬 ቻት ክልል */
            .chat-area {{ height: 110px; width: 100%; padding: 10px; background: linear-gradient(transparent, rgba(6,7,19,0.98)); overflow-y: auto; font-size: 12px; display: flex; flex-direction: column; gap: 5px; z-index: 10; }}
            .chat-input-container {{ display: flex; padding: 10px 15px; background: #0b0c1e; border-top: 1px solid rgba(255,255,255,0.05); z-index: 12; gap: 10px; }}
            .chat-input {{ flex: 1; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 10px 15px; color: #fff; font-size: 13px; outline: none; }}
            .btn-send-text {{ background: #25f4ee; border: none; color: #060713; width: 36px; height: 36px; border-radius: 50%; font-weight: bold; cursor: pointer; }}

            .bottom-controls {{ display: flex; justify-content: space-between; align-items: center; padding: 10px 20px; background: #060713; z-index: 10; }}
            .bottom-nav {{ position:absolute; bottom:0; left:0; width:100%; height:70px; background: rgba(22, 23, 34, 0.85); backdrop-filter: blur(15px); border-top:1px solid rgba(255,255,255,0.06); display:flex; justify-content:space-around; align-items:center; z-index:1000; }}
            .nav-item {{ display:flex; flex-direction:column; align-items:center; color:#666b86; font-size:11px; font-weight:600; cursor:pointer; }}
            .nav-item.active {{ color:#25f4ee; }}
            .nav-icon {{ font-size:22px; margin-bottom:4px; }}

            /* Overlays */
            .gift-overlay {{ display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.7); z-index:2000; align-items:flex-end; }}
            .gift-tray {{ width:100%; background:#10111e; border-top: 2px solid rgba(255,255,255,0.1); border-radius:24px 24px 0 0; padding:20px; display:grid; grid-template-columns: repeat(4, 1fr); gap:12px; }}
            .gift-card {{ background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05); border-radius:16px; padding:12px 5px; text-align:center; }}

            /* 🎡 Wheel UI */
            .wheel-box {{ width: 100%; background: #10111e; padding: 25px; border-radius: 24px 24px 0 0; text-align: center; display:none; }}
            .wheel-graphic {{ width: 150px; height: 150px; border-radius: 50%; border: 6px solid #25f4ee; margin: 15px auto; display: flex; align-items: center; justify-content: center; font-size: 40px; font-weight: bold; background: conic-gradient(#fe2c55 0% 25%, #00ff7f 25% 50%, #00bfff 50% 75%, #ffdd67 75% 100%); transition: transform 3s cubic-bezier(0.1, 0.8, 0.1, 1); }}

            .cinematic-stage {{ display:none; position:fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:2500; align-items:center; justify-content:center; }}
            .big-gift-anim {{ font-size:120px; animation: cinematicBlast 1.5s forwards ease-in-out; }}
            @keyframes cinematicBlast {{
                0% {{ transform: scale(0); opacity: 0; }}
                50% {{ transform: scale(1.2); opacity: 1; }}
                100% {{ opacity: 0; transform: scale(0.7) translateY(-100px); }}
            }}
        </style>
    </head>
    <body>

        <div class="bg-glow"></div>
        <div class="bg-glow-right"></div>

        <!-- 🎵 ኦዲዮ ማጫወቻዎች -->
        <audio id="bg-kirar-audio" loop crossOrigin="anonymous">
            <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mp3">
        </audio>
        <audio id="snd-applause" crossOrigin="anonymous">
            <source src="https://www.soundjay.com/human/sounds/applause-01.mp3" type="audio/mp3">
        </audio>
        <audio id="snd-laughter" crossOrigin="anonymous">
            <source src="https://www.soundjay.com/human/sounds/laughter-01.mp3" type="audio/mp3">
        </audio>

        <!-- 🧭 የታችኛው ሜኑ ባር -->
        <div class="bottom-nav" id="main-nav-bar">
            <div class="nav-item active" id="nav-home" onclick="switchTab('home')">
                <div class="nav-icon">📹</div>
                <div>የውይይት ክፍሎች</div>
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

        <!-- 🚪 1. ሎቢ ገጽ (ሁሉም የድሮ ሩሞች ተመልሰዋል) -->
        <div class="lobby-container" id="lobby-screen">
            <div class="lobby-title">Mela Live Rooms</div>

            <div class="create-room-box">
                <input type="text" id="lobby-username" class="input-field" placeholder="የእርስዎን ስም ያስገቡ...">
                <input type="text" id="lobby-roomname" class="input-field" placeholder="አዲስ የክፍል ስም ያስገቡ...">
                <button class="btn-3d" style="margin-bottom:12px;" onclick="createNewRoomAction()">🎙️ አዲስ የውይይት ክፍል ጀምር</button>
                <button class="btn-3d btn-3d-green" onclick="openWheelModal()">🎡 ዕለታዊ ዕድል ማሽከርከሪያ</button>
            </div>

            <div class="room-list-title">🟢 ንቁ የውይይት አዳራሾች</div>
            <div id="active-rooms-list">
                <div class="room-item" onclick="joinExistingRoom('🌍 የስደት ወግ (Diaspora Lounge)')">
                    <div>
                        <div style="font-weight:bold; color:#ffdd67; font-size:15px;">🌍 የስደት ወግ (Diaspora Lounge) ⭐</div>
                        <div style="font-size:12px; color:#aaa; margin-top:3px;">በስደት ያሉ ወገኖች የመገናኛ መድረክ</div>
                    </div>
                    <div style="color:#25f4ee; font-size:12px; font-weight:bold;">ግቡ ➡️</div>
                </div>
                <div class="room-item" onclick="joinExistingRoom('👩‍👧‍👦 የእናቶች ወግ (Mothers Circle)')">
                    <div>
                        <div style="font-weight:bold; color:#fe2c55; font-size:15px;">👩‍👧‍👦 የእናቶች ወግ (Mothers Circle) ❤️</div>
                        <div style="font-size:12px; color:#aaa; margin-top:3px;">የእናቶች የምክክር እና የልጅ አስተዳደግ ወግ</div>
                    </div>
                    <div style="color:#25f4ee; font-size:12px; font-weight:bold;">ግቡ ➡️</div>
                </div>
                <div class="room-item" onclick="joinExistingRoom('📚 የተማሪዎች ውይይት (Students Hub)')">
                    <div>
                        <div style="font-weight:bold; color:#00ff7f; font-size:15px;">📚 የተማሪዎች ውይይት (Students Hub) 🎓</div>
                        <div style="font-size:12px; color:#aaa; margin-top:3px;">የትምህርት፣ የዩኒቨርሲቲ ህይወት እና የፈተና ምክክሮች</div>
                    </div>
                    <div style="color:#25f4ee; font-size:12px; font-weight:bold;">ግቡ ➡️</div>
                </div>
                <div class="room-item" onclick="joinExistingRoom('⚽ የኳስ ሜዳ (Football Fan Zone)')">
                    <div>
                        <div style="font-weight:bold; color:#00bfff; font-size:15px;">⚽ የኳስ ሜዳ (Football Fan Zone) 🔥</div>
                        <div style="font-size:12px; color:#aaa; margin-top:3px;">የኳስ ጨዋታዎች ትንታኔ እና የደጋፊዎች ሙቅ ክርክር</div>
                    </div>
                    <div style="color:#25f4ee; font-size:12px; font-weight:bold;">ግቡ ➡️</div>
                </div>
            </div>
        </div>

        <!-- 👛 2. የዋሌት ገጽ (የተመለሰ) -->
        <div class="tab-screen" id="wallet-screen">
            <div class="page-title">የእኔ መላ ዋሌት (Mela Wallet)</div>
            <div class="info-card">
                <div style="font-size:14px; color:#888;">ያሉዎት ጠቅላላ የኮይን መጠን</div>
                <div style="font-size:38px; font-weight:900; color:#00cd63; margin:10px 0;">🪙 <span id="wallet-coin-balance">350</span></div>
                <div style="font-size:12px; color:#aaa;">የአየር ሰዓት በመቆየት ወይም በሽልማት ያገኙት ኮይን</div>
            </div>
            <div class="info-card" style="text-align: left;">
                <h4 style="color:#ffdd67; margin-bottom:10px;">💳 በቴሌብር (Telebirr) ኮይን መግዣ</h4>
                <p style="font-size:13px; color:#ccc; margin-bottom:5px;">ደረጃ 1፡ ወደ ስልክ ቁጥር <b>{MY_TELEBIRR_NUMBER}</b> ({MY_NAME}) መላክ የሚፈልጉትን ብር ይላኩ።</p>
                <p style="font-size:13px; color:#ccc;">ደረጃ 2፡ የላኩበትን የግብይት ማረጋገጫ (Transaction SMS) ለቦቱ ይላኩ። (1 ብር = 2 ኮይን)</p>
            </div>
        </div>

        <!-- 🔗 3. የሪፈራል ገጽ (የተመለሰ) -->
        <div class="tab-screen" id="referral-screen">
            <div class="page-title">ጋብዘው ይክበሩ (Referral Link)</div>
            <div class="info-card">
                <p style="font-size:14px; color:#ccc; margin-bottom:15px;">የመጋበዣ ሊንክዎን ለጓደኞችዎ ያጋሩ፤ እያንዳንዱ አዲስ ሰው ቦቱን ሲቀላቀል <b>🎁 20 ነፃ ኮይኖችን</b> በዋሌትዎ ላይ ያገኛሉ!</p>
                <div style="background:rgba(255,255,255,0.05); padding:12px; border-radius:10px; font-size:12px; color:#25f4ee; word-break:break-all;" id="ref-link-text">
                    https://t.me/MelaSpaceBot?start=ref_{ADMIN_CHAT_ID}
                </div>
            </div>
            <button class="btn-3d" onclick="navigator.clipboard.writeText(document.getElementById('ref-link-text').innerText); alert('የመጋበዣ ሊንኩ በተሳካ ሁኔታ ኮፒ ተደርጓል!');">📋 ሊንኩን ኮፒ አድርግ</button>
        </div>

        <!-- 🎙️ 4. ዋናው የውስጥ የቪዲዮ/ኦዲዮ ሩም ገጽ -->
        <div class="app-container" id="room-screen">
            <div class="top-bar">
                <div class="live-tag">🔴 LIVE</div>
                <div class="room-name-display" id="active-room-title">ክፍል: ---</div>
                <div style="font-size:13px; color:#fe2c55; cursor:pointer; font-weight:bold;" onclick="exitRoom()">🚪 ውጣ</div>
            </div>
            
            <div class="stage-area">
                <div class="time-reward-badge" id="mic-timer-badge">⏱️ መድረክ ላይ፦ 0 ሰከንድ (🪙 +0)</div>
                <div style="height:5px;"></div>
                
                <!-- 📺 Video & Audio Space (Grid Tiles with Avatar + Wave) -->
                <div class="video-grid" id="video-tiles-grid">
                    <!-- መቀመጫ 1 -->
                    <div class="video-tile empty" id="v-tile-1">
                        <div class="host-badge" id="host-tag-1" style="display:none;">HOST</div>
                        <div class="avatar-container" id="avatar-box-1">👤</div>
                        <div class="audio-wave" id="wave-1"></div>
                        <div class="video-label" id="v-label-1">መቀመጫ 1 (ባዶ)</div>
                    </div>
                    <!-- መቀመጫ 2 -->
                    <div class="video-tile empty" id="v-tile-2">
                        <div class="avatar-container" id="avatar-box-2">👤</div>
                        <div class="audio-wave" id="wave-2"></div>
                        <div class="video-label" id="v-label-2">መቀመጫ 2 (ባዶ)</div>
                    </div>
                    <!-- መቀመጫ 3 -->
                    <div class="video-tile empty" id="v-tile-3">
                        <div class="avatar-container" id="avatar-box-3">👤</div>
                        <div class="audio-wave" id="wave-3"></div>
                        <div class="video-label" id="v-label-3">መቀመጫ 3 (ባዶ)</div>
                    </div>
                    <!-- መቀመጫ 4 -->
                    <div class="video-tile empty" id="v-tile-4">
                        <div class="avatar-container" id="avatar-box-4">👤</div>
                        <div class="audio-wave" id="wave-4"></div>
                        <div class="video-label" id="v-label-4">መቀመጫ 4 (ባዶ)</div>
                    </div>
                </div>
            </div>

            <!-- 🎛️ Control Panel (የድምፅ በተኖች እና ማጀቢያዎች) -->
            <div class="utility-bar">
                <div class="button-row">
                    <button class="btn-3d-sm" style="border-color:#ffdd67; color:#ffdd67;" onclick="alert('🎰 ዕጣው እየወጣ ነው...')">🎰 ሎተሪ</button>
                    <button class="btn-3d-sm" style="border-color:#00ff7f; color:#00ff7f;" onclick="alert('🎲 አዲስ የቢንጎ ጨዋታ ተጀመረ!')">🎲 ቢንጎ</button>
                    <button class="btn-3d-sm" onclick="playRealSound('applause')">👏 ጭብጨባ</button>
                    <button class="btn-3d-sm" onclick="playRealSound('laughter')">😂 ሳቅ</button>
                </div>
                
                <div class="volume-control-box">
                    <span>🔇 ዜማ</span>
                    <input type="range" min="0" max="100" value="15" class="volume-slider" oninput="document.getElementById('bg-kirar-audio').volume = this.value / 100">
                    <select class="fx-select" id="voice-fx-picker">
                        <option value="normal">🎙️ መደበኛ ድምፅ</option>
                        <option value="echo">📻 ኤኮ (Echo)</option>
                        <option value="robot">🤖 ሮቦት (Robot)</option>
                    </select>
                </div>
            </div>

            <!-- 💬 ቻት ክልል -->
            <div class="chat-area" id="chat-box"></div>

            <!-- ✍️ የፅሁፍ መፃፊያ ባር -->
            <div class="chat-input-container">
                <input type="text" id="text-msg-input" class="chat-input" placeholder="ለሹክሹክታ /w @ስም መልእክት ወይም መደበኛ ፅሁፍ...">
                <button class="btn-send-text" onclick="sendTextMessage()">➔</button>
            </div>
            
            <div class="bottom-controls">
                <button class="btn-3d" style="max-width:130px; padding:10px; font-size:12px;" onclick="promptSeatRoleChoice()">🎙️ መድረክ ላይ ውጣ</button>
                <div style="display:flex; align-items:center;">
                    <button class="btn-3d btn-3d-green" style="max-width:90px; padding:10px; margin-right:10px; font-size:12px;" onclick="openGiftTray()">🎁 ስጦታ</button>
                    <div class="nav-icon" style="background: rgba(255,255,255,0.06); width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center;" id="mic-toggle-btn" onclick="toggleMic()">🔊</div>
                </div>
            </div>
        </div>

        <!-- Overlays -->
        <div class="gift-overlay" id="gift-modal-overlay" onclick="closeGiftTray()">
            <div class="gift-tray" id="gift-tray-zone" onclick="event.stopPropagation()">
                <div class="gift-card" onclick="processGiftSend('🌹 ጽጌረዳ', 10, '🌹')"><div style="font-size:30px;">🌹</div></div>
                <div class="gift-card" onclick="processGiftSend('☕ ጀበና ቡና', 50, '☕')"><div style="font-size:30px;">☕</div></div>
                <div class="gift-card" onclick="processGiftSend('👑 የMela አክሊል', 500, '👑')"><div style="font-size:30px;">👑</div></div>
            </div>
            <div class="wheel-box" id="wheel-zone" onclick="event.stopPropagation()">
                <h3 style="color:white; margin-bottom:10px;">🎡 ዕለታዊ የዕድል ማሽከርከሪያ</h3>
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
            let micTimerInterval = null; let secondsOnMic = 0;
            let lastGiftTime = 0; let giftComboCount = 0;

            let seatsData = {{ 
                1: {{ name: "ባዶ", active: false, type: "none", isHost: false }}, 
                2: {{ name: "ባዶ", active: false, type: "none", isHost: false }}, 
                3: {{ name: "ባዶ", active: false, type: "none", isHost: false }}, 
                4: {{ name: "ባዶ", active: false, type: "none", isHost: false }} 
            }};

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
                seatsData[1] = {{ name: myUsername, active: true, type: "audio", isHost: true }}; // ፈጣሪው Host ነው
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

                document.getElementById("bg-kirar-audio").volume = 0.15;
                document.getElementById("bg-kirar-audio").play().catch(e=>console.log(e));

                appendChat("🚀 Mela System", ` ወደ ውይይት ክፍሉ በሰላም መጡ!`, "color:#25f4ee; font-weight:bold;");
                updateSeatsUI();
            }}

            function updateSeatsUI() {{
                for(let i=1; i<=4; i++) {{
                    let tile = document.getElementById(`v-tile-${{i}}`);
                    let label = document.getElementById(`v-label-${{i}}`);
                    let avatar = document.getElementById(`avatar-box-${{i}}`);
                    let hostTag = document.getElementById(`host-tag-${{i}}`);
                    
                    if(hostTag) hostTag.style.display = seatsData[i].isHost ? "block" : "none";

                    if(seatsData[i].active) {{
                        tile.classList.remove("empty");
                        label.innerText = seatsData[i].name;
                        if(seatsData[i].type === "video") {{
                            avatar.style.display = "none";
                        }} else {{
                            avatar.style.display = "flex";
                            avatar.innerText = seatsData[i].name.charAt(0).toUpperCase();
                        }}
                    }} else {{
                        tile.classList.add("empty");
                        avatar.style.display = "flex";
                        avatar.innerText = "👤";
                        label.innerText = `መቀመጫ ${{i}} (ባዶ)`;
                    }}
                }}
            }}

            function promptSeatRoleChoice() {{
                let choice = prompt("በምን መሳተፍ ይፈልጋሉ?\\n1. በቪዲዮ (ካሜራ አብራ)\\n2. በኦዲዮ ብቻ (ድምፅ ብቻ)");
                if(choice === "1") requestSeatWithMode("video");
                else if(choice === "2") requestSeatWithMode("audio");
            }}

            function requestSeatWithMode(mode) {{
                for (let i = 1; i <= 4; i++) {{
                    if (!seatsData[i].active) {{
                        claimSeat(i, mode);
                        break;
                    }}
                }}
            }}

            async function claimSeat(seatId, mode) {{
                currentSeat = seatId;
                let isFirst = (seatId === 1);
                seatsData[seatId] = {{ name: myUsername, active: true, type: mode, isHost: isFirst }};
                updateSeatsUI();
                startMicTimer();

                try {{
                    localTracks.audioTrack = await AgoraRTC.createMicrophoneAudioTrack();
                    if(mode === "video") {{
                        localTracks.videoTrack = await AgoraRTC.createCameraTrack();
                        let tile = document.getElementById(`v-tile-${{seatId}}`);
                        localTracks.videoTrack.play(tile);
                    }} else {{
                        // ኦዲዮ ሲሆን የWave ምልክት በየጊዜው እንዲንቀሳቀስ ማድረጊያ
                        let wave = document.getElementById(`wave-${{seatId}}`);
                        if(wave) {{
                            wave.style.animation = "waveExpand 1.2s infinite ease-in-out";
                        }}
                    }}
                }} catch(e) {{ console.log(e); }}
            }}

            function startMicTimer() {{
                secondsOnMic = 0;
                const badge = document.getElementById("mic-timer-badge");
                badge.style.display = "inline-block";
                micTimerInterval = setInterval(() => {{
                    secondsOnMic++;
                    badge.innerText = `⏱️ መድረክ ላይ፦ ${{secondsOnMic}} ሰከንድ (🪙 +${{Math.floor(secondsOnMic/60) * 5}})`;
                }}, 1000);
            }}

            function sendTextMessage() {{
                const inputEl = document.getElementById("text-msg-input");
                const msgText = inputEl.value.trim();
                if(!msgText) return;
                
                if(msgText.startsWith("/w ")) {{
                    const parts = msgText.split(" ");
                    if(parts.length >= 3 && parts[1].startsWith("@")) {{
                        const targetUser = parts[1].replace("@", "");
                        const secretMsg = parts.slice(2).join(" ");
                        appendChat("🤫 ሹክሹክታ ለ [" + targetUser + "]", secretMsg, "color: #ffaa00; background: rgba(255,170,0,0.08); padding:5px; border-radius:5px;");
                        inputEl.value = ""; return;
                    }}
                }}
                appendChat(myUsername, msgText, "color: #fff;");
                inputEl.value = "";
            }}

            function appendChat(user, msg, style = "") {{
                const box = document.getElementById("chat-box");
                const div = document.createElement("div"); div.style = style;
                div.innerHTML = `<b>${{user}}:</b> ${{msg}}`; box.appendChild(div);
                box.scrollTop = box.scrollHeight;
            }}

            function processGiftSend(giftName, price, emoji) {{
                if (myCoins < price) {{ alert(`ይቅርታ! ባላንስዎ በቂ አይደለም።`); closeGiftTray(); return; }}
                myCoins -= price; closeGiftTray();
                
                let now = Date.now();
                if (now - lastGiftTime <= 10000) {{ giftComboCount++; }} else {{ giftComboCount = 1; }}
                lastGiftTime = now;

                const stage = document.getElementById("animation-stage-layer");
                document.getElementById("big-gift-emoji-element").innerText = emoji;
                stage.style.display = "flex"; setTimeout(() => {{ stage.style.display = "none"; }}, 1500);

                appendChat("🎁 GIFT", `${{myUsername}} ${{giftName}} ${{emoji}} አበረከተ! (Combo x${{giftComboCount}})`, "color:#ff5574; font-weight:bold;");
            }}

            function playRealSound(t) {{
                document.getElementById(t === 'applause' ? 'snd-applause' : 'snd-laughter').play().catch(e=>console.log(e));
            }}

            function openGiftTray() {{ document.getElementById("gift-modal-overlay").style.display = "flex"; document.getElementById("gift-tray-zone").style.display = "grid"; document.getElementById("wheel-zone").style.display = "none"; }}
            function openWheelModal() {{ document.getElementById("gift-modal-overlay").style.display = "flex"; document.getElementById("gift-tray-zone").style.display = "none"; document.getElementById("wheel-zone").style.display = "block"; }}
            function closeGiftTray() {{ document.getElementById("gift-modal-overlay").style.display = "none"; }}
            async function toggleMic() {{
                if(localTracks.audioTrack) {{
                    if(localTracks.audioTrack.muted) {{ localTracks.audioTrack.setMuted(false); document.getElementById("mic-toggle-btn").innerText = "🔊"; }}
                    else {{ localTracks.audioTrack.setMuted(true); document.getElementById("mic-toggle-btn").innerText = "🔇"; }}
                }}
            }}

            function exitRoom() {{
                document.getElementById("bg-kirar-audio").pause();
                if(micTimerInterval) clearInterval(micTimerInterval);
                if(currentSeat) {{
                    let wave = document.getElementById(`wave-${{currentSeat}}`);
                    if(wave) wave.style.animation = "none";
                    seatsData[currentSeat] = {{ name: "ባዶ", active: false, type: "none", isHost: false }};
                }}
                document.getElementById("room-screen").style.display = "none";
                document.getElementById("main-nav-bar").style.display = "flex";
                switchTab('home');
            }}
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
