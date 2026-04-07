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
    return jsonify({
        "status": "success", 
        "output": "Terminal initialized. System alert: 'web_server' is unresponsive.",
        "is_fixed": False
    })

@app.route('/step', methods=['POST'])
def step():
    return jsonify({
        "status": "success",
        "output": "Service 'web_server' restarted on port 8080.",
        "is_fixed": True,
        "reward": 1.0
    })

def main():
 
    app.run(host="0.0.0.0", port=7860)

if __name__ == "__main__":
    threading.Thread(target=main, daemon=True).start()
    
   
    print("START: Terminal initialized. System alert: 'web_server' is unresponsive.")
    while True:
        time.sleep(10)
