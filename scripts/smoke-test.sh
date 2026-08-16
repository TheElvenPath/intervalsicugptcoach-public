#!/usr/bin/env bash
# Start a freshly built image and prove it actually serves MCP.
#
# `docker build` succeeding says nothing about whether the app runs: an
# unpinned mcp>=1.26.0 once resolved to 2.0.0, which renamed
# mcp.server.fastmcp — the image built cleanly and died on import. Only running
# it catches that class of failure, so CI runs this before deploying.
#
# Credentials are deliberately fake. The server never calls intervals.icu at
# startup, so bogus values are enough to exercise import, tool registration and
# the HTTP transport.
#
#   ./scripts/smoke-test.sh [image-tag]

set -euo pipefail

IMAGE="${1:-intervals-mcp:smoke}"
NAME="intervals-mcp-smoke-$$"
PORT="${SMOKE_PORT:-18000}"
HOSTNAME_="smoke.local"
# Must satisfy the server's own rules: >=24 chars, URL-safe alphabet.
SECRET="ci_smoke_secret_0123456789_abcdefgh"

cleanup() { docker rm -f "$NAME" >/dev/null 2>&1 || true; }
trap cleanup EXIT

echo "==> starting $IMAGE"
docker run -d --name "$NAME" -p "127.0.0.1:$PORT:8000" \
  -e ICU_API_KEY=smoke-not-a-real-key \
  -e ICU_ATHLETE_ID=i0 \
  -e MCP_SECRET="$SECRET" \
  -e MCP_PUBLIC_HOST="$HOSTNAME_" \
  "$IMAGE" >/dev/null

echo "==> waiting for /healthz"
for i in $(seq 1 30); do
  if curl -fsS -m 2 "http://127.0.0.1:$PORT/healthz" >/dev/null 2>&1; then
    echo "    up after ${i}s"
    break
  fi
  if [ "$i" = 30 ]; then
    echo "FAIL: /healthz never answered" >&2
    docker logs "$NAME" 2>&1 | tail -40 >&2
    exit 1
  fi
  sleep 1
done

# Health alone only proves Starlette booted. Listing tools proves FastMCP
# registered them and the streamable-HTTP transport works end to end.
echo "==> checking tools/list"
body=$(curl -fsS -m 10 -X POST "http://127.0.0.1:$PORT/$SECRET/mcp" \
  -H "Host: $HOSTNAME_" \
  -H "Origin: https://claude.ai" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}')

count=$(printf '%s' "$body" | grep -o '"name":"[a-z_]*"' | wc -l | tr -d ' ')
echo "    tools registered: $count"

if [ "$count" -lt 10 ]; then
  echo "FAIL: expected at least 10 tools, got $count" >&2
  printf '%s\n' "$body" | head -c 500 >&2
  exit 1
fi

# The Origin allow-list is a security control, so a regression in it should fail
# the build rather than be discovered in production.
echo "==> checking that a foreign Origin is rejected"
code=$(curl -s -o /dev/null -w '%{http_code}' -m 10 -X POST "http://127.0.0.1:$PORT/$SECRET/mcp" \
  -H "Host: $HOSTNAME_" \
  -H "Origin: https://evil.example.com" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}')

if [ "$code" != "403" ]; then
  echo "FAIL: foreign Origin returned $code, expected 403" >&2
  exit 1
fi
echo "    rejected with 403"

echo "==> smoke test passed"
