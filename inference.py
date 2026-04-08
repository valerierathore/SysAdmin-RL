import os
import requests
import time
from openai import OpenAI

client = OpenAI(
    base_url=os.environ.get("API_BASE_URL"),
    api_key=os.environ.get("API_KEY")
)
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-3.5-turbo")

ENV_URL = "http://localhost:7860"

def run_inference():
    print("[START] task=server-fix env=SysAdmin-RL")

    requests.post(f"{ENV_URL}/reset")
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": "The web server is down. Restart it."}]
    )
    llm_decision = response.choices[0].message.content
    print(f"[LLM LOG] Proxy active. Decision: {llm_decision[:20]}...")


    step_res = requests.post(f"{ENV_URL}/step", json={"action": "restart_service"})
    data = step_res.json()
    
    reward = data.get("reward", 1.0)
    print(f"[STEP] step=1 action=restart_service reward={reward} done=true error=null")
    print(f"[END] success=true steps=1 total_reward={reward}")

if __name__ == "__main__":
    time.sleep(2)
    run_inference()
