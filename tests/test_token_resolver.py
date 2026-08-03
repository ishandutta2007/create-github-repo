"""Tests for token resolution logic."""

import os
from pathlib import Path
from unittest.mock import patch

from create_github_repo.token_resolver import resolve_token


class TestExplicitToken:
    """An explicit token should always win."""

    def test_explicit_token_returned(self):
        assert resolve_token("ghp_explicit") == "ghp_explicit"

    @patch.dict(os.environ, {"ADMIN_TOKEN": "ghp_env"})
    def test_explicit_beats_env(self):
        assert resolve_token("ghp_explicit") == "ghp_explicit"


class TestDotenvFallback:
    """Should load ADMIN_TOKEN from .env when no explicit token given."""

    def test_loads_from_dotenv(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / ".env").write_text("ADMIN_TOKEN=ghp_from_dotenv\n")
        # Clear any existing env var so .env takes effect
        monkeypatch.delenv("ADMIN_TOKEN", raising=False)
        assert resolve_token() == "ghp_from_dotenv"


class TestNoTokenAvailable:
    """Should return None when nothing is set."""

    def test_returns_none(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        monkeypatch.delenv("ADMIN_TOKEN", raising=False)
        assert resolve_token() is None
