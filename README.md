---
title: SysAdmin-RL
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# SysAdmin-RL: Automated IT Support Environment

This repository contains an OpenEnv-compatible environment for evaluating agentic troubleshooting capabilities in a Linux-style sysadmin scenario.

### Overview
The agent is tasked with restoring a downed web server. The environment requires the agent to:
1. **Analyze logs** (syslog/error.log) to identify root causes.
2. **Resolve conflicts** (addressing port 8080 blockage).
3. **Validate status** to ensure service recovery.

### Technical Setup
- **Framework:** Docker-based environment.
- **Port:** Running on `7860`.
- **Primary Logic:** Located in `server/app.py`.

### How to Validate
Run the `inference.py` script to initiate the agentic evaluation loop.
