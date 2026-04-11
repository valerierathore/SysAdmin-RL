import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- Environment State ---
class SystemState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.service_running = False
        self.port_8080_blocked = True  # The "Hard" task root cause
        self.disk_full = True          # The "Medium" task
        self.logs_viewed = False
        self.steps_taken = 0
        return "System initialized. Web server is DOWN. Status: Error 502."

state = SystemState()

# --- Main App Logic ---
@app.route('/reset', methods=['POST'])
def reset():
    msg = state.reset()
    return jsonify({"observation": msg, "status": "success"})

@app.route('/step', methods=['POST'])
def step():
    data = request.json
    action = data.get("action", "").lower().strip()
    state.steps_taken += 1
    
    observation = ""
    reward = 0.0
    done = False

    # 1. Diagnostic Actions
    if action == "read_syslog":
        observation = "syslog: [CRITICAL] Service 'web-stack' failed to bind to port 8080."
        state.logs_viewed = True
        reward = 0.1  # Small reward for investigating

    elif action == "read_errorlog":
        observation = "error.log: [ERROR] Address already in use: 0.0.0.0:8080."
        state.logs_viewed = True
        reward = 0.1

    # 2. Fix Actions
    elif action == "unblock_port":
        if state.port_8080_blocked:
            state.port_8080_blocked = False
            observation = "Success: Process blocking port 8080 has been terminated."
            reward = 0.4
        else:
            observation = "Port 8080 is already clear."

    elif action == "clean_disk":
        state.disk_full = False
        observation = "Disk space cleared. 15GB now available."
        reward = 0.2

    # 3. Final Recovery Action
    elif action == "restart_service":
        if state.port_8080_blocked:
            observation = "Failure: Cannot start service. Port 8080 is blocked by another process."
            reward = -0.1 # Penalty for not diagnosing first
        else:
            state.service_running = True
            observation = "Success: Web-stack service is now running on port 8080."
            reward = 1.0 # The big win
            done = True

    else:
        observation = f"Command '{action}' not recognized."
        reward = -0.05

    return jsonify({
        "observation": observation,
        "reward": reward,
        "is_fixed": done,
        "step_count": state.steps_taken
    })

def main():
    # HF Spaces uses port 7860
    app.run(host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
