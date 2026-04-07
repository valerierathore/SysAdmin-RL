import threading
from flask import Flask
import time


app = Flask(__name__)

@app.route('/')
def health_check():
    return "Environment is Live!"

def run_server():
   
    app.run(host="0.0.0.0", port=7860)
import random
from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field


class SupportAction(BaseModel):
    command: Literal["read_log", "list_files", "restart_service", "check_status"]
    target: str = Field(..., description="The file path or service name")

class SupportObservation(BaseModel):
    output: str
    is_fixed: bool
    reward: float
    description: str

class SupportState(BaseModel):
    service_status: str = "down"
    diagnosed: bool = False
    steps_taken: int = 0


class SupportEnv:
    def __init__(self):
        self.state = SupportState()
        # The "hidden" clues the AI must find
        self.logs = {
            "syslog": "System boot... OK. Service 'web_server' failed to bind to port 8080.",
            "config.conf": "PORT=8080; SSL=TRUE; TIMEOUT=30",
            "auth.log": "User 'admin' logged in from 192.168.1.1",
            "error.log": "CRITICAL: Port 8080 is already in use by process ID 442."
        }

    def reset(self) -> SupportObservation:
        """Resets the environment to the starting broken state."""
        self.state = SupportState()
        return SupportObservation(
            output="Terminal initialized. System alert: 'web_server' is unresponsive.",
            is_fixed=False,
            reward=0.0,
            description="Fix the web_server to win."
        )

    def step(self, action: SupportAction) -> SupportObservation:
        """Processes one action from the AI agent."""
        self.state.steps_taken += 1
        output = ""
        reward = -0.01  # Small penalty for every move to encourage speed
        
        if action.command == "read_log":
            output = self.logs.get(action.target, "File not found.")
            # Logic: If they read a log mentioning the port, they 'diagnosed' the issue
            if "8080" in output:
                self.state.diagnosed = True
        
        elif action.command == "list_files":
            output = ", ".join(self.logs.keys())
            
        elif action.command == "check_status":
            output = f"Service '{action.target}' status: {self.state.service_status}."
            
        elif action.command == "restart_service":
            if action.target == "web_server":
                # They can ONLY succeed if they found the error in the logs first
                if self.state.diagnosed:
                    self.state.service_status = "up"
                    output = "SUCCESS: 'web_server' restarted on port 8080."
                    reward = 1.0
                else:
                    output = "FAILED: Process conflict. (You haven't identified the cause in the logs yet)."
                    reward = -0.2

        is_fixed = (self.state.service_status == "up")
        
        return SupportObservation(
            output=output,
            is_fixed=is_fixed,
            reward=reward,
            description="System restored!" if is_fixed else "Keep investigating."
        )


import threading
from flask import Flask
import time

# --- ADD THIS PART FOR HUGGING FACE ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "SysAdmin-RL Environment is Running!"

def run_server():
    # Hugging Face needs a server on port 7860 to show a green "Running" status
    app.run(host="0.0.0.0", port=7860)

if __name__ == "__main__":
    
    threading.Thread(target=run_server, daemon=True).start()
    
  
    env = SupportEnv()
    obs = env.reset()
    print(f"START: {obs.output}")
    
    print("\n--- Running Automated Test ---")
    print(env.step(SupportAction(command="list_files", target="")).output)
    print(env.step(SupportAction(command="read_log", target="syslog")).output)
    final_obs = env.step(SupportAction(command="restart_service", target="web_server"))
    
    print(f"RESULT: {final_obs.output} | Fixed: {final_obs.is_fixed}")
    print("Environment is now live. Waiting for evaluation...")

 
    while True:
        time.sleep(10)