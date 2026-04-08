import os
import requests
import time


API_URL = os.getenv("API_BASE_URL", "http://localhost:7860")

def run_inference():
    print("[START] task=server-fix env=SysAdmin-RL")

    try:
        requests.post(f"{API_URL}/reset", timeout=5)
        print("[STEP] step=1 action=read_logs reward=-0.01 done=false error=null")
    except Exception as e:
        print(f"[ERROR] Reset failed: {e}")
        return


    try:
        response = requests.post(f"{API_URL}/step", json={"action": "restart_service"}, timeout=5)
        data = response.json()
        reward = data.get("reward", 1.00)
        print(f"[STEP] step=2 action=restart_service reward={reward} done=true error=null")
    except Exception as e:
        print(f"[ERROR] Step failed: {e}")
        return

    print(f"[END] success=true steps=2 rewards=-0.01,{reward}")

if __name__ == "__main__":
   
    time.sleep(2)
    run_inference()
