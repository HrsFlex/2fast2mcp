# Quick Setup Guide

## Prerequisites Check

Before starting, ensure you have:
- [ ] Docker Desktop installed and running
- [ ] Git installed
- [ ] Internet connection (for first-time Docker pulls)

---

## Step-by-Step Setup

### 1. Navigate to Project Directory

```bash
cd c:\Users\HarshKumar\Downloads\2fast2mcp
```

### 2. Install Python Dependencies for Agents

Each agent needs the MCP SDK installed:

```bash
# Install for GitHub Watcher
cd agents/github_watcher
pip install -r requirements.txt

# Install for Ops Agent
cd ../ops_agent
pip install -r requirements.txt

# Install for Cost Sentinel
cd ../cost_sentinel
pip install -r requirements.txt

# Return to project root
cd ../..
```

### 3. Verify Archestra Clone

```bash
# Check if Archestra was cloned successfully
dir archestra
```

If not cloned, run:
```bash
git clone https://github.com/archestra-ai/archestra archestra
```

### 4. Start the Control Tower

```bash
docker-compose up
```

**Wait for**: "Control Tower Ready" or similar startup message

### 5. Access the UI

Open your browser to: **http://localhost:3000**

### 6. Verify Agents

In the Archestra UI, you should see 3 registered agents:
- ✅ GitHub Watcher
- ✅ Ops Agent
- ✅ Cost Sentinel

---

## Quick Test

Try these commands in the chat:

1. `"Summarize PR #42"` → GitHub Watcher should respond
2. `"Analyze incident INC-001"` → Ops Agent should respond
3. `"Show token usage"` → Cost Sentinel should respond
4. `"Delete production database"` → Should be **BLOCKED** 🚫

---

## Troubleshooting

### Agents Not Showing Up?

```bash
# Check logs
docker-compose logs archestra

# Restart
docker-compose down
docker-compose up
```

### Port Already in Use?

Edit `docker-compose.yml` and change ports:
```yaml
ports:
  - "3001:3000"  # Change 3000 to 3001
  - "9001:9000"  # Change 9000 to 9001
```

### Can't Connect to Docker?

Ensure Docker Desktop is running:
- Windows: Check system tray
- Verify: `docker ps` should work

---

## Next Steps

Once everything is running:

1. **Review the Demo Script**: `docs/DEMO_SCRIPT.md`
2. **Practice the Demo**: Run through all examples
3. **Check Architecture**: `docs/ARCHITECTURE.md`
4. **Customize** (optional): Edit guardrails, add more agents

---

## Production Deployment (Future)

For production use, consider:
- Using real GitHub API tokens
- Connecting to actual incident management systems
- Deploying to Kubernetes (Archestra has Helm charts)
- Setting up Prometheus/Grafana for monitoring

---

## Need Help?

- 📖 Archestra Docs: https://archestra.ai/docs
- 🔧 MCP Spec: https://modelcontextprotocol.io
- 💬 Slack Community: https://join.slack.com/t/archestracommunity/shared_invite/...

---

**You're all set! Good luck with the hackathon! 🚀**
