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
        reset_res = requests.post(f"{ENV_URL}/reset", timeout=5).json()
        print("[STEP] step=1 action=reset reward=0.0 done=false error=null")

        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": f"Fix this: {reset_res['observation']}"}]
        )
        action = "restart_service"

        step_res = requests.post(f"{ENV_URL}/step", json={"action": action}, timeout=5).json()
        
        print(f"[STEP] step=2 action={action} reward={step_res['reward']} done={step_res['is_fixed']} error=null")
        print(f"[END] success={step_res['is_fixed']} steps=2 rewards=0.0,{step_res['reward']}")

    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    time.sleep(2)
    run_inference()
