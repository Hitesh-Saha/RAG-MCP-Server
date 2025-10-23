
# syntax=docker/dockerfile:1.4
FROM python:3.12-slim

# DockerHub metadata labels
LABEL org.opencontainers.image.title="RAG MCP Server"
LABEL org.opencontainers.image.description="A Retrieval Augmented Generation (RAG) server implementing the Model Context Protocol (MCP). Embed, search, and manage documents with a vector database."
LABEL org.opencontainers.image.source="https://github.com/Hitesh-Saha/RAG-MCP-Server"
LABEL org.opencontainers.image.licenses="MIT"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies if needed
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*


# Set work directory
WORKDIR /app

# Install uv
RUN pip install uv

# Copy requirements
COPY pyproject.toml uv.lock* ./

# Install dependencies using uv
RUN uv sync --frozen

COPY . .

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Expose the port your MCP server uses (adjust as needed)
EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app
ENV UV_SYSTEM_PYTHON=1


# Health check (optional but recommended)
# HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
#     CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Run your FastMCP server
CMD ["uv", "run", "rag_mcp_server"]
