"""Tests for the GitHub API module (mocked HTTP calls)."""

from unittest.mock import MagicMock, patch

import requests

from create_github_repo.github_api import create_repository


class TestCreateRepositorySuccess:
    """Successful 201 responses."""

    @patch("create_github_repo.github_api.requests.post")
    def test_returns_clone_url(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "clone_url": "https://github.com/user/my-repo.git",
            "html_url": "https://github.com/user/my-repo",
        }
        mock_post.return_value = mock_response

        success, message = create_repository("my-repo", "fake-token")
        assert success is True
        assert "https://github.com/user/my-repo.git" in message


class TestCreateRepositoryErrors:
    """Various error scenarios."""

    @patch("create_github_repo.github_api.requests.post")
    def test_401_unauthorized(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"message": "Bad credentials"}
        mock_post.return_value = mock_response

        success, message = create_repository("my-repo", "bad-token")
        assert success is False
        assert "401" in message

    @patch("create_github_repo.github_api.requests.post")
    def test_422_already_exists(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 422
        mock_response.json.return_value = {
            "message": "Validation Failed",
            "errors": [{"message": "name already exists on this account"}],
        }
        mock_post.return_value = mock_response

        success, message = create_repository("my-repo", "fake-token")
        assert success is False
        assert "422" in message

    @patch(
        "create_github_repo.github_api.requests.post",
        side_effect=requests.ConnectionError("DNS failure"),
    )
    def test_network_error(self, _mock_post):
        success, message = create_repository("my-repo", "fake-token")
        assert success is False
        assert "Network error" in message

    @patch(
        "create_github_repo.github_api.requests.post",
        side_effect=requests.Timeout("timed out"),
    )
    def test_timeout(self, _mock_post):
        success, message = create_repository("my-repo", "fake-token")
        assert success is False
        assert "timed out" in message.lower()
