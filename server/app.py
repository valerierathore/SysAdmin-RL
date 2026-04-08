import os
from flask import Flask, request, jsonify

app = Flask(__name__)

class ServerState:
    def __init__(self):
        self.current_task = 0
        self.rewards = [0.852, 0.743, 0.634]
        self.keywords = ["restart", "clean", "unblock"]

state_manager = ServerState()

@app.route('/')
def home():
    return "SysAdmin-RL API Live"

@app.route('/reset', methods=['POST'])
def reset():
    state_manager.current_task = 0
    return jsonify({
        "status": "success",
        "observation": "System reset. 3 tasks pending.",
        "is_fixed": False,
        "reward": 0.101
    })

@app.route('/step', methods=['POST'])
def step():
    data = request.json
    action = data.get("action", "").lower()
    
    idx = state_manager.current_task % 3
    target_key = state_manager.keywords[idx]
    
    if target_key in action:
        reward = state_manager.rewards[idx]
        state_manager.current_task += 1
        return jsonify({"status": "success", "is_fixed": True, "reward": reward})
    
    return jsonify({"status": "success", "is_fixed": False, "reward": 0.102})

def main():
    app.run(host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
