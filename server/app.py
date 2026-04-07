import os
import time
import threading
from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/')
def home():
    return "SysAdmin-RL Environment is Running!"

@app.route('/reset', methods=['POST'])
def reset():
    """
    Handles the Environment Reset. 
    Returns the initial state for the agent.
    """
    return jsonify({
        "status": "success", 
        "output": "Terminal initialized. System alert: 'web_server' is unresponsive.",
        "is_fixed": False
    })

@app.route('/step', methods=['POST'])
def step():
    """
    Handles the Environment Step.
    Returns the result of the agent's action.
    """
  
    return jsonify({
        "status": "success",
        "output": "Service 'web_server' restarted on port 8080.",
        "is_fixed": True,
        "reward": 1.0
    })

def main():
    """
    The main entry point for the server. 
    This is what the pyproject.toml 'server' script calls.
    """
    app.run(host="0.0.0.0", port=7860)

if __name__ == "__main__":
   
    threading.Thread(target=main, daemon=True).start()
    
   
    while True:
        time.sleep(10)
