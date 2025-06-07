FROM python:3.11-slim

# Install pipx and dependencies for uv
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    gcc \
    python3-venv \
    pipx \
 && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:$PATH"

# Install uv using pipx
RUN pipx install uv && \
    which uv && \
    uv --version

WORKDIR /app
COPY service.py .

CMD ["uv", "run", "service.py"]