"""
Ops Agent MCP Server

Handles incident analysis and response with safety guardrails.
Demonstrates blocking of dangerous operations via Archestra guardrails.
"""

import json
import asyncio
from pathlib import Path
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types


# Initialize MCP server
app = Server("ops-agent")

# Load mock data
DATA_FILE = Path(__file__).parent / "incidents.json"

def load_incidents() -> dict[str, Any]:
    """Load mock incident data from JSON file"""
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def determine_root_cause(incident: dict) -> str:
    """Analyze symptoms to determine likely root cause"""
    symptoms = incident['symptoms'].lower()
    
    if "timeout" in symptoms:
        return "🔍 Database connection pool exhaustion - connections not being released properly"
    elif "corruption" in symptoms or "checksum" in symptoms:
        return "🔍 Disk I/O errors or hardware failure causing data integrity issues"
    elif "memory" in symptoms:
        return "🔍 Memory leak in worker code - objects not garbage collected"
    elif "cache" in symptoms:
        return "🔍 Cache invalidation issue or CDN configuration problem"
    else:
        return "🔍 Unknown - requires manual investigation"


def suggest_actions(incident: dict) -> list[str]:
    """Suggest remediation actions based on incident type"""
    symptoms = incident['symptoms'].lower()
    severity = incident['severity']
    
    actions = []
    
    if "timeout" in symptoms:
        actions.extend([
            "Increase database connection pool size to 200",
            "Restart database connection service",
            "Check for long-running queries in slow query log"
        ])
    elif "corruption" in symptoms:
        actions.extend([
            "Run database integrity check (CRITICAL - READ ONLY)",
            "Restore from last known good backup",
            "Alert database team for manual intervention"
        ])
    elif "memory" in symptoms:
        actions.extend([
            "Restart affected worker service",
            "Enable memory profiling for next 24h",
            "Review recent code changes in worker"
        ])
    elif "cache" in symptoms:
        actions.extend([
            "Clear CDN cache",
            "Verify cache configuration",
            "Check origin server response headers"
        ])
    else:
        actions.append("Escalate to on-call engineer")
    
    # Add monitoring for all incidents
    if severity in ["HIGH", "CRITICAL"]:
        actions.append("Set up real-time alerts for this service")
    
    return actions


async def analyze_incident(incident_id: str) -> str:
    """
    Analyze an incident and determine root cause
    
    Args:
        incident_id: The incident ID to analyze (e.g., INC-001)
        
    Returns:
        Detailed incident analysis with root cause and recommendations
    """
    data = load_incidents()
    
    incident = data['incidents'].get(incident_id)
    if not incident:
        return f"❌ Incident {incident_id} not found in the system"
    
    # Map severity to emoji
    severity_emojis = {
        "CRITICAL": "🔴",
        "HIGH": "🟠",
        "MEDIUM": "🟡",
        "LOW": "🟢"
    }
    severity_emoji = severity_emojis.get(incident['severity'], "⚪")
    
    # Determine root cause
    root_cause = determine_root_cause(incident)
    
    # Get recommended actions
    recommended_actions = suggest_actions(incident)
    
    analysis = f"""
🚨 **Incident Analysis: {incident['title']}**

**ID**: {incident_id}
**Severity**: {severity_emoji} {incident['severity']}
**Status**: {incident['status'].upper()}
**Created**: {incident['created_at'][:16].replace('T', ' ')}

**Affected Services**:
{chr(10).join(f'• {service}' for service in incident['affected_services'])}

**Impact**: {incident['impact']}

**Symptoms**:
{incident['symptoms']}

**Root Cause Analysis**:
{root_cause}

**Recommended Actions**:
{chr(10).join(f'{i+1}. {action}' for i, action in enumerate(recommended_actions))}
"""
    
    return analysis.strip()


