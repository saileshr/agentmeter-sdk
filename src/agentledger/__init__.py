"""AgentLedger — cost tracking and attribution for AI agents.

Usage:
    # OpenAI
    from agentledger import track_openai
    client = track_openai(openai.OpenAI(), project="my-agent")

    # Any LLM (manual)
    from agentledger import track_llm_call
    with track_llm_call(provider="openai", model="gpt-4o") as call:
        response = my_llm_call(...)
        call.input_tokens = response.usage.input_tokens

    # Business outcome attribution
    from agentledger import record_outcome
    record_outcome(run_id="run-123", outcome="ticket_resolved", value_usd=12.50)
"""

from agentledger._version import __version__
from agentledger.adapters.generic import track_llm_call
from agentledger.config import AgentLedgerConfig
from agentledger.cost import CostRegistry, ModelPricing
from agentledger.exporters.console import ConsoleExporter
from agentledger.exporters.memory import MemoryExporter
from agentledger.outcome import record_outcome
from agentledger.tracker import configure, get_tracker, reset
from agentledger.types import CostBreakdown, LLMEvent, Outcome, TokenUsage

# Lazy imports for optional-dependency adapters
_LAZY_IMPORTS = {
    "track_openai": ("agentledger.adapters.openai", "track_openai"),
    "track_anthropic": ("agentledger.adapters.anthropic", "track_anthropic"),
}


def __getattr__(name: str):
    if name in _LAZY_IMPORTS:
        module_path, attr_name = _LAZY_IMPORTS[name]
        try:
            import importlib

            module = importlib.import_module(module_path)
            return getattr(module, attr_name)
        except ImportError as e:
            package = name.replace("track_", "")
            raise ImportError(
                f"agentledger.{name} requires the '{package}' package. "
                f"Install it with: pip install agentledger[{package}]"
            ) from e
    raise AttributeError(f"module 'agentledger' has no attribute {name}")


__all__ = [
    "__version__",
    # Config
    "AgentLedgerConfig",
    "configure",
    "get_tracker",
    "reset",
    # Types
    "LLMEvent",
    "TokenUsage",
    "CostBreakdown",
    "Outcome",
    # Cost
    "CostRegistry",
    "ModelPricing",
    # Adapters
    "track_openai",
    "track_anthropic",
    "track_llm_call",
    # Outcome
    "record_outcome",
    # Exporters
    "ConsoleExporter",
    "MemoryExporter",
]
