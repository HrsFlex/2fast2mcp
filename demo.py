"""
Demo script showing agent functionality with mock data
This simulates what the agents will do when called through MCP
"""

import json
import asyncio
from pathlib import Path

# -----------------------------------------------------------------------------
# GITHUB WATCHER Demo
# -----------------------------------------------------------------------------

def demo_github_watcher():
    print("\n" + "=" * 70)
    print("📋 GITHUB WATCHER AGENT DEMO")
    print("=" * 70 + "\n")
    
    # Load data
    with open("agents/github_watcher/mock_data.json", 'r') as f:
        data = json.load(f)
    
    # Demo 1: Summarize PR #42
    print("🔍 Demo 1: Summarize PR #42")
    print("-" * 70)
    pr = next((p for p in data['pull_requests'] if p['number'] == 42), None)
    if pr:
        print(f"📋 **PR #{pr['number']}: {pr['title']}**")
        print(f"👤 **Author**: {pr['author']}")
        print(f"🏷️  **Labels**: {', '.join(pr['labels'])}")
        print(f"\n📝 **Description**:")
        print(f"{pr['description']}")
        print(f"\n📊 **Changes**: +{pr['additions']} / -{pr['deletions']}")
        
        # Risk assessment
        has_auth = any('auth' in f.lower() for f in pr['files_changed'])
        has_config = any('config' in f.lower() for f in pr['files_changed'])
        if has_auth or has_config:
            print(f"\n⚠️  **Risk**: 🟡 MEDIUM - Touches authentication/config files")
        else:
            print(f"\n⚠️  **Risk**: 🟢 LOW - Standard code changes")
    
    # Demo 2: List Recent Issues
    print("\n\n🔍 Demo 2: List Recent Issues")
    print("-" * 70)
    for issue in data['issues'][:3]:
        priority = "🔥" if "high-priority" in issue['labels'] else "📌"
        print(f"{priority} **#{issue['number']}**: {issue['title']}")
        print(f"   🏷️  {', '.join(issue['labels'])}")
        print()


# -----------------------------------------------------------------------------
# OPS AGENT Demo
# -----------------------------------------------------------------------------

def demo_ops_agent():
    print("\n" + "=" * 70)
    print("🚨 OPS AGENT DEMO")
    print("=" * 70 + "\n")
    
    # Load data
    with open("agents/ops_agent/incidents.json", 'r') as f:
        data = json.load(f)
    
    # Demo 1: Analyze Incident
    print("🔍 Demo 1: Analyze Incident INC-001")
    print("-" * 70)
    inc = data['incidents']['INC-001']
    severity_emojis = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}
    
    print(f"🚨 **{inc['title']}**")
    print(f"**Severity**: {severity_emojis[inc['severity']]} {inc['severity']}")
    print(f"**Status**: {inc['status'].upper()}")
    print(f"\n**Affected Services**:")
    for svc in inc['affected_services']:
        print(f"  • {svc}")
    print(f"\n**Symptoms**: {inc['symptoms']}")
    
    # Root cause
    if "timeout" in inc['symptoms'].lower():
        print(f"\n**Root Cause**: 🔍 Database connection pool exhaustion")
        print(f"\n**Recommended Actions**:")
        print(f"  1. Increase database connection pool size to 200")
        print(f"  2. Restart database connection service")
        print(f"  3. Check for long-running queries")
    
    # Demo 2: Guardrail Test
    print("\n\n🔍 Demo 2: Execute Remediation (Safe)")
    print("-" * 70)
    action = "Restart API service"
    print(f"Action: {action}")
    print(f"✅ **Action Executed**: {action}")
    print(f"🔄 Service restarted successfully. Monitoring for stability...")
    
    print("\n\n🔍 Demo 3: Execute Remediation (BLOCKED) 🚫")
    print("-" * 70)
    dangerous_action = "Delete production database"
    print(f"Action: {dangerous_action}")
    print(f"🚫 **ACTION BLOCKED**: Destructive database operations are not allowed!")
    print(f"   This demonstrates security guardrails in action.")


# -----------------------------------------------------------------------------
# COST SENTINEL Demo
# -----------------------------------------------------------------------------

def demo_cost_sentinel():
    print("\n" + "=" * 70)
    print("💰 COST SENTINEL AGENT DEMO")
    print("=" * 70 + "\n")
    
    # Create tracker
    class MockCostTracker:
        def __init__(self):
            self.usage = {
                "gpt-4": {"tokens": 15000, "cost": 0.45},
                "gpt-3.5-turbo": {"tokens": 5000, "cost": 0.0075},
                "gpt-4o-mini": {"tokens": 8000, "cost": 0.0012}
            }
            self.total_tokens = 28000
            self.total_cost = 0.4587
            self.budget_limit = 100.0
    
    tracker = MockCostTracker()
    
    # Demo 1: Token Usage
    print("🔍 Demo 1: Get Token Usage")
    print("-" * 70)
    print(f"💰 **Cost Sentinel Report**\n")
    print(f"📊 **Total Usage**:")
    print(f"   • Total Tokens: {tracker.total_tokens:,}")
    print(f"   • Total Cost: ${tracker.total_cost:.2f}")
    print(f"   • Budget: ${tracker.budget_limit:.2f}")
    print(f"   • Remaining: ${tracker.budget_limit - tracker.total_cost:.2f}")
    
    percentage = (tracker.total_cost / tracker.budget_limit) * 100
    print(f"\n📈 **Budget Status**: {percentage:.1f}% used")
    print(f"✅ Budget healthy")
    
    print(f"\n📋 **Usage by Model**:")
    for model, data in tracker.usage.items():
        print(f"   • {model}: {data['tokens']:,} tokens (${data['cost']:.4f})")
    
    # Demo 2: Model Recommendation
    print("\n\n🔍 Demo 2: Recommend Model Switch for Simple Tasks")
    print("-" * 70)
    print(f"💡 **Model Recommendation for SIMPLE Complexity**")
    print(f"\n🎯 **Recommended Model**: gpt-4o-mini")
    print(f"📝 **Reason**: Simple queries don't need expensive models")
    
    gpt4_cost = 10000 * 0.03 / 1000
    mini_cost = 10000 * 0.00015 / 1000
    savings = gpt4_cost - mini_cost
    savings_pct = (savings / gpt4_cost) * 100
    
    print(f"\n💰 **Cost Analysis** (per 10K tokens):")
    print(f"   • Current (gpt-4): ${gpt4_cost:.4f}")
    print(f"   • Recommended (gpt-4o-mini): ${mini_cost:.4f}")
    print(f"   • **Savings**: ${savings:.4f} ({savings_pct:.1f}% reduction)")
    
    print(f"\n✨ **Best For**:")
    print(f"   • basic Q&A")
    print(f"   • simple summaries")
    print(f"   • formatting")


# -----------------------------------------------------------------------------
# Main Demo runner
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🏎️  MCP AGENT CONTROL TOWER - LIVE DEMO")
    print("=" * 70)
    
    print("\n📌 This demo simulates what the agents will do when deployed")
    print("📌 All data is from mock files - ready for Archestra integration")
    
    demo_github_watcher()
    demo_ops_agent()
    demo_cost_sentinel()
    
    print("\n" + "=" * 70)
    print("✅ DEMO COMPLETE")
    print("=" * 70)
    
    print("\n🚀 Next Steps:")
    print("   1. Run: docker-compose up")
    print("   2. Access: http://localhost:3005")
    print("   3. Try these commands in the Chat UI!")
    print("\n" + "=" * 70 + "\n")
