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
        "observation": "System Offline. 3 Tasks Pending: 1. Restart Web, 2. Clear Cache, 3. Update Firewall.",
        "is_fixed": False,
        "reward": 0.02
    })

@app.route('/state', methods=['GET'])
def state():
    return jsonify({
        "status": "active",
        "is_fixed": False,
        "reward": 0.02,
        "observation": "Waiting for task selection."
    })

@app.route('/step', methods=['POST'])
def step():
    data = request.json
    action = data.get("action", "").lower()
    task_id = data.get("task_id", 1)
    
    if task_id == 1:
        if "restart" in action:
            return jsonify({"status": "success", "is_fixed": True, "reward": 0.95})
        return jsonify({"status": "success", "is_fixed": False, "reward": 0.05})
    
    elif task_id == 2:
        if "cache" in action:
            return jsonify({"status": "success", "is_fixed": True, "reward": 0.92})
        return jsonify({"status": "success", "is_fixed": False, "reward": 0.05})
    
    elif task_id == 3:
        if "firewall" in action:
            return jsonify({"status": "success", "is_fixed": True, "reward": 0.88})
        return jsonify({"status": "success", "is_fixed": False, "reward": 0.05})

    return jsonify({"status": "error", "reward": 0.02})

def main():
    app.run(host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
