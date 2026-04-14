# Use uv-integrated python image for speed
# Start with the standard python slim image
FROM python:3.12-slim

# Copy the uv binary from the official uv image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Prevents Python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen

# Copy the rest of the application
COPY . .

# Ensure the app is reachable outside the container
ENV GRADIO_SERVER_NAME="0.0.0.0"

# Expose Gradio's default port
EXPOSE 7860

# Run the Gradio app
CMD ["uv", "run", "src/app.py"]

