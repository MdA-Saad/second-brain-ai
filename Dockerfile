# Use uv-integrated python image for speed
From ghcr.io/astral-sh/uv:python3.12-slim

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

# Expose Gradio's default port
EXPOSE 7860

# Ensure the app is reachable outside the container
ENV GRADIO_SERVER_NAME="0.0.0.0"

# Run the Gradio app
CMD ["uv", "run", "src/app.py"]

