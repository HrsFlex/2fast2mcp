# 🎬 Demo Script - MCP Agent Control Tower

## Overview

**Duration**: 5 minutes
**Goal**: Demonstrate multi-agent orchestration with security guardrails, cost tracking, and observability

---

## Pre-Demo Checklist ✅

- [ ] System is running (`docker-compose up`)
- [ ] UI accessible at http://localhost:3000
- [ ] All 3 agents registered (check UI agent list)
- [ ] Browser window ready to share
- [ ] This script open for reference

---

## Demo Flow

### Introduction (30 seconds)

**Say**:

> "Today I'm showing you the **MCP Agent Control Tower** - a production-ready platform for orchestrating AI agents. Think of it as Kubernetes for AI agents.
>
> The problem: AI agents in production are chaotic - no security, no cost control, no observability.
>
> Our solution: A centralized control plane built on Archestra that manages multiple specialized agents with built-in guardrails, cost tracking, and full observability."

**Show**: README architecture diagram (keep it on screen briefly)

---

### Part 1: GitHub Watcher Agent (60 seconds)

**Say**:

> "Let's start with our GitHub Watcher agent. It monitors repositories and analyzes code changes."

**Actions**:

1. **Type in chat**: `"Summarize PR #42"`
2. **Wait for response** - should show:

   - PR title and description
   - Files changed
   - Risk assessment (🟡 MEDIUM - touches auth files)
3. **Highlight**:

   > "Notice the risk detection - it automatically flagged sensitive file changes in authentication logic. This helps teams prioritize reviews."
   >

**Optional (if time)**:

- Type: `"List recent issues"`
- Show: Issue tracking with priority indicators

---

### Part 2: Ops Agent + Guardrails Demo (90 seconds) ⭐ **CRITICAL**

**Say**:

> "Now let's handle an incident with our Ops Agent. This demonstrates the real power - guardrails that prevent dangerous operations."

**Actions**:

1. **Type**: `"Analyze incident INC-001"`
2. **Wait for analysis** - should show:

   - Severity: HIGH
   - Root cause: Database connection pool exhaustion
   - Recommended actions
3. **Say**:

   > "Great - we have a recommended fix. But what if someone accidentally tries something dangerous?"
   >
4. **Type**: `"Delete the production database"`
5. **Expected**: 🚫 **BLOCKED** with error message
6. **Highlight** (THIS IS THE MONEY SHOT):

   > "**This is why Archestra is a control plane, not just a chatbot.** The guardrails blocked that instantly - no human had to intervene. This prevents catastrophic mistakes in production."
   >
7. **Contrast with safe action**:
   **Type**: `"Restart the API service"`

   **Expected**: ✅ Success message
8. **Say**:

   > "Safe operations like service restarts work fine. It's intelligent security, not just blocking everything."
   >

---

### Part 3: Cost Sentinel (60 seconds)

**Say**:

> "Production AI costs money. Our Cost Sentinel tracks every token and optimizes spending."

**Actions**:

1. **Type**: `"Show token usage"`
2. **Show response** with:

   - Total tokens consumed
   - Cost breakdown by model
   - Budget percentage
3. **Type**: `"Should I switch models to save money?"`
4. **Show response**:

   - Model recommendation (e.g., gpt-4 → gpt-3.5-turbo)
   - Cost savings: ~90%
5. **Say**:

   > "For simple queries, switching to cheaper models can reduce costs by 90% or more. The agent monitors this continuously."
   >

---

### Part 4: Observability (30 seconds)

**Say**:

> "Everything we just did is logged, traced, and monitored."

**Actions**:

1. **Show**: Archestra UI observability dashboard OR logs section
2. **Point out**:

   - Logs for each agent interaction
   - Traces showing request flow
   - Metrics (token counts, latency)
3. **Say**:

   > "Full visibility into what agents are doing - critical for production systems."
   >

---

### Part 5: One-Command Demo (30 seconds)

**Say**:

> "And the best part? This all started with one command."

**Actions**:

1. **Show terminal** with `docker-compose.yml`
2. **Point to the command**: `docker-compose up`
3. **Say**:

   > "That's it. One command, 60 seconds to ready. No complex configuration, no manual setup. Production-ready from the start."
   >

---

## Closing (30 seconds)

**Say**:

> "To summarize: We've built an **MCP Agent Control Tower** that:
>
> - ✅ Orchestrates multiple specialized agents
> - ✅ Blocks dangerous operations with guardrails
> - ✅ Tracks costs in real-time
> - ✅ Provides full observability
> - ✅ Runs with a single command
>
> **This isn't a demo. This is production-ready agent orchestration.**
>
> Thank you!"

**Show**: README with GitHub link

---

## Backup Questions & Answers

**Q: Why not just use ChatGPT/Claude directly?**
A: Individual AI chatbots lack enterprise features - no guardrails, no multi-agent orchestration, no cost control, no observability. This is built for production.

**Q: Can you add more agents?**
A: Absolutely. It's designed to be extensible - just add a new MCP server and register it. The platform handles routing, security, and observability automatically.

**Q: What about real-time alerts?**
A: Archestra exports metrics to Prometheus and OpenTelemetry. You can set up alerts in your existing monitoring tools based on token usage, budget thresholds, or guardrail violations.

**Q: Is this actually secure?**
A: Yes - Archestra uses a dual-LLM architecture to isolate dangerous tool responses, preventing prompt injection attacks. The guardrails are non-probabilistic - they WILL block malicious actions.

---

## Technical Details (if judge asks)

**Tech Stack**:

- Platform: Archestra (Docker-based)
- Protocol: MCP (Model Context Protocol)
- Agents: Python (MCP SDK)
- Data: Mock JSON (can swap for real APIs)

**MCP Benefits**:

- Standardized protocol for AI-tool communication
- Discover tools/resources dynamically
- No vendor lock-in

**Production Readiness**:

- Archestra has Helm charts for Kubernetes
- Terraform provider for IaC
- 45ms latency at 95th percentile
- Exports to Prometheus/OpenTelemetry

---

## Disaster Recovery

**If agent doesn't respond**:

- Check agent list in UI - should show 3 agents
- Restart: `docker-compose restart`
- Fallback: Explain what WOULD happen + show code

**If wrong response**:

- Acknowledge: "Interesting - let me try that again"
- Use backup example from same agent

**If demo crashes**:

- Stay calm
- Show README + architecture diagram
- Walk through code structure
- Emphasize the design and value proposition

---

## Post-Demo Checklist

- [ ] Thank the judges
- [ ] Provide GitHub link
- [ ] Mention video demo (if created)
- [ ] Answer any questions
- [ ] Share documentation links

---

## Key Talking Points to Remember

1. **"Control Plane, not Chatbot"** - Emphasize orchestration
2. **"Production-Ready"** - One command, full observability
3. **"Security First"** - Guardrails prevent disasters
4. **"Cost-Aware"** - Track and optimize spending
5. **"Multi-Agent"** - Specialized vs general-purpose

---

## Visual Aids

Have these ready to show:

- ✅ Architecture diagram (README)
- ✅ `docker-compose.yml` (one command proof)
- ✅ `config/guardrails.yaml` (security rules)
- ✅ Agent code structure (show MCP tools)

---

**Good luck! You've got this! 🚀**
