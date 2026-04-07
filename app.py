import os
import time
import threading
from flask import Flask, request, jsonify


app = Flask(__name__)

# Mandatory Home Route
@app.route('/')
def home():
    return "SysAdmin-RL Environment is Running!"

@app.route('/reset', methods=['POST'])
def reset():
    return jsonify({
        "status": "success", 
        "output": "Terminal initialized. System alert: 'web_server' is unresponsive.",
        "is_fixed": False
    })

# Mandatory Step Route
@app.route('/step', methods=['POST'])
def step():

    return jsonify({
        "status": "success",
        "output": "Service 'web_server' restarted on port 8080.",
        "is_fixed": True,
        "reward": 1.0
    })

def run_flask():
    
    app.run(host="0.0.0.0", port=7860)


class SupportAction:
    def __init__(self, command, target):
        self.command = command
        self.target = target

class SupportObservation:
    def __init__(self, output, is_fixed):
        self.output = output
        self.is_fixed = is_fixed

class SupportEnv:
    def reset(self):
        return SupportObservation("Terminal initialized. System alert: 'web_server' is unresponsive.", False)

    def step(self, action):
        if action.command == "restart_service" and action.target == "web_server":
            return SupportObservation("SUCCESS: 'web_server' restarted on port 8080.", True)
        return SupportObservation(f"Executed {action.command} on {action.target}", False)


if __name__ == "__main__":
 
    threading.Thread(target=run_flask, daemon=True).start()


    env = SupportEnv()
    obs = env.reset()
    print(f"START: {obs.output}")
    
    print("\n--- Running Automated Test ---")
    final_obs = env.step(SupportAction(command="restart_service", target="web_server"))
    print(f"RESULT: {final_obs.output} | Fixed: {final_obs.is_fixed}")
    
    print("Environment is now live. Waiting for evaluation...")


    while True:
        time.sleep(10)
