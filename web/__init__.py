#@hdfilm0900_bot
import os
from flask import Flask, render_template_string

web_app = Flask(__name__)

# --- Simple Home Page Template ---
home_tmplt = """
<!DOCTYPE html>
<html>
<head>
    <title>HA Bots</title>
    <style>
        body { background: #020617; color: white; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; font-family: sans-serif; }
        h1 { color: #818cf8; border: 1px solid #1e293b; padding: 20px; border-radius: 10px; background: #0f172a; }
    </style>
</head>
<body>
    <h1>HA Bots is Online ✓</h1>
</body>
</html>
"""

@web_app.route('/')
def home():
    return render_template_string(home_tmplt)

# Ye function hona zaroori hai kyunki bot.py ise hi call kar raha hai
def run_server():
    port = int(os.environ.get("PORT", 10000))
    print(f"Flask server starting on port {port}...")
    web_app.run(host="0.0.0.0", port=port)

