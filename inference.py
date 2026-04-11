import os
import requests
import time
from openai import OpenAI

# Configuration
API_BASE_URL = os.environ.get("API_BASE_URL")
API_KEY = os.environ.get("API_KEY")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-4o") # Or your specific model
ENV_URL = "http://localhost:7860"

def run_inference():
    if not API_BASE_URL or not API_KEY:
        print("[ERROR] API_BASE_URL and API_KEY not set")
        return

    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    
    # Critical: Start log must match the task and env exactly
    print("[START] task=sequential-admin env=SysAdmin-RL")

    try:
        # Step 0: Reset and get the initial state
        reset_req = requests.post(f"{ENV_URL}/reset")
        obs = reset_req.json().get("observation", "System is down. Investigate the cause.")
        
        total_reward = 0.0
        max_steps = 5

        for i in range(max_steps):
            # Step 1: Let the AI actually THINK based on the observation
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a SysAdmin. Available actions: read_syslog, read_errorlog, unblock_port, restart_service. "
                                   "Analyze logs and fix the service. Reply with ONLY the action name."
                    },
                    {"role": "user", "content": f"Observation: {obs}"}
                ],
                temperature=0.0
            )

            action = response.choices[0].message.content.strip().lower()

            # Step 2: Send the AI's chosen action to your environment
            res = requests.post(f"{ENV_URL}/step", json={"action": action}).json()
            
            # Step 3: Parse the environment's response
            obs = res.get("observation", "No observation provided")
            reward = float(res.get("reward", 0.0))
            done = res.get("is_fixed", False)
            total_reward += reward

            # Step 4: Mandatory [STEP] log for the grader
            print(f"[STEP] step={i+1} action={action} reward={reward} done={done} error=null")

            if done:
                break
            
            time.sleep(1)

        # Step 5: Final [END] log
        success = "true" if total_reward > 0 else "false"
        print(f"[END] success={success} steps={i+1} rewards={total_reward}")

    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    # Wait for the server (app.py) to fully boot up
    time.sleep(10)
    run_inference() 
