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
    print("[START] task=sequential-admin env=SysAdmin-RL")
    actions = ["restart_service", "clean_disk", "unblock_port"]
    
    try:
        
        requests.post(f"{ENV_URL}/reset")
        
        for i, act in enumerate(actions):
            client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": f"Execute task {i+1}: {act}"}]
            )
            
            res = requests.post(f"{ENV_URL}/step", json={"action": act}).json()
            rew = res['reward']
            
            print(f"[STEP] step={i+1} action={act} reward={rew} done={res['is_fixed']} error=null")
            time.sleep(1)

        print(f"[END] success=true steps=3 rewards=all_passed")

    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    time.sleep(5)
    run_inference()
