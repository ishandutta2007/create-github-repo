"""Resolve a GitHub personal access token from arguments or the environment."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


def resolve_token(explicit_token: str | None = None) -> str | None:
    """Return a GitHub token, trying sources in priority order.

    Resolution order:
        1. ``explicit_token`` (passed via ``--token``).
        2. ``ADMIN_TOKEN`` from a ``.env`` file in the **current working directory**.
        3. ``ADMIN_TOKEN`` already present in the process environment.

    Args:
        explicit_token: A token supplied directly (e.g. from the CLI).

    Returns:
        The resolved token string, or ``None`` if no token was found.
    """
    if explicit_token:
        return explicit_token

    # Try loading .env from the current working directory
    env_path = Path.cwd() / ".env"
    if env_path.is_file():
        load_dotenv(dotenv_path=env_path, override=True)

    token = os.environ.get("ADMIN_TOKEN")
    return token if token else None
