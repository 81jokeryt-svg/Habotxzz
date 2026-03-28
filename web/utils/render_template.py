import os
import mimetypes
from flask import Flask, render_template_string, request, abort
from datetime import datetime

# Flask App Initialization
web_app = Flask(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# WATCH PAGE TEMPLATE (Aapka Diya Hua Design)
# ─────────────────────────────────────────────────────────────────────────────
watch_tmplt = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ file_name }} - HA Bots</title>
    <link rel="stylesheet" href="https://cdn.plyr.io/3.7.8/plyr.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">
    <style>
        :root {
            --p:#818cf8; --p2:#6366f1; --sec:#a78bfa; --acc:#38bdf8;
            --txt:#f1f5f9; --txt2:#94a3b8;
            --bg:#020617; --glass:rgba(10,18,38,.8); --gb:rgba(129,140,248,.13);
        }
        body { font-family:'Inter',sans-serif; background:var(--bg); color:var(--txt); min-height:100vh; display:flex; flex-direction:column; margin:0; }
        header { padding:.8rem 1.5rem; background:var(--glass); border-bottom:1px solid var(--gb); text-align:center; backdrop-filter:blur(20px); }
        .header-logo { font-size:1.2rem; font-weight:800; background:linear-gradient(90deg,#e2e8f0,var(--p)); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
        .container { flex:1; padding:2rem; display:flex; flex-direction:column; align-items:center; }
        .player-wrap { width:100%; max-width:900px; aspect-ratio:16/9; background:#000; border-radius:15px; overflow:hidden; box-shadow:0 20px 50px rgba(0,0,0,0.5); }
        .btn-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 20px; width: 100%; max-width: 900px; }
        .xbtn { padding: 12px; text-align: center; border-radius: 8px; text-decoration: none; color: white; font-weight: bold; font-size: 0.9rem; transition: 0.3s; }
        .btn-dl { background: linear-gradient(135deg,#4f46e5,#818cf8); }
        .btn-vlc { background: linear-gradient(135deg,#92400e,#f59e0b); }
        .btn-mx { background: linear-gradient(135deg,#065f46,#10b981); }
        footer { padding: 1rem; text-align: center; font-size: 0.8rem; color: var(--txt2); }
        @media (max-width: 600px) { .btn-row { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <header><span class="header-logo">HA Bots</span><br><small>{{ file_name }}</small></header>
    <div class="container">
        <div class="player-wrap">
            <video class="player" playsinline controls>
                <source src="{{ src }}" type="video/mp4">
            </video>
        </div>
        <div class="btn-row">
            <a href="{{ src }}" class="xbtn btn-dl">Download Now</a>
            <a href="vlc://{{ src }}" class="xbtn btn-vlc">Play in VLC</a>
            <a href="intent:{{ src }}#Intent;package=com.mxtech.videoplayer.ad;end" class="xbtn btn-mx">MX Player</a>
        </div>
    </div>
    <footer>Powered by <a href="https://t.me/HA_Bots" style="color:var(--p); text-decoration:none;">HA Bots</a></footer>
    <script src="https://cdn.plyr.io/3.7.8/plyr.js"></script>
    <script>const player = new Plyr('.player');</script>
</body>
</html>
"""

# ─────────────────────────────────────────────────────────────────────────────
# HOME PAGE TEMPLATE
# ─────────────────────────────────────────────────────────────────────────────
home_tmplt = """
<!DOCTYPE html>
<html>
<head>
    <title>HA Bots - Home</title>
    <style>
        body { background: #020617; color: white; font-family: sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .card { text-align: center; padding: 40px; border: 1px solid #1e293b; border-radius: 20px; background: #0f172a; }
        h1 { color: #818cf8; }
    </style>
</head>
<body>
    <div class="card">
        <h1>HA Bots is Online</h1>
        <p>Bot Status: Running Perfectly ✓</p>
    </div>
</body>
</html>
"""

# ─────────────────────────────────────────────────────────────────────────────
# ROUTES (Flask Logic)
# ─────────────────────────────────────────────────────────────────────────────

@web_app.route('/')
def home():
    return render_template_string(home_tmplt)

@web_app.route('/watch')
def watch_video():
    # URL parameters se data uthayega: /watch?id=123&name=video.mp4
    file_id = request.args.get('id')
    file_name = request.args.get('name', 'Video File')
    
    # Yahan aapko apna bot ka stream domain dalna hoga
    stream_url = f"https://your-bot-link.com/download/{file_id}" 
    
    return render_template_string(watch_tmplt, file_name=file_name, src=stream_url)

# Render ke liye Health Check Route
@web_app.route('/health')
def health():
    return "OK", 200

# Server start karne ka function
def run_server():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host="0.0.0.0", port=port)
