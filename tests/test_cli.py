"""Tests for the CLI (argument parsing and exit codes)."""

from unittest.mock import patch

import pytest

from create_github_repo.cli import main


class TestCLIMissingToken:
    """CLI should exit 1 when no token is available."""

    @patch("create_github_repo.cli.resolve_token", return_value=None)
    def test_no_token_exits_with_error(self, _mock_resolve):
        assert main(["my-repo"]) == 1


class TestCLISuccess:
    """CLI should exit 0 on a successful repo creation."""

    @patch(
        "create_github_repo.cli.create_repository",
        return_value=(True, "Repository created successfully: https://github.com/user/my-repo.git"),
    )
    @patch("create_github_repo.cli.resolve_token", return_value="fake-token")
    def test_success_exit_code(self, _mock_resolve, _mock_create):
        assert main(["my-repo"]) == 0

    @patch(
        "create_github_repo.cli.create_repository",
        return_value=(True, "Repository created successfully: https://github.com/user/my-repo.git"),
    )
    @patch("create_github_repo.cli.resolve_token", return_value="fake-token")
    def test_description_forwarded(self, _mock_resolve, mock_create):
        main(["my-repo", "-d", "A cool project"])
        _, kwargs = mock_create.call_args
        assert kwargs["description"] == "A cool project"


class TestCLIFailure:
    """CLI should exit 1 on API failure."""

    @patch(
        "create_github_repo.cli.create_repository",
        return_value=(False, "Validation failed (HTTP 422): name already exists"),
    )
    @patch("create_github_repo.cli.resolve_token", return_value="fake-token")
    def test_failure_exit_code(self, _mock_resolve, _mock_create):
        assert main(["my-repo"]) == 1
