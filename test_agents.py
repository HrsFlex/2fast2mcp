"""
Test script to verify all MCP agents are working correctly
"""

import json
import asyncio
from pathlib import Path

# Test that all mock data files are loadable
def test_mock_data():
    """Test that all mock data files can be loaded"""
    print("🧪 Testing Mock Data Files...")
    
    # Test GitHub Watcher mock data
    github_data_path = Path("agents/github_watcher/mock_data.json")
    with open(github_data_path, 'r') as f:
        github_data = json.load(f)
    
    assert len(github_data['pull_requests']) == 4, "Should have 4 PRs"
    assert len(github_data['issues']) == 3, "Should have 3 issues"
    assert 'repository_stats' in github_data, "Should have repo stats"
    print("✅ GitHub Watcher mock data loaded successfully")
    print(f"   - {len(github_data['pull_requests'])} PRs")
    print(f"   - {len(github_data['issues'])} issues")
    
    # Test Ops Agent incidents
    ops_data_path = Path("agents/ops_agent/incidents.json")
    with open(ops_data_path, 'r') as f:
        ops_data = json.load(f)
    
    assert len(ops_data['incidents']) == 4, "Should have 4 incidents"
    assert 'INC-001' in ops_data['incidents'], "Should have INC-001"
    print("✅ Ops Agent incidents data loaded successfully")
    print(f"   - {len(ops_data['incidents'])} incidents")
    
    print("\n✅ All mock data files are valid!\n")


def test_agent_imports():
    """Test that agent server scripts can be imported"""
    print("🧪 Testing Agent Imports...")
    
    import sys
    sys.path.insert(0, str(Path("agents/github_watcher")))
    sys.path.insert(0, str(Path("agents/ops_agent")))
    sys.path.insert(0, str(Path("agents/cost_sentinel")))
    
    try:
        # These imports will fail if the scripts have syntax errors
        import importlib.util
        
        # GitHub Watcher
        spec = importlib.util.spec_from_file_location("github_server", "agents/github_watcher/server.py")
        github_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(github_module)
        print("✅ GitHub Watcher server imports successfully")
        
        # Ops Agent
        spec = importlib.util.spec_from_file_location("ops_server", "agents/ops_agent/server.py")
        ops_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ops_module)
        print("✅ Ops Agent server imports successfully")
        
        # Cost Sentinel
        spec = importlib.util.spec_from_file_location("cost_server", "agents/cost_sentinel/server.py")
        cost_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cost_module)
        print("✅ Cost Sentinel server imports successfully")
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        raise
    
    print("\n✅ All agents import without errors!\n")


def test_config_files():
    """Test that configuration files are valid YAML"""
    print("🧪 Testing Configuration Files...")
    
    try:
        import yaml
    except ImportError:
        print("⚠️  PyYAML not installed, skipping YAML validation")
        return
    
    config_files = [
        "config/agents.yaml",
        "config/guardrails.yaml",
        "config/archestra.yaml"
    ]
    
    for config_file in config_files:
        path = Path(config_file)
        if not path.exists():
            print(f"⚠️  {config_file} not found, skipping")
            continue
            
        with open(path, 'r') as f:
            config = yaml.safe_load(f)
        print(f"✅ {config_file} is valid YAML")
    
    print("\n✅ All configuration files are valid!\n")


def print_demo_scenarios():
    """Print demo scenarios to try"""
    print("=" * 60)
    print("🎯 DEMO SCENARIOS TO TRY")
    print("=" * 60)
    
    print("\n📋 GitHub Watcher:")
    print("  1. 'Summarize PR #42' - Auth middleware PR (MEDIUM risk)")
    print("  2. 'Summarize PR #44' - Database migration (HIGH risk)")
    print("  3. 'List recent issues' - Show open issues")
    print("  4. 'Analyze code diff for PR 42' - Risk analysis")
    
    print("\n🚨 Ops Agent:")
    print("  1. 'Analyze incident INC-001' - API timeout (HIGH severity)")
    print("  2. 'Analyze incident INC-002' - Database corruption (CRITICAL)")
    print("  3. 'List incidents' - Show all open incidents")
    print("  4. 'Execute: Restart API service' - Safe action ✅")
    print("  5. 'Delete production database' - BLOCKED! 🚫")
    
    print("\n💰 Cost Sentinel:")
    print("  1. 'Show me token usage' - Current usage stats")
    print("  2. 'Check budget status' - Budget health check")
    print("  3. 'Recommend model for simple tasks' - Cost optimization")
    print("  4. 'Simulate usage with gpt-4 and 10000 tokens' - Test tracking")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🏎️  MCP AGENT CONTROL TOWER - TEST SUITE")
    print("=" * 60 + "\n")
    
    try:
        # Run all tests
        test_mock_data()
        test_agent_imports()
        test_config_files()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60 + "\n")
        
        # Print demo scenarios
        print_demo_scenarios()
        
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"❌ TESTS FAILED: {e}")
        print("=" * 60)
        raise
