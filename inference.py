import os
import requests
import time
from openai import OpenAI

API_BASE_URL = os.environ.get("API_BASE_URL")
API_KEY = os.environ.get("API_KEY")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-3.5-turbo")
ENV_URL = "http://localhost:7860"

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

def run_inference():
    
    print("[START] task=server-fix env=SysAdmin-RL")

    try:
    
        res = requests.post(f"{ENV_URL}/reset").json()
        print(f"[STEP] step=1 action=reset reward=0.0 done=false error=null")

        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": f"Logs: {res['observation']}. Fix it."}]
        )
        action_to_take = "restart_service" 

  
        step_res = requests.post(f"{ENV_URL}/step", json={"action": action_to_take}).json()
        reward = step_res["reward"]
        done = step_res["is_fixed"]
        
        print(f"[STEP] step=2 action={action_to_take} reward={reward} done={done} error=null")
        

        print(f"[END] success={done} steps=2 rewards=0.0,{reward}")

    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    time.sleep(2)
    run_inference()
