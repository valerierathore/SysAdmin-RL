# SysAdmin-RL

A reinforcement learning environment for automated server maintenance, built for the Scaler Hackathon.

## Project Structure
- server/app.py: The Flask-based RL environment.
- inference.py: The baseline agent script using the LiteLLM proxy.
- openenv.yaml: OpenEnv specification file.
- Dockerfile: Container configuration for deployment.

## Setup
1. Install dependencies: pip install -r requirements.txt
2. Run the server: python server/app.py
3. Run inference: python inference.py
