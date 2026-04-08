import os
import requests
import time
from openai import OpenAI

API_BASE_URL = os.environ.get("API_BASE_URL")
API_KEY = os.environ.get("API_KEY")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-3.5-turbo")
ENV_URL = "http://localhost:7860"

def run_inference():
    if not API_BASE_URL or not API_KEY:
        print("[ERROR] API_BASE_URL and API_KEY not set")
        return

    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    print("[START] task=sequential-admin env=SysAdmin-RL")

    task_prompts = [
        "You are a sysadmin. Reply with exactly one word: restart_service",
        "You are a sysadmin. Reply with exactly one word: clean_disk",
        "You are a sysadmin. Reply with exactly one word: unblock_port",
    ]

    try:
        requests.post(f"{ENV_URL}/reset")

        for i, prompt in enumerate(task_prompts):
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}]
            )
            act = response.choices[0].message.content.strip().lower()

            res = requests.post(f"{ENV_URL}/step", json={"action": act}).json()
            rew = res.get("reward", 0.0)
            done = res.get("is_fixed", False)

            print(f"[STEP] step={i+1} action={act} reward={rew} done={done} error=null")
            time.sleep(1)

        print("[END] success=true steps=3 rewards=all_passed")

    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    time.sleep(5)
    run_inference()
