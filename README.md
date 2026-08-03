# create-github-repo

[![PyPI version](https://img.shields.io/pypi/v/create-github-repo.svg)](https://pypi.org/project/create-github-repo/)
[![Python versions](https://img.shields.io/pypi/pyversions/create-github-repo.svg)](https://pypi.org/project/create-github-repo/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A CLI tool to create GitHub repositories from the command line.

## Installation

```bash
pip install create-github-repo
```

## Quick Start

```bash
# Create a public repo (uses ADMIN_TOKEN from .env in the current directory)
create-github-repo my-new-repo

# With a description
create-github-repo my-new-repo -d "A cool project"

# With an explicit token
create-github-repo my-new-repo -t ghp_your_token_here

# Create a private repo
create-github-repo my-new-repo --private
```

## Authentication

The tool resolves your GitHub token in this order:

1. **`--token` / `-t` flag** — passed directly on the command line.
2. **`.env` file** — looks for `ADMIN_TOKEN` in a `.env` file in the **current working directory**.

### Setting up a `.env` file

Create a `.env` file in the directory where you run the command:

```env
ADMIN_TOKEN=github_pat_xxxxxxxxxxxxxxxxxxxx
```

> **Tip:** Add `.env` to your `.gitignore` to avoid committing secrets.

### Generating a GitHub Token

1. Go to [GitHub → Settings → Developer settings → Fine-grained personal access tokens](https://github.com/settings/tokens?type=beta).
2. Click **Generate new token**.
3. Under **Repository permissions**, set **Administration** to **Read and write**.
4. Click **Generate token** and copy the value into your `.env` file.

## Usage

```
usage: create-github-repo [-h] [-d DESCRIPTION] [-t TOKEN] [--private] [-V] name

Create a GitHub repository from the command line.

positional arguments:
  name                  Name of the GitHub repository to create (required).

options:
  -h, --help            show this help message and exit
  -d, --description     Repository description (optional). Defaults to "".
  -t, --token           GitHub personal access token (optional).
                        Falls back to ADMIN_TOKEN in a .env file in the current directory.
  --private             Create a private repository. Defaults to public.
  -V, --version         show program's version number and exit
```

## Examples

```bash
# Minimal — just a repo name
create-github-repo awesome-project

# With description
create-github-repo awesome-project -d "My awesome project"

# Private repo with explicit token
create-github-repo secret-project --private -t ghp_abc123
```

### Output

```
✅ Repository created successfully: https://github.com/youruser/awesome-project.git
```

On error:

```
❌ Validation failed (HTTP 422): name already exists on this account
```

## Development

```bash
# Clone the repo
git clone https://github.com/ishandutta2007/create-github-repo.git
cd create-github-repo

# Install in editable mode
pip install -e .

# Run tests
pip install pytest
pytest -v
```

## Project Structure

```
create-github-repo/
├── create_github_repo/
│   ├── __init__.py          # Package version
│   ├── cli.py               # CLI entry point (argparse)
│   ├── github_api.py        # GitHub REST API interaction
│   └── token_resolver.py    # Token resolution logic
├── tests/
│   ├── test_cli.py
│   ├── test_github_api.py
│   └── test_token_resolver.py
├── .github/
│   └── workflows/
│       └── publish.yml      # CI/CD: test + publish to PyPI
├── pyproject.toml           # Package metadata & build config
├── LICENSE                  # MIT License
└── README.md
```

## License

[MIT](LICENSE) © Ishan Dutta
