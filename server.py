import os

import httpx
from mcp.server import MCPServer

NEXPLOY_API_BASE = "https://nexploy-smith-1.onrender.com"

mcp = MCPServer("nexploy")


@mcp.tool()
async def fetch_user(access_token: str) -> dict:
    """Fetch the authenticated Nexploy user's profile.

    Args:
        access_token: Bearer access token returned by the Nexploy login endpoint.
    """
    headers = {"Authorization": f"Bearer {access_token}"}

    async with httpx.AsyncClient(base_url=NEXPLOY_API_BASE, timeout=30.0) as client:
        response = await client.get("/profile/me", headers=headers)

    if response.status_code == 401:
        raise ValueError("The Nexploy access token is invalid or expired.")

    if response.is_error:
        raise RuntimeError(
            f"Nexploy profile request failed with HTTP {response.status_code}."
        )

    return response.json()

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
    )