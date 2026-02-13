"""
GitHub Watcher MCP Server

Provides tools and resources for analyzing GitHub repositories, PRs, and issues.
"""

import json
import asyncio
from pathlib import Path
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types


# Initialize MCP server
app = Server("github-watcher")

# Load mock data
DATA_FILE = Path(__file__).parent / "mock_data.json"

def load_data() -> dict[str, Any]:
    """Load mock GitHub data from JSON file"""
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def analyze_risk(files: list[str]) -> tuple[str, str]:
    """
    Analyze risk level based on file patterns
    
    Returns:
        tuple: (risk_emoji, risk_description)
    """
    risky_patterns = {
        'config': 'Configuration files',
        'env': 'Environment variables',
        'secret': 'Secrets/credentials',
        'auth': 'Authentication logic',
        'database': 'Database schema',
        'migration': 'Database migrations',
        '.yaml': 'Config files',
        '.yml': 'Config files'
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


async def summarize_pr(pr_number: int) -> str:
    """
    Summarize a pull request with risk assessment
    
    Args:
        pr_number: The PR number to summarize
        
    Returns:
        Formatted summary of the PR with risk analysis
    """
    data = load_data()
    
    pr = next((p for p in data['pull_requests'] if p['number'] == pr_number), None)
    if not pr:
        return f"❌ PR #{pr_number} not found in repository"
    
    # Analyze risk based on files changed
    risk_emoji, risk_desc = analyze_risk(pr['files_changed'])
    
    summary = f"""
📋 **PR #{pr['number']}: {pr['title']}**

👤 **Author**: {pr['author']}
📅 **Created**: {pr['created_at'][:10]}
🏷️  **Labels**: {', '.join(pr['labels'])}

📝 **Description**:
{pr['description']}

📂 **Files Changed**: {len(pr['files_changed'])} files
   • {chr(10).join(f"   - {f}" for f in pr['files_changed'][:5])}
   {'   ...' if len(pr['files_changed']) > 5 else ''}

📊 **Changes**: +{pr['additions']} / -{pr['deletions']}

⚠️  **Risk Assessment**: {risk_emoji} {risk_desc}
"""
    
    return summary.strip()


async def list_recent_issues(limit: int = 5) -> str:
    """
    List recent issues from the repository
    
    Args:
        limit: Maximum number of issues to return (default: 5)
        
    Returns:
        Formatted list of recent issues
    """
    data = load_data()
    issues = data['issues'][:limit]
    
    if not issues:
        return "No issues found in repository"
    
    output = f"📋 **Recent Issues** (showing {len(issues)} of {len(data['issues'])})\n\n"
    
    for issue in issues:
        priority_emoji = "🔥" if "high-priority" in issue['labels'] else "📌"
        status_emoji = "🔴" if issue['status'] == "open" else "🟡"
        
        output += f"""{priority_emoji} **#{issue['number']}**: {issue['title']}
   {status_emoji} Status: {issue['status'].title()}
   🏷️  Labels: {', '.join(issue['labels'])}
   👤 Author: {issue['author']}
   📅 Created: {issue['created_at'][:10]}
   
"""
    
    return output.strip()


async def analyze_code_diff(pr_number: int) -> str:
    """
    Analyze code changes in a PR for potential risks
    
    Args:
        pr_number: The PR number to analyze
        
    Returns:
        Risk analysis and recommendations
    """
    data = load_data()
    
    pr = next((p for p in data['pull_requests'] if p['number'] == pr_number), None)
    if not pr:
        return f"❌ PR #{pr_number} not found"
    
    risk_emoji, risk_desc = analyze_risk(pr['files_changed'])
    
    # Generate recommendations based on risk
    recommendations = []
    
    if any('auth' in f.lower() for f in pr['files_changed']):
        recommendations.append("🔒 Security review required - authentication logic modified")
    
    if any('database' in f.lower() or 'migration' in f.lower() for f in pr['files_changed']):
        recommendations.append("🗄️  Database review required - schema changes detected")
    
    if any('config' in f.lower() or '.yaml' in f or '.yml' in f for f in pr['files_changed']):
        recommendations.append("⚙️  Configuration review - ensure no secrets are committed")
    
    if pr['additions'] + pr['deletions'] > 500:
        recommendations.append("📏 Large changeset - consider breaking into smaller PRs")
    
    if not recommendations:
        recommendations.append("✅ Standard code review process")
    
    analysis = f"""
🔍 **Code Diff Analysis for PR #{pr_number}**

**Risk Level**: {risk_emoji} {risk_desc}

**Recommendations**:
{chr(10).join(f'• {rec}' for rec in recommendations)}

**Review Checklist**:
✓ Security implications reviewed
✓ Tests cover new changes
✓ Documentation updated
✓ Breaking changes documented
"""
    
    return analysis.strip()


async def get_repo_stats() -> str:
    """
    Get repository statistics
    
    Returns:
        JSON string with repository stats
    """
    data = load_data()
    stats = data['repository_stats']
    
    stats_text = f"""
⭐ **Repository Statistics**

• Stars: {stats['stars']}
• Forks: {stats['forks']}
• Contributors: {stats['contributors']}
• Open Issues: {stats['open_issues']}
• Open PRs: {stats['open_prs']}
• Primary Language: {stats['primary_language']}
"""
    
    return stats_text.strip()


async def get_recent_activity() -> str:
    """
    Get recent repository activity timeline
    
    Returns:
        Formatted timeline of recent events
    """
    data = load_data()
    
    # Combine PRs and issues and sort by date
    events = []
    
    for pr in data['pull_requests'][:3]:
        events.append({
            'type': 'PR',
            'date': pr['created_at'],
            'title': pr['title'],
            'number': pr['number'],
            'author': pr['author']
        })
    
    for issue in data['issues'][:3]:
        events.append({
            'type': 'Issue',
            'date': issue['created_at'],
            'title': issue['title'],
            'number': issue['number'],
            'author': issue['author']
        })
    
    # Sort by date (newest first)
    events.sort(key=lambda x: x['date'], reverse=True)
    
    activity = "📅 **Recent Activity**\n\n"
    
    for event in events[:5]:
        emoji = "🔀" if event['type'] == 'PR' else "📋"
        activity += f"{emoji} {event['date'][:10]} - {event['type']} #{event['number']}: {event['title']}\n"
        activity += f"   👤 {event['author']}\n\n"
    
    return activity.strip()


# Register tools and resources
@app.list_tools()
async def list_tools() -> list[types.Tool]:
    """List available tools"""
    return [
        types.Tool(
            name="summarize_pr",
            description="Summarize a pull request with risk assessment",
            inputSchema={
                "type": "object",
                "properties": {
                    "pr_number": {"type": "integer", "description": "The PR number to summarize"}
                },
                "required": ["pr_number"]
            }
        ),
        types.Tool(
            name="list_recent_issues",
            description="List recent issues from the repository",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Maximum number of issues", "default": 5}
                }
            }
        ),
        types.Tool(
            name="analyze_code_diff",
            description="Analyze code changes in a PR for potential risks",
            inputSchema={
                "type": "object",
                "properties": {
                    "pr_number": {"type": "integer", "description": "The PR number to analyze"}
                },
                "required": ["pr_number"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle tool calls"""
    if name == "summarize_pr":
        result = await summarize_pr(arguments["pr_number"])
    elif name == "list_recent_issues":
        result = await list_recent_issues(arguments.get("limit", 5))
    elif name == "analyze_code_diff":
        result = await analyze_code_diff(arguments["pr_number"])
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
