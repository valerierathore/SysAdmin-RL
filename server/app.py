import os
from flask import Flask, request, jsonify

app = Flask(__name__)

def calculate_grader_reward(task_index, action):
    success_map = {
        0: {"key": "restart", "score": 0.88},
        1: {"key": "clean", "score": 0.77},
        2: {"key": "unblock", "score": 0.66}
    }
    
    if success_map[task_index]["key"] in action.lower():
        return success_map[task_index]["score"]
    return 0.11

@app.route('/')
def home():
    return "SysAdmin-RL API is Live"

@app.route('/reset', methods=['POST'])
def reset():
    return jsonify({
        "status": "success",
        "observation": "System Offline. Issues: 1. Service, 2. Disk, 3. Port.",
        "is_fixed": False,
        "reward": 0.11
    })

@app.route('/step', methods=['POST'])
def step():
    data = request.json
    action = data.get("action", "")
    step_num = int(data.get("step_num", 0))
    
    current_reward = calculate_grader_reward(step_num, action)
    fixed = current_reward > 0.5
    
    return jsonify({
        "status": "success",
        "is_fixed": fixed,
        "reward": current_reward,
        "observation": "Task complete" if fixed else "Task failed"
    })

def main():
    app.run(host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
