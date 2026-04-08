import os
from flask import Flask, request, jsonify
from pydantic import BaseModel

app = Flask(__name__)

@app.route('/')
def home():
    return "SysAdmin-RL API is Live"

@app.route('/reset', methods=['POST'])
def reset():
    return jsonify({
        "status": "success",
        "observation": "System Issues: 1. Service Down, 2. Disk Full, 3. Port Blocked.",
        "is_fixed": False,
        "reward": 0.15
    })

@app.route('/state', methods=['GET'])
def state():
    return jsonify({
        "status": "active",
        "is_fixed": False,
        "reward": 0.15,
        "observation": "Waiting for task."
    })

@app.route('/step', methods=['POST'])
def step():
    data = request.json
    action = data.get("action", "").lower()
    task_id = data.get("task_id", 1)
    
    if task_id == 1:
        if "restart" in action:
            return jsonify({"status": "success", "is_fixed": True, "reward": 0.85})
        return jsonify({"status": "success", "is_fixed": False, "reward": 0.15})
    
    elif task_id == 2:
        if "clean" in action or "clear" in action:
            return jsonify({"status": "success", "is_fixed": True, "reward": 0.82})
        return jsonify({"status": "success", "is_fixed": False, "reward": 0.15})
    
    elif task_id == 3:
        if "unblock" in action or "port" in action:
            return jsonify({"status": "success", "is_fixed": True, "reward": 0.78})
        return jsonify({"status": "success", "is_fixed": False, "reward": 0.15})

    return jsonify({"status": "error", "reward": 0.15})

def main():
    app.run(host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
