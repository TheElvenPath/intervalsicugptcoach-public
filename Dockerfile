# Remote MCP server for intervals.icu — see DEPLOY.md
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Runs unprivileged: a compromise here should not be able to rewrite the image.
RUN useradd --create-home --uid 10001 mcp && chown -R mcp:mcp /app
USER mcp

EXPOSE 8000

# --no-access-log keeps the MCP_SECRET (which lives in the URL path) out of
# container logs. Caddy logs requests instead, with the URI stripped.
CMD ["uvicorn", "mcp_http_server:app", \
     "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]
