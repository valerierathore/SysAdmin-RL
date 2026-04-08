import os
from flask import Flask, request, jsonify
from pydantic import BaseModel

app = Flask(__name__)

@app.route('/')
def home():
    return "SysAdmin-RL API is Live and Running!"

@app.route('/reset', methods=['POST'])
def reset():
    return jsonify({
        "status": "success",
        "observation": "System alert: 'web_server' service is down (Port 80).",
        "is_fixed": False,
        "reward": 0.0
    })

@app.route('/state', methods=['GET'])
def state():
    return jsonify({
        "status": "active",
        "is_fixed": False,
        "reward": 0.0,
        "observation": "Service 'web_server' is stopped. Load: 0.1."
    })

@app.route('/step', methods=['POST'])
def step():
    data = request.json
    action = data.get("action", "").lower()
    
    if "restart" in action:
        return jsonify({
            "status": "success",
            "observation": "Service 'web_server' restarted successfully.",
            "is_fixed": True,
            "reward": 1.0
        })
    return jsonify({
        "status": "success",
        "observation": "Action failed. Service still down.",
        "is_fixed": False,
        "reward": 0.0
    })

def main():
    app.run(host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
