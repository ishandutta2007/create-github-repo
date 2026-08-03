"""Interact with the GitHub REST API to create repositories."""

from __future__ import annotations

import requests

GITHUB_API_URL = "https://api.github.com/user/repos"


def create_repository(
    name: str,
    token: str,
    description: str = "",
    private: bool = False,
) -> tuple[bool, str]:
    """Create a new GitHub repository for the authenticated user.

    Args:
        name: Repository name.
        token: GitHub personal access token.
        description: Repository description (may be empty).
        private: Whether the repository should be private.

    Returns:
        A ``(success, message)`` tuple.  On success the message contains the
        clone URL; on failure it contains a human-readable error.
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    payload: dict[str, object] = {
        "name": name,
        "private": private,
    }
    if description:
        payload["description"] = description

    try:
        response = requests.post(
            GITHUB_API_URL,
            headers=headers,
            json=payload,
            timeout=30,
        )
    except requests.ConnectionError:
        return False, "Network error: could not reach GitHub. Check your connection."
    except requests.Timeout:
        return False, "Request timed out while contacting GitHub."

    if response.status_code == 201:
        repo_data = response.json()
        clone_url = repo_data.get("clone_url", repo_data.get("html_url", ""))
        return True, f"Repository created successfully: {clone_url}"

    # --- Error handling ---
    try:
        error_body = response.json()
        errors = error_body.get("errors", [])
        if errors:
            details = "; ".join(e.get("message", str(e)) for e in errors)
        else:
            details = error_body.get("message", response.text)
    except ValueError:
        details = response.text

    status = response.status_code
    if status == 401:
        return False, f"Authentication failed (HTTP 401): {details}"
    if status == 403:
        return False, f"Forbidden (HTTP 403): {details}"
    if status == 422:
        return False, f"Validation failed (HTTP 422): {details}"

    return False, f"GitHub API error (HTTP {status}): {details}"
