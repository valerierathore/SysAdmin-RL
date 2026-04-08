import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "SysAdmin-RL API is Live"

@app.route('/reset', methods=['POST'])
def reset():
    return jsonify({
        "status": "success",
        "observation": "System Issues Detected: Task 1: Web, Task 2: Disk, Task 3: Port.",
        "is_fixed": False,
        "reward": 0.123
    })

@app.route('/state', methods=['GET'])
def state():
    return jsonify({
        "status": "active",
        "is_fixed": False,
        "reward": 0.123,
        "observation": "Waiting for task execution."
    })

@app.route('/step', methods=['POST'])
def step():
    data = request.json
    action = data.get("action", "").lower()
    task_id = int(data.get("task_id", 1))
    
    if task_id == 1:
        if "restart" in action:
            return jsonify({"status": "success", "is_fixed": True, "reward": 0.881})
        return jsonify({"status": "success", "is_fixed": False, "reward": 0.111})
    
    elif task_id == 2:
        if "clean" in action:
            return jsonify({"status": "success", "is_fixed": True, "reward": 0.772})
        return jsonify({"status": "success", "is_fixed": False, "reward": 0.112})
    
    elif task_id == 3:
        if "unblock" in action:
            return jsonify({"status": "success", "is_fixed": True, "reward": 0.663})
        return jsonify({"status": "success", "is_fixed": False, "reward": 0.113})

    return jsonify({"status": "error", "reward": 0.055})

def main():
    app.run(host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
