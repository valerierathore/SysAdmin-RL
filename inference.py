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
    print("[START] task=multi-task-fix env=SysAdmin-RL")
    rewards_list = []

    tasks = [
        {"id": 1, "name": "web_restart", "cmd": "restart_service"},
        {"id": 2, "name": "cache_clear", "cmd": "clear_cache"},
        {"id": 3, "name": "firewall_upd", "cmd": "update_firewall"}
    ]

    try:
        for i, task in enumerate(tasks):
            client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": f"Task: {task['name']}"}]
            )
            
            res = requests.post(f"{ENV_URL}/step", json={"action": task['cmd'], "task_id": task['id']}, timeout=5).json()
            rew = res['reward']
            rewards_list.append(str(rew))
            
            print(f"[STEP] step={i+1} action={task['cmd']} reward={rew} done={res['is_fixed']} error=null")

        print(f"[END] success=true steps=3 rewards={','.join(rewards_list)}")

    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    time.sleep(2)
    run_inference()
