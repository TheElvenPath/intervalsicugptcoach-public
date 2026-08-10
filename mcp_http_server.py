"""
Remote HTTP entrypoint for the intervals.icu MCP server
=======================================================
Serves the same tools as mcp_server.py over Streamable HTTP so the server can be
added to claude.ai as a custom connector and used from any device — including
mobile, where Claude Desktop and stdio transport are not available.

Single-tenant: the athlete's intervals.icu credentials come from the server's
own environment (ICU_API_KEY / ICU_ATHLETE_ID), exactly as in the stdio server.

Authentication
--------------
claude.ai's custom-connector UI cannot attach a static header to requests, so
the shared secret lives in the URL path instead:

    https://<host>/<MCP_SECRET>/mcp

Over HTTPS the path is encrypted in transit, which makes this a reasonable
personal-use guard. It is not a substitute for OAuth on a shared deployment —
the URL is visible to anyone who can read the reverse-proxy access log, so keep
that log private (see DEPLOY.md) and rotate MCP_SECRET if it ever leaks.

Run:
    uvicorn mcp_http_server:app --host 127.0.0.1 --port 8000
"""

import os
import re
import sys

from starlette.responses import PlainTextResponse

from mcp.server.transport_security import TransportSecuritySettings

# Importing mcp_server registers every @mcp.tool() onto the shared FastMCP
# instance. Its mcp.run(transport="stdio") sits behind an __main__ guard, so the
# import itself starts nothing.
from mcp_server import mcp


def _require_env(name: str, hint: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        sys.stderr.write(f"FATAL: {name} is not set. {hint}\n")
        raise SystemExit(1)
    return value


MCP_SECRET = _require_env(
    "MCP_SECRET",
    "Generate one with: python -c \"import secrets; print(secrets.token_urlsafe(32))\"",
)
PUBLIC_HOST = _require_env(
    "MCP_PUBLIC_HOST",
    "Set it to the domain the reverse proxy serves, e.g. coach.example.com",
)

# A short secret defeats the purpose — an attacker who can guess the path gets
# full read/write access to the athlete's intervals.icu calendar.
if len(MCP_SECRET) < 24:
    sys.stderr.write("FATAL: MCP_SECRET must be at least 24 characters.\n")
    raise SystemExit(1)

# The secret is interpolated into a Starlette route template, where "/" would
# split the path and "{" would be parsed as a path parameter. Restricting it to
# the URL-safe alphabet that secrets.token_urlsafe() emits keeps the route literal.
if not re.fullmatch(r"[A-Za-z0-9_-]+", MCP_SECRET):
    sys.stderr.write(
        "FATAL: MCP_SECRET may contain only letters, digits, '-' and '_'.\n"
        'Generate one with: python -c "import secrets; print(secrets.token_urlsafe(32))"\n'
    )
    raise SystemExit(1)

# The MCP SDK rejects requests whose Host/Origin headers are not allow-listed,
# which is what stops a malicious page from driving this server through the
# user's browser. Defaults cover claude.ai; MCP_ALLOWED_ORIGINS extends the list
# for other clients (comma-separated, exact matches only — no wildcards).
#
# PUBLIC_HOST is deliberately NOT allowed as an origin: this server returns JSON
# to an MCP client, never HTML, so no browser page legitimately calls it from its
# own origin. Leaving it out means that when the server shares a domain with a
# website, a script injected into that site still cannot reach these tools.
_extra_origins = [
    o.strip() for o in os.environ.get("MCP_ALLOWED_ORIGINS", "").split(",") if o.strip()
]
ALLOWED_ORIGINS = [
    "https://claude.ai",
    "https://www.claude.ai",
    *_extra_origins,
]

mcp.settings.streamable_http_path = f"/{MCP_SECRET}/mcp"
# Stateless mode rebuilds session state per request, so a dropped mobile
# connection reconnects cleanly instead of resuming a session the client lost.
mcp.settings.stateless_http = True
mcp.settings.transport_security = TransportSecuritySettings(
    enable_dns_rebinding_protection=True,
    allowed_hosts=[PUBLIC_HOST, f"{PUBLIC_HOST}:*"],
    allowed_origins=ALLOWED_ORIGINS,
)


@mcp.custom_route("/healthz", methods=["GET"])
async def healthz(_request) -> PlainTextResponse:
    """Unauthenticated liveness probe — deliberately leaks nothing."""
    return PlainTextResponse("ok")


app = mcp.streamable_http_app()

sys.stderr.write(
    f"intervals-icu MCP ready on https://{PUBLIC_HOST}/<MCP_SECRET>/mcp\n"
    f"allowed origins: {', '.join(ALLOWED_ORIGINS)}\n"
)
