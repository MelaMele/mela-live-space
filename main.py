import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Mela Space - Complete Master Edition")

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
        <title>Mela Master Space</title>
        <script src="https://download.agora.io/sdk/release/AgoraRTC_N-4.18.0.js"></script>
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
            body, html {{ width: 100%; height: 100%; overflow: hidden; background: #060713; color: #fff; }}
            
            /* ✨ Neon Glows */
            .bg-glow {{ position: absolute; width: 300px; height: 300px; background: radial-gradient(circle, rgba(37,244,238,0.15) 0%, rgba(0,0,0,0) 70%); top: -50px; left: -50px; z-index: 1; pointer-events: none; }}
            .bg-glow-right {{ position: absolute; width: 300px; height: 300px; background: radial-gradient(circle, rgba(254,44,85,0.12) 0%, rgba(0,0,0,0) 70%); bottom: 50px; right: -50px; z-index: 1; pointer-events: none; }}

            /* 🚪 ሎቢ ገጽ */
            .lobby-container {{ position: absolute; top:0; left:0; width:100%; height:calc(100% - 70px); background:#060713; z-index:500; display:flex; flex-direction:column; padding:25px 20px; overflow-y:auto; }}
            .lobby-header {{ text-align:center; margin: 15px 0; z-index: 2; }}
            .lobby-title {{ color:#25f4ee; font-size:26px; font-weight:900; text-shadow: 0 0 20px rgba(37,244,238,0.6); }}
            
            .create-room-box {{ background: rgba(22, 23, 34, 0.7); backdrop-filter: blur(10px); border:1px solid rgba(255,255,255,0.07); border-radius:20px; padding:22px; margin-bottom:25px; box-shadow: 0 8px 32px rgba(0,0,0,0.3); z-index: 2; }}
            .input-field {{ width:100%; background: rgba(47, 48, 61, 0.6); border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:14px; color:white; font-size:14px; margin-bottom:14px; outline:none; }}
            
            .checkbox-container {{ display: flex; align-items: center; gap: 8px; margin-bottom: 14px; font-size: 13px; color: #aaa; }}
            .btn-create {{ width:100%; background: linear-gradient(45deg, #fe2c55, #ff5574); border:none; color:white; padding:15px; border-radius:12px; font-weight:bold; font-size:16px; cursor:pointer; box-shadow: 0 4px 15px rgba(254,44,85,0.4); }}
            
            .room-list-title {{ font-size:15px; color:#888; margin-bottom:15px; font-weight:bold; z-index: 2; }}
            .room-item {{ background: rgba(22, 23, 34, 0.6); border:1px solid rgba(255,255,255,0.05); padding:16px; border-radius:16px; display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; cursor:pointer; z-index: 2; }}

            /* 🗂️ የታብ ገፆች */
            .tab-screen {{ display:none; position:absolute; top:0; left:0; width:100%; height:calc(100% - 70px); background:#060713; z-index:400; padding:25px 20px; overflow-y:auto; }}
            .page-title {{ font-size:24px; font-weight:800; color:#25f4ee; margin-bottom:25px; text-align:center; }}
            .info-card {{ background: rgba(22, 23, 34, 0.7); border:1px solid rgba(255,255,255,0.06); border-radius:20px; padding:22px; margin-bottom:20px; text-align:center; }}
            
            /* 🎙️ ዋናው የውስጥ ሩም */
            .app-container {{ display: none; position: relative; width: 100%; height: 100%; flex-direction: column; background: #060713; }}
            .top-bar {{ display: flex; justify-content: space-between; align-items: center; padding: 15px 20px; border-bottom: 1px solid rgba(255,255,255,0.05); z-index: 10; }}
            .live-tag {{ background: linear-gradient(45deg, #fe2c55, #ff0033); padding: 5px 14px; border-radius: 20px; font-weight: 800; font-size: 11px; }}
            .room-name-display {{ font-size:13px; font-weight:bold; color:#25f4ee; background:rgba(37,244,238,0.15); border: 1px solid rgba(37,244,238,0.2); padding:5px 14px; border-radius:20px; }}
            
            .wave-container {{ width:90%; height:35px; background:rgba(0,0,0,0.4); margin: 0 auto 10px auto; display:none; border-radius:12px; overflow:hidden; border: 1px solid rgba(37,244,238,0.1); }}
            .wave-canvas {{ width:100%; height:100%; }}

            .stage-area {{ flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; padding: 10px; z-index: 5; overflow-y: auto; }}
            .host-section {{ text-align: center; margin-bottom: 12px; position: relative; }}
            .host-avatar {{ width: 75px; height: 75px; border-radius: 50%; background: #111; border: 3px solid #fe2c55; display: flex; align-items: center; justify-content: center; font-size: 34px; margin: 0 auto 5px auto; box-shadow: 0 0 15px rgba(254,44,85,0.3); }}
            .host-badge {{ position: absolute; top: 0; right: 15px; background: #ffdd67; color: #000; font-size: 10px; padding: 2px 6px; border-radius: 10px; font-weight: bold; }}

            .seats-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; width: 100%; max-width: 360px; margin-bottom: 10px; }}
            .seat-circle {{ width: 52px; height: 52px; border-radius: 50%; background: #161722; border: 2px solid #25f4ee; display: flex; align-items: center; justify-content: center; font-size: 20px; margin: 0 auto 4px auto; cursor: pointer; position: relative; }}
            .seat-circle.empty {{ border-color: rgba(255,255,255,0.15); background: rgba(255,255,255,0.03); color: #555; }}
            .seat-name {{ font-size: 11px; color: #bbb; text-align:center; }}
            .user-tag {{ position: absolute; bottom: -2px; background: #fe2c55; color: white; font-size: 8px; padding: 1px 4px; border-radius: 5px; font-weight: bold; display: none; }}

            /* 🎛️ Soundboard & Advanced Control Panel */
            .utility-bar {{ display: flex; flex-direction: column; gap: 10px; width: 100%; background: rgba(255,255,255,0.02); padding: 10px; border-top: 1px solid rgba(255,255,255,0.05); border-bottom: 1px solid rgba(255,255,255,0.05); z-index: 10; }}
            .button-row {{ display: flex; justify-content: space-around; width: 100%; gap: 5px; flex-wrap: wrap; }}
            .util-btn {{ background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: white; padding: 6px 10px; border-radius: 15px; font-size: 11px; font-weight: bold; cursor: pointer; flex: 1; min-width: 80px; text-align: center; }}
            .util-btn:active {{ background: #25f4ee; color: #000; }}
            
            /* 🎵 Volume Slider & Voice FX Box */
            .slider-fx-container {{ display: flex; flex-direction: column; gap: 8px; width: 95%; margin: 0 auto; }}
            .volume-control-box {{ display: flex; align-items: center; justify-content: center; gap: 10px; font-size: 11px; color: #aaa; }}
            .volume-slider {{ flex: 1; -webkit-appearance: none; background: rgba(255,255,255,0.1); height: 5px; border-radius: 3px; outline: none; }}
            .volume-slider::-webkit-slider-thumb {{ -webkit-appearance: none; appearance: none; width: 14px; height: 14px; border-radius: 50%; background: #25f4ee; cursor: pointer; box-shadow: 0 0 8px #25f4ee; }}
            
            .fx-box {{ display: flex; justify-content: center; gap: 10px; align-items: center; font-size: 11px; color: #888; }}
            .fx-select {{ background: #161722; border: 1px solid rgba(255,255,255,0.1); color: white; border-radius: 8px; padding: 3px 8px; font-size: 11px; outline: none; }}

            /* 💬 የላይቭ ቻት ክልል */
            .chat-area {{ height: 110px; width: 100%; padding: 10px; background: linear-gradient(transparent, rgba(6,7,19,0.98)); overflow-y: auto; font-size: 12px; display: flex; flex-direction: column; gap: 5px; z-index: 10; }}
            
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

            /* 🎬 ሲኒማቲክ የስጦታ አኒሜሽን */
            .cinematic-stage {{ display:none; position:fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:2500; align-items:center; justify-content:center; }}
            .big-gift-anim {{ font-size:120px; animation: cinematicBlast 1.5s forwards cubic-bezier(0.175, 0.885, 0.32, 1.275); }}
            @keyframes cinematicBlast {{
                0% {{ transform: scale(0) rotate(-45deg); opacity: 0; }}
                30% {{ transform: scale(1.3) rotate(10deg); opacity: 1; }}
                50% {{ transform: scale(1) rotate(0deg); }}
                100% {{ opacity: 0; transform: scale(0.6) translateY(-150px); }}
            }}
            
            /* 🏆 Leaderboard Style */
            .leaderboard-list {{ text-align: left; margin-top: 15px; }}
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
                        <div style="font-weight:bold; color:#fff; font-size:15px;">👵 የእናቶች ወግ (Mela Lounge) ❤️</div>
                        <div style="font-size:12px; color:#aaa; margin-top:3px;">የባህል ወጎች፣ ምክሮች እና ማህበራዊ ትዝታዎች መጋሪያ መድረክ</div>
                    </div>
                    <div style="color:#25f4ee; font-size:12px; font-weight:bold; background:rgba(37,244,238,0.1); padding:6px 12px; border-radius:12px;">🎙️ ግባ</div>
                </div>
                <div class="room-item" onclick="joinExistingRoom('📚 የተማሪዎች መወያያ (Mela Room)')">
                    <div>
                        <div style="font-weight:bold; color:#fff; font-size:15px;">📚 የተማሪዎች መወያያ (Mela Room) 🎓</div>
                        <div style="font-size:12px; color:#aaa; margin-top:3px;">ለትምህርት፣ ለዕውቀት እና ለቴክኖሎጂ ክህሎት ማሳደጊያ ውይይት</div>
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
            
            <div class="info-card">
                <h3 style="color:#ffdd67; font-size:15px; margin-bottom:10px;">🏆 የክፍሉ ከፍተኛ ለጋሾች (Leaderboard)</h3>
                <div class="leaderboard-list">
                    <div class="leader-row"><span>🥇 1. Melaku M. (Host)</span><span style="color:#ffdd67;">👑 5,200 🪙</span></div>
                    <div class="leader-row"><span>🥈 2. ቤተልሔም አሰፋ</span><span style="color:#ccc;">💎 2,800 🪙</span></div>
                    <div class="leader-row"><span>🥉 3. ዮናስ ካሳሁን</span><span style="color:#cd7f32;">🔥 1,450 🪙</span></div>
                </div>
            </div>
            <button class="btn-create" style="background: linear-gradient(45deg, #00cd63, #00ff7f); width:100%;" onclick="alert('የአውቶማቲክ ቴሌብር ክፍያ ሲስተም በቅርቡ ይለቀቃል!')">💳 በቴሌብር ኮይን ግዛ (Top Up)</button>
        </div>

        <div class="tab-screen" id="referral-screen">
            <div class="page-title">ጋብዘው ይክበሩ (Refer & Earn)</div>
            <div class="info-card">
                <h3 style="color:#ffdd67; margin-bottom:12px;">🎉 ለእያንዳንዱ ሰው 20 ነፃ ኮይን!</h3>
                <p style="font-size:13px; color:#ccc; margin-bottom:15px; line-height:1.5;">የእርስዎን መለያ ሊንክ ለጓደኞችዎ ያጋሩ፤ እነሱ ሊንኩን ተጠቅመው መተግበሪያውን ሲቀላቀሉ ለእርስዎ 20 ኮይን በዋሌትዎ ላይ ይጨመራል።</p>
                <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px; font-size:11px; color:#25f4ee; border:1px dashed rgba(37,244,238,0.3); word-break:break-all;" id="ref-link-text">
                    https://t.me/MelaSpaceBot?start=ref_1065443252
                </div>
            </div>
            <button class="btn-create" onclick="copyRefLink()">📋 ሊንኩን ኮፒ አድርግ</button>
        </div>

        <div class="app-container" id="room-screen">
            <div class="top-bar">
                <div class="live-tag" id="room-badge-type">🔴 LIVE</div>
                <div class="room-name-display" id="active-room-title">ክፍል: ---</div>
                <div style="font-size:13px; color:#fe2c55; cursor:pointer; font-weight:bold;" onclick="exitRoom()">🚪 ውጣ</div>
            </div>
            
            <div class="stage-area">
                <div class="wave-container" id="wave-visualizer-box"><canvas id="wave-canvas" class="wave-canvas"></canvas></div>
                <div class="host-section">
                    <div class="host-avatar" id="host-crown-zone">🎙️</div>
                    <div class="host-badge">HOST</div>
                    <div style="font-size:13px; font-weight:bold; color:#fff;" id="room-host-name">---</div>
                </div>
                <div class="seats-grid" id="seats-container"></div>
            </div>

            <div class="utility-bar">
                <div class="button-row">
                    <button class="util-btn" style="border-color:#ffdd67; color:#ffdd67;" onclick="runLuckyDraw()">🎰 Lucky Draw</button>
                    <button class="util-btn" style="border-color:#00ff7f; color:#00ff7f;" onclick="startBingoGame()">🎲 Bingo ግጠም</button>
                    <button class="util-btn" onclick="playRealSound('applause')">👏 ጭብጨባ</button>
                    <button class="util-btn" onclick="playRealSound('laughter')">😂 ሳቅ</button>
                </div>
                
                <div class="slider-fx-container">
                    <div class="volume-control-box">
                        <span>🔇 ዜማ</span>
                        <input type="range" min="0" max="100" value="15" class="volume-slider" id="kirar-vol-slider" oninput="adjustMusicVolume(this.value)">
                        <span>🔊</span>
                    </div>
                    <div class="fx-box">
                        <span>🎤 የድምፅ ማጣሪያ፦</span>
                        <select class="fx-select" id="voice-fx-mode" onchange="changeVoiceFX(this.value)">
                            <option value="normal">⚙️ መደበኛ ድምፅ</option>
                            <option value="echo">📻 Echo (የመድረክ ድምፅ)</option>
                            <option value="robot">🤖 ሮቦት ፊልተር</option>
                            <option value="baby">👶 የህፃን ድምፅ</option>
                        </select>
                    </div>
                </div>
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
                <div class="gift-card" onclick="processGiftSend('🌹 ጽጌረዳ', 10, '🌹')"><div class="gift-emoji">🌹</div></div>
                <div class="gift-card" onclick="processGiftSend('☕ የጀበና ቡና', 50, '☕')"><div class="gift-emoji">☕</div></div>
                <div class="gift-card" onclick="processGiftSend('🦁 አንበሳ', 200, '🦁')"><div class="gift-emoji">🦁</div></div>
                <div class="gift-card" onclick="processGiftSend('👑 የMela አክሊል', 500, '👑')"><div class="gift-emoji">👑</div></div>
            </div>
        </div>

        <div class="cinematic-stage" id="animation-stage-layer"><div class="big-gift-anim" id="big-gift-emoji-element">👑</div></div>

        <script>
            const AGORA_APP_ID = "ea7dfdf9926d400fb8a54d31be0bd44c"; 
            let client = AgoraRTC.createClient({{ mode: "rtc", codec: "vp8" }});
            let localAudioTrack = null; let currentSeat = null;
            let myUsername = "እንግዳ"; let currentRoomName = ""; let myCoins = 350; 
            
            let audioContext = null; let analyser = null; let dataArray = null; let animationFrameId = null;
            let seatsData = {{ 1:{{name:"ባዶ",active:false,tag:""}}, 2:{{name:"ባዶ",active:false,tag:""}}, 3:{{name:"ባዶ",active:false,tag:""}}, 4:{{name:"ባዶ",active:false,tag:""}}, 5:{{name:"ባዶ",active:false,tag:""}}, 6:{{name:"ባዶ",active:false,tag:""}} }};

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
                    document.getElementById("wallet-coin-balance").innerText = myCoins;
                }} else if(tabName === 'referral') {{
                    document.getElementById("referral-screen").style.display = "block";
                    document.getElementById("nav-ref").classList.add("active");
                }}
            }}

            function createNewRoomAction() {{
                const uName = document.getElementById("lobby-username").value.trim();
                const rName = document.getElementById("lobby-roomname").value.trim();
                const isVip = document.getElementById("lobby-is-vip").checked;
                if(!uName || !rName) {{ alert("እባክዎ መረጃዎችን በትክክል ያስገቡ!"); return; }}
                myUsername = uName; currentRoomName = rName;
                
                if(isVip) {{
                    let pin = prompt("ለቪአይፒ ክፍሉ መቆለፊያ ባለ 4 አሃዝ ፒን (PIN) ያስገቡ፦");
                    if(!pin) return;
                    currentRoomName = "🔒 [VIP] " + rName;
                }}
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
                document.getElementById("room-host-name").innerText = myUsername;
                document.getElementById("chat-box").innerHTML = "";
                
                if(currentRoomName.includes("🔒")) {{
                    document.getElementById("room-badge-type").innerText = "🔒 VIP PRIVATE";
                    document.getElementById("room-badge-type").style.background = "linear-gradient(45deg, #ffdd67, #ffaa00)";
                    document.getElementById("room-badge-type").style.color = "#000";
                }} else {{
                    document.getElementById("room-badge-type").innerText = "🔴 LIVE";
                    document.getElementById("room-badge-type").style.background = "linear-gradient(45deg, #fe2c55, #ff0033)";
                    document.getElementById("room-badge-type").style.color = "#fff";
                }}

                // 🎵 የጀርባ ሙዚቃ ማስጀመር
                const audio = document.getElementById("bg-kirar-audio");
                audio.volume = 0.15;
                document.getElementById("kirar-vol-slider").value = 15;
                audio.play().catch(e => console.log("Audio waiting for active interactions."));

                appendChat("🚀 Mela System", ` ወደ "${{currentRoomName}}" ክፍል በሰላም መጡ!`, "color:#25f4ee; font-weight:bold;");
                renderSeats();
                initAgora(currentRoomName);
            }}

            function adjustMusicVolume(value) {{
                const audio = document.getElementById("bg-kirar-audio");
                audio.volume = value / 100;
            }}

            // 👏😂 የእውነተኛ ድምፅ ማጫወቻ ፈንክሽን
            function playRealSound(type) {{
                try {{
                    const soundEl = document.getElementById(type === 'applause' ? 'snd-applause' : 'snd-laughter');
                    if(soundEl) {{
                        soundEl.currentTime = 0;
                        soundEl.volume = 1.0;
                        let pPromise = soundEl.play();
                        if (pPromise !== undefined) {{
                            pPromise.catch(error => {{ console.log("Audio play blocked: ", error); }});
                        }}
                    }}
                    appendChat("🎙️ Soundboard", ` [${{myUsername}}] የ${{type === 'applause'?'ጭብጨባ 👏':'ሳቅ 😂'}} ድምፅ ለቋል!`, "color:#25f4ee; font-weight:bold;");
                }} catch (err) {{
                    console.log("Audio Error: ", err);
                }}
            }}

            // 🎤 የድምፅ ማጣሪያዎችን መቀያየሪያ
            function changeVoiceFX(mode) {{
                appendChat("🎙️ Voice FX", ` [${{myUsername}}] የድምፅ ማጣሪያውን ወደ [${{mode}}] ቀይሯል።`, "color:#00ff7f; font-size:11px;");
                // አጎራ ኤስዲኬ ላይ የድምፅ ማጣሪያዎችን እዚህ ጋር አታች ማድረግ ይቻላል
            }}

            // 🎲 በክፍሉ ውስጥ የቢንጎ ጨዋታ ማስጀመሪያ
            function startBingoGame() {{
                appendChat("🎲 BINGO", ` [${{myUsername}}] አዲስ የቢንጎ ግሩፕ ጨዋታ በአዳራሹ ጀምሯል! ቁጥሮች በድምፅ ሊጠሩ ነው...`, "color:#00ff7f; font-weight:bold;");
                let count = 0;
                let interval = setInterval(() => {{
                    count++;
                    let luckyNum = Math.floor(Math.random() * 90) + 1;
                    appendChat("🎲 የቢንጎ ቁጥር", ` 🚨 ቁጥር ${{luckyNum}}!`, "color:#ffdd67; font-weight:bold;");
                    if(count >= 5) {{
                        clearInterval(interval);
                        appendChat("🎉 BINGO አሸናፊ", " ጨዋታው ተጠናቋል! አሸናፊው 50 ኮይን ወስዷል።", "color:#00cd63; font-weight:bold;");
                    }}
                }}, 3000);
            }}

            function copyRefLink() {{
                const linkText = document.getElementById("ref-link-text").innerText.trim();
                navigator.clipboard.writeText(linkText).then(() => {{
                    alert("የሪፈራል ሊንክዎ በትክክል ኮፒ ሆኗል!");
                }}).catch(() => {{
                    alert("እባክዎ ሊንኩን ተጭነው ይቅዱት።");
                }});
            }}

            function sendTextMessage() {{
                const inputEl = document.getElementById("text-msg-input");
                const msgText = inputEl.value.trim();
                if(!msgText) return;
                appendChat(myUsername, msgText, "color: #fff; background: rgba(255,255,255,0.02); padding: 4px 8px; border-radius: 6px;");
                inputEl.value = ""; 
            }}

            function runLuckyDraw() {{
                if(myCoins < 10) {{ alert("ለቲኬት የሚሆን በቂ ኮይን የለዎትም!"); return; }}
                myCoins -= 10;
                appendChat("🎰 ሎተሪ", `[${{myUsername}}] የዕድል ቁጥር ቲኬት ገዝተዋል። እጣው እየወጣ ነው...`, "color:#ffdd67;");
                
                setTimeout(() => {{
                    const win = Math.random() > 0.4;
                    if(win) {{
                        myCoins += 50;
                        appendChat("🎉 ጃክፖት", ` [${{myUsername}}] የእድል ቁጥር እጣው ደርሶዎት 50 ኮይን አሸንፈዋል!`, "color:#00cd63; font-weight:bold;");
                        playRealSound('applause');
                    }} else {{
                        appendChat("🎰 ሎተሪ", `ይቅርታ እጣው አልደረሶትም። በድጋሚ ይሞክሩ!`, "color:#888;");
                    }}
                }}, 2000);
            }}

            function openGiftTray() {{ document.getElementById("gift-modal-overlay").style.display = "flex"; }}
            function closeGiftTray() {{ document.getElementById("gift-modal-overlay").style.display = "none"; }}

            function processGiftSend(giftName, price, emoji) {{
                if (myCoins < price) {{ alert(`ይቅርታ! ባላንስዎ በቂ አይደለም።`); closeGiftTray(); return; }}
                myCoins -= price;
                closeGiftTray();
                
                // ዘውድ እና ባጅ አኒሜሽን ህግ
                if(giftName.includes("አክሊል")) {{
                    document.getElementById("host-crown-zone").innerText = "👑";
                    appendChat("👑 የክብር ዘውድ", ` ${{myUsername}} ከፍተኛ ስጦታ በመስጠቱ የክብር አክሊል ተቀዳጅቷል!`, "color:#ffdd67; font-weight:bold;");
                }}

                const stage = document.getElementById("animation-stage-layer");
                const emojiEl = document.getElementById("big-gift-emoji-element");
                emojiEl.innerText = emoji; stage.style.display = "flex";
                setTimeout(() => {{ stage.style.display = "none"; }}, 1500);
                appendChat("🎁 GIFT", `${{myUsername}} ለክፍሉ ${{giftName}} ${{emoji}} አበርክተዋል!`, "color:#ff5574; font-weight:bold;");
            }}

            async function exitRoom() {{
                document.getElementById("bg-kirar-audio").pause();
                if(localAudioTrack) {{ localAudioTrack.stop(); localAudioTrack.close(); localAudioTrack = null; }}
                stopVoiceWave(); await client.leave(); currentSeat = null;
                for(let i=1; i<=6; i++) seatsData[i] = {{ name: "ባዶ", active: false, tag: "" }};
                document.getElementById("room-screen").style.display = "none";
                document.getElementById("main-nav-bar").style.display = "flex";
                switchTab('home');
            }}

            function renderSeats() {{
                const container = document.getElementById("seats-container"); container.innerHTML = "";
                for (let i = 1; i <= 6; i++) {{
                    const seat = seatsData[i]; const node = document.createElement("div");
                    node.innerHTML = `<div class="seat-circle ${{seat.active ? '' : 'empty'}}" onclick="claimSeat(${{i}})">${{seat.active?'👤':'➕'}}<div class="user-tag" id="utag-${{i}}">${{seat.tag}}</div></div><div class="seat-name">${{seat.name}}</div>`;
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
                if (currentSeat) seatsData[currentSeat] = {{ name: "ባዶ", active: false, tag:"" }};
                currentSeat = seatId; seatsData[seatId] = {{ name: myUsername, active: true, tag: "VIP" }}; renderSeats();
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