async def execute_remediation(action: str) -> str:
    """
    Execute a remediation action (subject to guardrails)
    
    Args:
        action: The action to execute
        
    Returns:
        Result of the action execution
    """
    # This is where Archestra's guardrails will intercept dangerous actions
    # Before this code even runs, patterns like "delete prod database" will be blocked
    
    action_lower = action.lower()
    
    # Safe actions (allowed)
    if "restart" in action_lower and "service" in action_lower:
        return f"✅ **Action Executed**: {action}\n\n🔄 Service restarted successfully. Monitoring for stability..."
    
    elif "increase" in action_lower and ("pool" in action_lower or "limit" in action_lower):
        return f"✅ **Configuration Updated**: {action}\n\n⚙️  Settings applied. New connections being established..."
    
    elif "enable" in action_lower or "set up" in action_lower:
        return f"✅ **Monitoring Enabled**: {action}\n\n📊 Alerts configured. You'll receive notifications if thresholds are exceeded."
    
    elif "clear" in action_lower and "cache" in action_lower:
        return f"✅ **Cache Cleared**: {action}\n\n🗑️  CDN cache purged. Fresh content will be served."
    
    elif "check" in action_lower or "verify" in action_lower:
        return f"✅ **Check Initiated**: {action}\n\n🔍 Verification in progress. Results will be logged."
    
    # Dangerous actions (should be caught by guardrails, but defensive check)
    elif "delete" in action_lower and ("prod" in action_lower or "database" in action_lower):
        return "🚫 **ACTION BLOCKED**: Destructive database operations require manual approval and are not allowed via automation."
    
    elif "drop" in action_lower:
        return "🚫 **ACTION BLOCKED**: Cannot drop tables or databases automatically. This requires manual intervention."
    
    elif "truncate" in action_lower:
        return "🚫 **ACTION BLOCKED**: Data truncation is not permitted via automated remediation."
    
    else:
        return f"⚠️  **Manual Action Required**: {action}\n\nThis action requires manual execution by an authorized engineer."


async def list_incidents(status: str = "open", limit: int = 5) -> str:
    """
    List incidents filtered by status
    
    Args:
        status: Filter by status (open, investigating, resolved, all)
        limit: Maximum number of incidents to return
        
    Returns:
        Formatted list of incidents
    """
    data = load_incidents()
    
    # Filter incidents
    incidents = []
    for inc_id, inc_data in data['incidents'].items():
        if status == "all" or inc_data['status'] == status:
            incidents.append({
                'id': inc_id,
                **inc_data
            })
    
    # Sort by creation time (most recent first)
    incidents.sort(key=lambda x: x['created_at'], reverse=True)
    incidents = incidents[:limit]
    
    if not incidents:
        return f"No incidents with status '{status}' found"
    
    severity_emojis = {
        "CRITICAL": "🔴",
        "HIGH": "🟠",
        "MEDIUM": "🟡",
        "LOW": "🟢"
    }
    
    output = f"🚨 **Incidents ({status.upper()})** - Showing {len(incidents)}\n\n"
    
    for inc in incidents:
        severity_emoji = severity_emojis.get(inc['severity'], "⚪")
        output += f"""{severity_emoji} **{inc['id']}**: {inc['title']}
   📊 Severity: {inc['severity']}
   📅 Created: {inc['created_at'][:10]}
   🎯 Services: {', '.join(inc['affected_services'])}
   💥 Impact: {inc['impact']}
   
"""
    
    return output.strip()


# Register tools
@app.list_tools()
async def list_tools() -> list[types.Tool]:
    """List available tools"""
    return [
        types.Tool(
            name="analyze_incident",
            description="Analyze an incident and determine root cause",
            inputSchema={
                "type": "object",
                "properties": {
                    "incident_id": {"type": "string", "description": "The incident ID (e.g., INC-001)"}
                },
                "required": ["incident_id"]
            }
        ),
        types.Tool(
            name="execute_remediation",
            description="Execute a remediation action (subject to guardrails)",
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {"type": "string", "description": "The action to execute"}
                },
                "required": ["action"]
            }
        ),
        types.Tool(
            name="list_incidents",
            description="List incidents filtered by status",
            inputSchema={
                "type": "object",
                "properties": {
                    "status": {"type": "string", "description": "Filter by status", "default": "open"},
                    "limit": {"type": "integer", "description": "Maximum results", "default": 5}
                }
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle tool calls"""
    if name == "analyze_incident":
        result = await analyze_incident(arguments["incident_id"])
    elif name == "execute_remediation":
        result = await execute_remediation(arguments["action"])
    elif name == "list_incidents":
        result = await list_incidents(arguments.get("status", "open"), arguments.get("limit", 5))
    else:
        raise ValueError(f"Unknown tool: {name}")
    
    return [types.TextContent(type="text", text=result)]


async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
