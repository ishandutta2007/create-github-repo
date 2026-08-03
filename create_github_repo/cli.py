"""Command-line interface for create-github-repo."""

import argparse
import sys

from create_github_repo import __version__
from create_github_repo.github_api import create_repository
from create_github_repo.token_resolver import resolve_token


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(
        prog="create-github-repo",
        description="Create a GitHub repository from the command line.",
        epilog=(
            "Examples:\n"
            "  create-github-repo my-new-repo\n"
            "  create-github-repo my-new-repo -d \"A cool project\"\n"
            '  create-github-repo my-new-repo -d "A cool project" -t ghp_xxxx\n'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "name",
        help="Name of the GitHub repository to create (required).",
    )
    parser.add_argument(
        "-d",
        "--description",
        default="",
        help='Repository description (optional). Defaults to "".',
    )
    parser.add_argument(
        "-t",
        "--token",
        default=None,
        help=(
            "GitHub personal access token (optional). "
            "Falls back to ADMIN_TOKEN in a .env file in the current directory."
        ),
    )
    parser.add_argument(
        "--private",
        action="store_true",
        default=False,
        help="Create a private repository. Defaults to public.",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    """Entry point for the CLI.

    Args:
        argv: Command-line arguments. Defaults to ``sys.argv[1:]``.

    Returns:
        Exit code (0 for success, 1 for failure).
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    # --- Resolve token ---
    token = resolve_token(args.token)
    if token is None:
        print(
            "Error: No GitHub token provided.\n"
            "Supply one with --token or set ADMIN_TOKEN in a .env file.",
            file=sys.stderr,
        )
        return 1

    # --- Create the repo ---
    success, message = create_repository(
        name=args.name,
        token=token,
        description=args.description,
        private=args.private,
    )

    if success:
        print(f"✅ {message}")
        return 0
    else:
        print(f"❌ {message}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
