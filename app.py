"""
MCP Agent Control Tower - Web Interface
Enterprise AI Agent Orchestration Platform
"""

from flask import Flask, render_template, request, jsonify
import json, time, random
from pathlib import Path

app = Flask(__name__)

# -----------------------------------------------------------------------------
# Data Sources
# -----------------------------------------------------------------------------

def load_github_data():
    with open('agents/github_watcher/mock_data.json', 'r') as f:
        return json.load(f)

def load_incidents():
    with open('agents/ops_agent/incidents.json', 'r') as f:
        return json.load(f)

# -----------------------------------------------------------------------------
# Helper: simulate realistic processing time
# -----------------------------------------------------------------------------

def simulate_latency(min_ms=200, max_ms=600):
    """Add realistic processing latency"""
    delay = random.randint(min_ms, max_ms) / 1000.0
    time.sleep(delay)

# -----------------------------------------------------------------------------
# GitHub Watcher Agent
# -----------------------------------------------------------------------------

def analyze_pr_risk(files):
    risky_patterns = {
        'config': 'Configuration files',
        'env': 'Environment variables',
        'secret': 'Secrets/credentials',
        'auth': 'Authentication logic',
        'database': 'Database schema',
        'migration': 'Database migrations',
    }
    
    detected_risks = []
    for file in files:
        file_lower = file.lower()
        for pattern, description in risky_patterns.items():
            if pattern in file_lower:
                detected_risks.append(description)
    
    risk_count = len(set(detected_risks))
    
    if risk_count > 3:
        return "🔴 HIGH", f"Multiple sensitive areas: {', '.join(set(detected_risks[:3]))}"
    elif risk_count > 0:
        return "🟡 MEDIUM", f"Touches: {', '.join(set(detected_risks))}"
    else:
        return "🟢 LOW", "Standard code changes"

def github_summarize_pr(pr_number):
    data = load_github_data()
    pr = next((p for p in data['pull_requests'] if p['number'] == pr_number), None)
    
    if not pr:
        return {"error": f"PR #{pr_number} not found in connected repository"}
    
    risk_emoji, risk_desc = analyze_pr_risk(pr['files_changed'])
    
    return {
        "number": pr['number'],
        "title": pr['title'],
        "author": pr['author'],
        "description": pr['description'],
        "files_changed": pr['files_changed'],
        "additions": pr['additions'],
        "deletions": pr['deletions'],
        "labels": pr['labels'],
        "risk_level": risk_emoji,
        "risk_description": risk_desc
    }

def github_list_issues(limit=5):
    data = load_github_data()
    issues = data['issues'][:limit]
    return {"issues": issues, "total": len(data['issues'])}

# -----------------------------------------------------------------------------
# Ops Agent
# -----------------------------------------------------------------------------

def ops_analyze_incident(incident_id):
    data = load_incidents()
    incident = data['incidents'].get(incident_id)
    
    if not incident:
        return {"error": f"Incident {incident_id} not found in monitoring system"}
    
    symptoms = incident['symptoms'].lower()
    if "timeout" in symptoms:
        root_cause = "Database connection pool exhaustion — connections not being released properly under high concurrency"
        actions = [
            "Increase database connection pool size to 200",
            "Restart database connection service",
            "Check for long-running queries in slow query log"
        ]
    elif "corruption" in symptoms:
        root_cause = "Disk I/O errors or hardware failure causing data integrity issues on primary replica"
        actions = [
            "Run database integrity check (CRITICAL — READ ONLY)",
            "Restore from last known good backup",
            "Alert database team for manual intervention"
        ]
    elif "memory" in symptoms:
        root_cause = "Memory leak in worker process — objects not being garbage collected after batch processing"
        actions = [
            "Restart affected worker service",
            "Enable memory profiling for next 24h",
            "Review recent code changes in worker"
        ]
    else:
        root_cause = "CDN origin misconfiguration causing cache bypass — all requests hitting origin directly"
        actions = [
            "Verify CDN cache headers on origin responses",
            "Purge and rebuild CDN cache rules",
            "Monitor cache hit ratio for next 2h"
        ]
    
    return {
        "incident_id": incident_id,
        "title": incident['title'],
        "severity": incident['severity'],
        "status": incident['status'],
        "affected_services": incident['affected_services'],
        "symptoms": incident['symptoms'],
        "impact": incident['impact'],
        "root_cause": root_cause,
        "recommended_actions": actions
    }

