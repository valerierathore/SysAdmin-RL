import os
from flask import Flask, request, jsonify
from pydantic import BaseModel
from typing import Optional

app = Flask(__name__)


class ActionRequest(BaseModel):
    action: str

class StateResponse(BaseModel):
    status: str
    is_fixed: bool
    reward: float
    observation: str



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
        "observation": "Current system load: 0.5. Service 'web_server' is stopped."
    })

@app.route('/step', methods=['POST'])
def step():
    data = request.json
    action = data.get("action", "")
    
    if "restart" in action.lower():
        return jsonify({
            "status": "success",
            "observation": "Service 'web_server' restarted successfully.",
            "is_fixed": True,
            "reward": 1.0
        })
    return jsonify({
        "status": "success",
        "observation": "Command not recognized. Service still down.",
        "is_fixed": False,
        "reward": 0.0
    })

def main():
    app.run(host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
