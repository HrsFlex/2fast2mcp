"""
Cost Sentinel MCP Server

Monitors token usage and manages cost optimization.
Tracks LLM consumption and recommends model switching for cost savings.
"""

import asyncio
from datetime import datetime
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types


# Initialize MCP server
app = Server("cost-sentinel")


# Simple in-memory cost tracker (resets on restart - good for MVP demo)
class CostTracker:
    """Tracks token usage and costs across different models"""
    
    def __init__(self):
        self.total_tokens = 0
        self.total_cost = 0.0
        self.budget_limit = 100.0  # USD
        
        # Model pricing per 1K tokens (input)
        self.model_pricing = {
            "gpt-4": 0.03,
            "gpt-4-turbo": 0.01,
            "gpt-3.5-turbo": 0.0015,
            "gpt-4o": 0.0025,
            "gpt-4o-mini": 0.00015,
            "claude-3-opus": 0.015,
            "claude-3-sonnet": 0.003,
            "claude-3-haiku": 0.00025
        }
        
        # Track usage by model
        self.usage_by_model = {}
        
        # Simulate some initial usage for demo purposes
        self._init_demo_data()
    
    def _init_demo_data(self):
        """Preload some demo usage data"""
        self.add_usage("gpt-4", 15000)
        self.add_usage("gpt-3.5-turbo", 5000)
        self.add_usage("gpt-4o-mini", 8000)
    
    def add_usage(self, model: str, tokens: int):
        """Add token usage for a specific model"""
        cost_per_token = (self.model_pricing.get(model, 0.01) / 1000)
        cost = tokens * cost_per_token
        
        self.total_tokens += tokens
        self.total_cost += cost
        
        if model not in self.usage_by_model:
            self.usage_by_model[model] = {"tokens": 0, "cost": 0.0}
        
        self.usage_by_model[model]["tokens"] += tokens
        self.usage_by_model[model]["cost"] += cost
    
    def get_budget_status(self) -> dict:
        """Get current budget status"""
        remaining = self.budget_limit - self.total_cost
        percentage = (self.total_cost / self.budget_limit) * 100
        
        return {
            "spent": self.total_cost,
            "remaining": max(0, remaining),
            "percentage": min(100, percentage),
            "alert": percentage > 80,
            "critical": percentage > 95
        }
    
    def calculate_savings(self, from_model: str, to_model: str, tokens: int) -> dict:
        """Calculate potential cost savings from switching models"""
        from_price = self.model_pricing.get(from_model, 0.01) / 1000
        to_price = self.model_pricing.get(to_model, 0.001) / 1000
        
        from_cost = tokens * from_price
        to_cost = tokens * to_price
        savings = from_cost - to_cost
        savings_pct = (savings / from_cost * 100) if from_cost > 0 else 0
        
        return {
            "from_cost": from_cost,
            "to_cost": to_cost,
            "savings": savings,
            "savings_percentage": savings_pct
        }


# Global tracker instance
tracker = CostTracker()


async def get_token_usage() -> str:
    """
    Get current token usage statistics
    
    Returns:
        Detailed breakdown of token usage and costs
    """
    status = tracker.get_budget_status()
    
    # Build usage breakdown by model
    model_breakdown = ""
    for model, data in tracker.usage_by_model.items():
        model_breakdown += f"\n   • {model}: {data['tokens']:,} tokens (${data['cost']:.2f})"
    
    report = f"""
💰 **Cost Sentinel Report**

📊 **Total Usage**:
   • Total Tokens: {tracker.total_tokens:,}
   • Total Cost: ${tracker.total_cost:.2f}
   • Budget: ${tracker.budget_limit:.2f}
   • Remaining: ${status['remaining']:.2f}

📈 **Budget Status**: {status['percentage']:.1f}% used
{"🔴 **ALERT**: Budget threshold exceeded!" if status['critical'] else "⚠️  **WARNING**: Approaching budget limit" if status['alert'] else "✅ Budget healthy"}

📋 **Usage by Model**:{model_breakdown}

💡 **Recommendation**: 
{"Consider switching to cheaper models to extend budget" if status['alert'] else "Current spending is within acceptable limits"}
"""
    
    return report.strip()