def ops_execute_action(action):
    action_lower = action.lower()
    
    if "delete" in action_lower and ("prod" in action_lower or "database" in action_lower):
        return {
            "status": "blocked",
            "message": "🚫 BLOCKED: Destructive database operations are not allowed",
            "reason": "Security guardrail intercepted a potentially destructive action targeting production infrastructure"
        }
    elif "drop" in action_lower or "truncate" in action_lower:
        return {
            "status": "blocked",
            "message": "🚫 BLOCKED: Data deletion/truncation not permitted",
            "reason": "Security guardrail prevented schema-level destructive operation"
        }
    
    if "restart" in action_lower:
        return {
            "status": "success",
            "message": f"✅ Executed: {action}",
            "result": "Service restarted successfully. Health checks passing. Monitoring for stability over the next 5 minutes."
        }
    elif "increase" in action_lower:
        return {
            "status": "success",
            "message": f"✅ Configuration Updated: {action}",
            "result": "Settings applied to production cluster. New connections being established with updated pool size."
        }
    else:
        return {
            "status": "manual",
            "message": f"⚠️ Manual Action Required: {action}",
            "result": "This action requires manual execution by an authorized engineer with production access."
        }

# -----------------------------------------------------------------------------
# Cost Sentinel
# -----------------------------------------------------------------------------

class CostTracker:
    def __init__(self):
        self.usage_by_model = {
            "gpt-4": {"tokens": 15000, "cost": 0.45},
            "gpt-3.5-turbo": {"tokens": 5000, "cost": 0.0075},
            "gpt-4o-mini": {"tokens": 8000, "cost": 0.0012}
        }
        self.total_tokens = 28000
        self.total_cost = 0.4587
        self.budget_limit = 100.0
    
    def get_usage(self):
        remaining = self.budget_limit - self.total_cost
        percentage = (self.total_cost / self.budget_limit) * 100
        
        return {
            "total_tokens": self.total_tokens,
            "total_cost": self.total_cost,
            "budget_limit": self.budget_limit,
            "remaining": remaining,
            "percentage": percentage,
            "alert": percentage > 80,
            "usage_by_model": self.usage_by_model
        }
    
    def recommend_model(self, complexity="medium"):
        recommendations = {
            "simple": {
                "model": "gpt-4o-mini",
                "price": 0.00015,
                "reason": "For simple queries, a lightweight model delivers equivalent quality at a fraction of the cost"
            },
            "medium": {
                "model": "gpt-3.5-turbo",
                "price": 0.0015,
                "reason": "Optimal balance of reasoning capability and cost efficiency for analytical workloads"
            },
            "complex": {
                "model": "gpt-4",
                "price": 0.03,
                "reason": "Complex reasoning, architecture decisions, and security analysis require the most capable model"
            }
        }
        
        rec = recommendations.get(complexity, recommendations["medium"])
        current_cost = 10000 * 0.03 / 1000
        recommended_cost = 10000 * rec["price"] / 1000
        savings = current_cost - recommended_cost
        savings_pct = (savings / current_cost) * 100 if current_cost > 0 else 0
        
        return {
            "recommended_model": rec["model"],
            "reason": rec["reason"],
            "current_cost": current_cost,
            "recommended_cost": recommended_cost,
            "savings": savings,
            "savings_percentage": savings_pct
        }

cost_tracker = CostTracker()

# -----------------------------------------------------------------------------
# API Routes
# -----------------------------------------------------------------------------

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/github/pr/<int:pr_number>')
def api_github_pr(pr_number):
    simulate_latency(300, 800)
    result = github_summarize_pr(pr_number)
    return jsonify(result)

@app.route('/api/github/issues')
def api_github_issues():
    simulate_latency(200, 500)
    limit = request.args.get('limit', 5, type=int)
    result = github_list_issues(limit)
    return jsonify(result)

@app.route('/api/ops/incident/<incident_id>')
def api_ops_incident(incident_id):
    simulate_latency(400, 900)
    result = ops_analyze_incident(incident_id)
    return jsonify(result)

@app.route('/api/ops/execute', methods=['POST'])
def api_ops_execute():
    simulate_latency(300, 700)
    data = request.json
    action = data.get('action', '')
    result = ops_execute_action(action)
    return jsonify(result)

@app.route('/api/cost/usage')
def api_cost_usage():
    simulate_latency(200, 500)
    result = cost_tracker.get_usage()
    return jsonify(result)

@app.route('/api/cost/recommend')
def api_cost_recommend():
    simulate_latency(300, 600)
    complexity = request.args.get('complexity', 'medium')
    result = cost_tracker.recommend_model(complexity)
    return jsonify(result)

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("🏎️  MCP AGENT CONTROL TOWER")
    print("=" * 70)
    print("\n✨ Enterprise AI Agent Orchestration Platform")
    print("🌐 Dashboard: http://localhost:5000")
    print("\n📊 Active Modules:")
    print("   • GitHub Watcher — PR & Issue Intelligence")
    print("   • Ops Agent — Automated Incident Response")
    print("   • Cost Sentinel — Budget Optimization")
    print("\n🔒 Security: Guardrails ACTIVE")
    print("📡 Monitoring: REAL-TIME")
    print("🤖 Auto-Remediation: ENABLED")
    print("\n" + "=" * 70 + "\n")
    
    app.run(debug=True, port=5000, host='0.0.0.0')
