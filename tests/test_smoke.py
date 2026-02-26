"""Smoke test suite for Ouroboros.

Tests core invariants:
- All modules import cleanly
- Tool registry discovers all expected tools
- ...
"""
import ast
import os
import pathlib
import re
import sys
import tempfile

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent

# ── Module imports ───────────────────────────────────────────────

CORE_MODULES = [
    "ouroboros.agent",
    "ouroboros.context",
    "ouroboros.loop",
    "ouroboros.llm",
    "ouroboros.memory",
    "ouroboros.review",
    "ouroboros.utils",
    "ouroboros.consciousness",
]

TOOL_MODULES = [
    "ouroboros.tools.registry",
    "ouroboros.tools.core",
    "ouroboros.tools.git",
    "ouroboros.tools.shell",
    # REMOVED: "ouroboros.tools.search", (DEPRECATED)
    "ouroboros.tools.control",
    "ouroboros.tools.browser",
    "ouroboros.tools.review",
    "ouroboros.tools.web_search",
]

SUPERVISOR_MODULES = [
    "supervisor.state",
    "supervisor.telegram",
    "supervisor.queue",
    "supervisor.workers",
    "supervisor.git_ops",
    "supervisor.events",
]


@pytest.mark.parametrize("module", CORE_MODULES + TOOL_MODULES + SUPERVISOR_MODULES)
def test_import(module):
    """Every module imports without error."""
    __import__(module)


# ── Tool registry ────────────────────────────────────────────────

@pytest.fixture
def registry():
    from ouroboros.tools.registry import ToolRegistry
    tmp = pathlib.Path(tempfile.mkdtemp())
    return ToolRegistry(repo_dir=tmp, drive_root=tmp)

def test_tool_set_matches(registry):
    """Tool registry contains exactly the expected tools (no more, no less)."""
    schemas = registry.schemas()
    actual_tools = {t["function"]["name"] for t in schemas}
    expected_tools = set(EXPECTED_TOOLS)

    missing = expected_tools - actual_tools
    extra = actual_tools - expected_tools

    assert missing == set(), f"Missing tools: {sorted(missing)}"
    assert extra == set(), f"Extra tools: {sorted(extra)}"
    assert actual_tools == expected_tools, "Tool set mismatch"


EXPECTED_TOOLS = [
    "repo_read", "repo_write_commit", "repo_list", "repo_commit_push",
    "drive_read", "drive_write", "drive_list",
    "git_status", "git_diff",
    "run_shell", "claude_code_edit",
    "browse_page", "browser_action",
    "web_search",
    "chat_history", "update_scratchpad", "update_identity",
    "request_restart", "promote_to_stable", "request_review",
    "schedule_task", "cancel_task",
    "switch_model", "toggle_evolution", "toggle_consciousness",
    "send_owner_message", "send_photo",
    "codebase_digest", "codebase_health",
    "knowledge_read", "knowledge_write", "knowledge_list",
    "multi_model_review",
    # GitHub Issues
    "list_github_issues", "get_github_issue", "comment_on_issue",
    "close_github_issue", "create_github_issue",
    "summarize_dialogue",
    # Task decomposition
    "get_task_result", "wait_for_task",
    "generate_evolution_stats",
    # VLM / Vision
    "analyze_screenshot", "vlm_query",
    # Message routing
    "forward_to_worker",
    # Context management
    "compact_context",
    "list_available_tools",
    "enable_tools",
]


@pytest.mark.parametrize("tool_name", EXPECTED_TOOLS)
def test_tool_registered(registry, tool_name):
    """Each expected tool is in the registry."""
    available = [t["function"]["name"] for t in registry.schemas()]
    assert tool_name in available, f"{tool_name} not in registry"


# ... rest of tests remain unchanged