async def check_budget_status() -> str:
    """
    Check if nearing budget limit
    
    Returns:
        Budget alert with recommendations if needed
    """
    status = tracker.get_budget_status()
    
    if status['critical']:
        return f"""
🔴 **CRITICAL BUDGET ALERT!**

💵 Spent: ${status['spent']:.2f} / ${tracker.budget_limit:.2f}
📊 {status['percentage']:.1f}% of budget consumed

⚠️  **Immediate Action Required**:
1. Switch to gpt-4o-mini for all non-critical queries
2. Review and pause non-essential agent activities
3. Request budget increase if needed

💡 **Estimated Impact**:
   Switching to gpt-4o-mini could reduce costs by ~90%
"""
    elif status['alert']:
        return f"""
⚠️  **BUDGET WARNING**

💵 Spent: ${status['spent']:.2f} / ${tracker.budget_limit:.2f}
📊 {status['percentage']:.1f}% of budget consumed
💰 Remaining: ${status['remaining']:.2f}

💡 **Recommendations**:
1. Monitor usage closely
2. Consider switching to cheaper models for simple tasks
3. Review agent configurations for optimization opportunities
"""
    else:
        return f"""
✅ **Budget Status: Healthy**

💵 Spent: ${status['spent']:.2f} / ${tracker.budget_limit:.2f}
📊 {status['percentage']:.1f}% of budget used
💰 Remaining: ${status['remaining']:.2f}

No action needed. Continue normal operations.
"""


async def recommend_model_switch(query_complexity: str = "medium", current_model: str = "gpt-4") -> str:
    """
    Recommend optimal model based on query complexity
    
    Args:
        query_complexity: Complexity level (simple, medium, complex)
        current_model: Current model in use
        
    Returns:
        Model recommendation with cost savings analysis
    """
    complexity = query_complexity.lower()
    
    # Model recommendations by complexity
    recommendations = {
        "simple": {
            "model": "gpt-4o-mini",
            "reason": "Simple queries don't need expensive models",
            "use_cases": ["basic Q&A", "simple summaries", "formatting"]
        },
        "medium": {
            "model": "gpt-3.5-turbo",
            "reason": "Good balance of performance and cost",
            "use_cases": ["code review", "analysis", "recommendations"]
        },
        "complex": {
            "model": "gpt-4",
            "reason": "Complex reasoning requires most capable model",
            "use_cases": ["architecture design", "security analysis", "critical decisions"]
        }
    }
    
    rec = recommendations.get(complexity, recommendations["medium"])
    
    # Calculate savings
    sample_tokens = 10000  # Typical conversation
    savings = tracker.calculate_savings(current_model, rec["model"], sample_tokens)
    
    response = f"""
💡 **Model Recommendation for {complexity.upper()} Complexity**

🎯 **Recommended Model**: {rec["model"]}
📝 **Reason**: {rec["reason"]}

💰 **Cost Analysis** (per 10K tokens):
   • Current ({current_model}): ${savings['from_cost']:.4f}
   • Recommended ({rec["model"]}): ${savings['to_cost']:.4f}
   • **Savings**: ${savings['savings']:.4f} ({savings['savings_percentage']:.1f}% reduction)

✨ **Best For**:
{chr(10).join(f'   • {use_case}' for use_case in rec['use_cases'])}
"""
    
    if rec["model"] != current_model:
        response += f"\n\n🔄 **Action**: Switch from {current_model} to {rec['model']} for optimal cost-performance balance"
    else:
        response += f"\n\n✅ You're already using the optimal model for this complexity level"
    
    return response.strip()


async def simulate_usage(model: str = "gpt-4", tokens: int = 5000) -> str:
    """
    Simulate token usage to test cost tracking (demo/testing only)
    
    Args:
        model: Model name
        tokens: Number of tokens to simulate
        
    Returns:
        Updated usage statistics
    """
    tracker.add_usage(model, tokens)
    
    return f"""
🧪 **Simulated Usage Added**

✅ Added {tokens:,} tokens for {model}

Updated Statistics:
• Total Tokens: {tracker.total_tokens:,}
• Total Cost: ${tracker.total_cost:.2f}
• Budget Used: {tracker.get_budget_status()['percentage']:.1f}%
"""


# Register tools
@app.list_tools()
async def list_tools() -> list[types.Tool]:
    """List available tools"""
    return [
        types.Tool(
            name="get_token_usage",
            description="Get current token usage statistics",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="check_budget_status",
            description="Check if nearing budget limit",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="recommend_model_switch",
            description="Recommend optimal model based on query complexity",
            inputSchema={
                "type": "object",
                "properties": {
                    "query_complexity": {"type": "string", "description": "Complexity level", "default": "medium"},
                    "current_model": {"type": "string", "description": "Current model", "default": "gpt-4"}
                }
            }
        ),
        types.Tool(
            name="simulate_usage",
            description="Simulate token usage for testing",
            inputSchema={
                "type": "object",
                "properties": {
                    "model": {"type": "string", "description": "Model name", "default": "gpt-4"},
                    "tokens": {"type": "integer", "description": "Number of tokens", "default": 5000}
                }
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle tool calls"""
    if name == "get_token_usage":
        result = await get_token_usage()
    elif name == "check_budget_status":
        result = await check_budget_status()
    elif name == "recommend_model_switch":
        result = await recommend_model_switch(
            arguments.get("query_complexity", "medium"),
            arguments.get("current_model", "gpt-4")
        )
    elif name == "simulate_usage":
        result = await simulate_usage(
            arguments.get("model", "gpt-4"),
            arguments.get("tokens", 5000)
        )
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
