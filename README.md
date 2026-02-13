# 🏎️ MCP Agent Control Tower

> **A centralized control plane to run, observe, secure, and orchestrate MCP-based agents in real time.**

[![Archestra](https://img.shields.io/badge/Powered%20by-Archestra-blue)](https://archestra.ai)
[![MCP](https://img.shields.io/badge/Protocol-MCP-green)](https://modelcontextprotocol.io)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 🎯 Problem

AI agents are powerful but chaotic in production:
- ❌ **No centralized management** - each agent runs in isolation
- ❌ **Security risks** - prompt injection, data exfiltration vulnerabilities
- ❌ **Uncontrolled costs** - no visibility into token consumption
- ❌ **Zero observability** - can't trace or debug agent actions

---

## 💡 Solution

**MCP Agent Control Tower** - Think "Kubernetes for AI Agents"

A production-ready orchestration platform built on [Archestra](https://archestra.ai), the enterprise MCP platform.

### Key Features ✨

✅ **Multi-Agent Orchestration** - 3 specialized agents working in harmony  
✅ **Security Guardrails** - Blocks dangerous operations automatically  
✅ **Cost Optimization** - Real-time tracking with model switching  
✅ **Full Observability** - Logs, traces, and metrics out-of-the-box  
✅ **One-Command Setup** - Production-ready in < 60 seconds  

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────┐
│  👤 Chat UI (Archestra)                 │
│  Unified interface for all agents       │
└─────────────┬────────────────────────────┘
              │
┌─────────────▼────────────────────────────┐
│  🎛️  Archestra Control Plane            │
│  • Agent Routing                         │
│  • Guardrails Enforcement                │
│  • Cost Tracking                         │
│  • Observability (Logs/Traces/Metrics)   │
└─────────────┬────────────────────────────┘
              │
    ┌─────────┼─────────┐
    │         │         │
┌───▼───┐ ┌──▼────┐ ┌─▼──────┐
│GitHub │ │  Ops  │ │  Cost  │
│Watcher│ │ Agent │ │Sentinel│
└───────┘ └───────┘ └────────┘
```

---

## 🤖 Agents

### 1. 📋 GitHub Watcher
**Purpose**: Repository monitoring and code analysis

**Capabilities**:
- ✅ Summarize pull requests with risk assessment
- ✅ Analyze code diffs for sensitive changes
- ✅ List and track issues
- ✅ Detect risky patterns (auth, config, database changes)

**Example**: *"Summarize PR #42"*

---

### 2. 🚨 Ops Agent
**Purpose**: Incident response with safety guardrails

**Capabilities**:
- ✅ Analyze incidents and determine root cause
- ✅ Recommend remediation actions
- ✅ Execute safe operations (restarts, config updates)
- ✅ **BLOCK** dangerous operations (database deletion, data truncation)

**Example**: *"Analyze incident INC-001"*  
**Guardrail Demo**: *"Delete the production database"* → 🚫 **BLOCKED**

---

### 3. 💰 Cost Sentinel
**Purpose**: Token tracking and cost optimization

**Capabilities**:
- ✅ Monitor token usage across models
- ✅ Track spending against budget limits
- ✅ Alert when nearing budget threshold
- ✅ Recommend model switching (GPT-4 → GPT-3.5) for 90%+ savings

**Example**: *"Show token usage"*

---

## 🚀 Quickstart

### Prerequisites
- Docker Desktop installed
- Git

### Setup (< 2 minutes)

**1. Clone the repository**
```bash
git clone <your-repo-url>
cd 2fast2mcp
```

**2. Start the Control Tower**
```bash
docker-compose up
```

**3. Access the Chat UI**
- Open http://localhost:3000
- Start chatting with agents! 🎉

---

## 🎬 Demo

### Try These Examples:

#### GitHub Watcher:
```
"Summarize PR #42"
"List recent issues"
"Analyze code diff for PR #44"
```

#### Ops Agent:
```
"Analyze incident INC-001"
"What should I do about the database timeout?"
"Execute: Restart the API service"
```

#### Guardrails Demo (⚠️ This is BLOCKED):
```
"Delete the production database"
→ 🚫 Destructive database operations are not allowed
```

#### Cost Sentinel:
```
"Show me token usage"
"Am I over budget?"
"Recommend a cheaper model for simple tasks"
```

---

## ✨ Why Archestra?

| Feature | Description |
|---------|-------------|
| **MCP-Native** | Built specifically for Model Context Protocol |
| **Security** | Guardrails + prompt injection prevention |
| **Observability** | Logs, traces, metrics automatically exported |
| **Cost Control** | Dynamic model switching + budget enforcement |
| **Production-Ready** | Docker, Kubernetes, Terraform support |
| **Fast** | 45ms latency at 95th percentile |

---

## 📊 Features Showcase

### 🛡️ Security Guardrails ✅

Our Ops Agent demonstrates production-grade security:

```yaml
guardrails:
  - Block destructive database operations
  - Prevent data exfiltration
  - Require approval for risky actions
  - Log every agent action
```

**Live Demo**: Try typing *"delete prod database"* - it will be blocked instantly!

---

### 📈 Observability

Full visibility into agent behavior:
- ✅ **Logs**: Every tool call and response
- ✅ **Traces**: End-to-end request flow
- ✅ **Metrics**: Token usage, latency, costs

Access the dashboard at: http://localhost:9000/observability

---

### 💰 Cost Optimization

Cost Sentinel tracks spending and suggests optimizations:

```
Current Model: gpt-4 ($0.03/1K tokens)
Recommended: gpt-4o-mini ($0.00015/1K tokens)
Savings: 99.5% 💰
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Platform** | Archestra (MCP orchestration) |
| **Protocol** | Model Context Protocol (MCP) |
| **Agents** | Python (MCP SDK) |
| **Deployment** | Docker Compose |
| **Data** | Mock JSON files (MVP) |

---

## 📁 Project Structure

```
2fast2mcp/
├── agents/                       # Custom MCP servers
│   ├── github_watcher/
│   │   ├── server.py            # GitHub agent
│   │   ├── mock_data.json       # Sample PRs/issues
│   │   └── requirements.txt
│   ├── ops_agent/
│   │   ├── server.py            # Ops incident agent
│   │   ├── incidents.json       # Mock incidents
│   │   └── requirements.txt
│   └── cost_sentinel/
│       ├── server.py            # Cost tracking agent
│       └── requirements.txt
├── config/                       # Archestra configuration
│   ├── archestra.yaml           # Platform settings
│   ├── guardrails.yaml          # Security rules
│   └── agents.yaml              # Agent registry
├── docs/                         # Documentation
│   ├── ARCHITECTURE.md
│   └── DEMO_SCRIPT.md
├── docker-compose.yml            # One-command deployment
└── README.md                     # You are here! 👋
```

---

## 🏆 Hackathon Highlights

What makes this project special:

✨ **Production-Ready**: Not just a demo - uses enterprise platform (Archestra)  
✨ **Multi-Agent**: 3 specialized agents with distinct capabilities  
✨ **Security-First**: Guardrails prevent dangerous operations  
✨ **Observable**: Full visibility into agent behavior  
✨ **Cost-Aware**: Tracks spending and optimizes models automatically  
✨ **One Command**: `docker-compose up` → ready in 60 seconds  

---

## 🎯 Use Cases

### For DevOps Teams:
- Monitor GitHub activity automatically
- Analyze incidents with AI-powered root cause analysis
- Safe remediation with guardrails

### For Finance/Management:
- Track AI costs in real-time
- Enforce budget limits
- Optimize model selection for cost savings

### For Security Teams:
- Block dangerous operations
- Prevent data exfiltration
- Audit all agent actions

---

## 🔧 Advanced Configuration

### Custom Guardrails

Edit `config/guardrails.yaml` to add your own security rules:

```yaml
guardrails:
  - name: "Your Custom Rule"
    rules:
      - pattern: "dangerous.*action"
        action: BLOCK
        message: "🚫 This action is not allowed"
```

### Adding More Agents

1. Create new agent directory under `agents/`
2. Implement MCP server using Python SDK
3. Register in `config/agents.yaml`
4. Restart: `docker-compose restart`

---

## 📝 Development

### Running Agents Locally (without Docker)

```bash
cd agents/github_watcher
pip install -r requirements.txt
python server.py
```

### Testing Individual Tools

```bash
# Test GitHub agent
echo '{"method":"summarize_pr","params":{"pr_number":42}}' | python agents/github_watcher/server.py
```

---

## 🐛 Troubleshooting

**Agents not showing up?**
- Check `docker-compose logs archestra`
- Verify agent paths in `config/agents.yaml`

**Can't access UI?**
- Ensure ports 3000 and 9000 are not in use
- Try: `docker-compose down && docker-compose up`

**Mock data not loading?**
- Verify JSON files are valid
- Check file permissions

---

## 🤝 Contributing

This is a hackathon project, but we welcome contributions!

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 👏 Acknowledgments

- **Archestra** - MCP-native Secure AI Platform ([archestra.ai](https://archestra.ai))
- **Anthropic** - Model Context Protocol specification
- **Hackathon Organizers** - For this awesome opportunity!

---

## 📚 Learn More

- [Archestra Documentation](https://archestra.ai/docs)
- [MCP Specification](https://modelcontextprotocol.io)
- [Our Architecture Docs](docs/ARCHITECTURE.md)
- [Demo Script](docs/DEMO_SCRIPT.md)

---

<div align="center">

**Built with ❤️ for the MCP Hackathon**

⭐ Star this repo if you found it helpful!

</div>
