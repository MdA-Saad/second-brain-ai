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
    echo "HF_TOKEN=your_token_here" > .env
    echo "Created .env. Please update it with your actual token."
fi

echo "Setup complete! Use 'source .venv/bin/activate' to start."
echo "Pro-tip: Type 'uv run python - m src.app' to launch the UI."
