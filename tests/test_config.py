"""Tests for agentledger.config."""


from agentledger.config import AgentLedgerConfig
from agentledger.exporters.console import ConsoleExporter
from agentledger.exporters.memory import MemoryExporter


class TestAgentLedgerConfig:
    def test_defaults(self):
        config = AgentLedgerConfig()
        assert config.project == "default"
        assert config.tags == {}
        assert config.enabled is True
        assert config.debug is False
        assert len(config.exporters) == 1
        assert isinstance(config.exporters[0], ConsoleExporter)

    def test_explicit_project(self):
        config = AgentLedgerConfig(project="my-project")
        assert config.project == "my-project"

    def test_explicit_exporters(self):
        mem = MemoryExporter()
        config = AgentLedgerConfig(exporters=[mem])
        assert config.exporters == [mem]

    def test_env_project(self, monkeypatch):
        monkeypatch.setenv("AGENTLEDGER_PROJECT", "env-project")
        config = AgentLedgerConfig()
        assert config.project == "env-project"

    def test_explicit_overrides_env(self, monkeypatch):
        monkeypatch.setenv("AGENTLEDGER_PROJECT", "env-project")
        config = AgentLedgerConfig(project="explicit")
        assert config.project == "explicit"

    def test_env_disabled(self, monkeypatch):
        monkeypatch.setenv("AGENTLEDGER_ENABLED", "false")
        config = AgentLedgerConfig()
        assert config.enabled is False

    def test_env_debug(self, monkeypatch):
        monkeypatch.setenv("AGENTLEDGER_DEBUG", "true")
        config = AgentLedgerConfig()
        assert config.debug is True

    def test_env_export_memory(self, monkeypatch):
        monkeypatch.setenv("AGENTLEDGER_EXPORT", "memory")
        config = AgentLedgerConfig()
        assert len(config.exporters) == 1
        assert isinstance(config.exporters[0], MemoryExporter)

    def test_disabled_config(self):
        config = AgentLedgerConfig(enabled=False)
        assert config.enabled is False
