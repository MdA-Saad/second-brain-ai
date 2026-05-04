#! /bin/bash

set -e

echo "Setting up second brain ai environment..."

if ! command -v uv &> /dev/null
then
    echo "uv is not installed. Installing now.."
    curl -Lssf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
fi

echo "Syncing dependencies..."
uv sync

if [! -f .env]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Created .env. Please update it with your actual token."
fi
set -a #automatically export all variables
source .env # read the .env files
set +a

echo "Setup complete! Use 'source .venv/bin/activate' to start."
echo "Pro-tip: Type 'uv run python - m src.app' to launch the UI."


