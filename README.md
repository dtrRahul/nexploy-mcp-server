# Nexploy MCP Server

An MCP server that exposes Nexploy user profile data to MCP-compatible AI clients.
It uses the official Python MCP SDK and Streamable HTTP transport.

## What it provides

The server exposes one tool:

- `fetch_user`: fetches the authenticated user's profile from Nexploy using `GET /profile/me`.

The tool expects a Nexploy bearer access token and returns the profile response from the API.

## Requirements

- Python 3.11 or newer
- `uv`

## Install dependencies

```powershell
uv sync
```

## Run locally

Start the Streamable HTTP server from this directory:

```powershell
uv run server.py
```

The server listens on:

```text
http://127.0.0.1:8000/mcp
```

The port is read from the `PORT` environment variable when one is provided, which makes the server compatible with Render.

Do not open `/mcp` directly in a browser. MCP clients must connect using the MCP protocol.

## Connect from VS Code

Create a local `.vscode/mcp.json` file if needed. It is intentionally ignored by Git because it contains machine-specific configuration.

```json
{
	"servers": {
		"nexploy-mcp": {
			"type": "http",
			"url": "http://127.0.0.1:8000/mcp"
		}
	}
}
```

Start the server, reload VS Code, and reconnect the `nexploy-mcp` server. Then call `fetch_user` and provide a valid Nexploy access token through the tool input.

## Deploy to Render

Push this project to GitHub and create a Render **Web Service** connected to the repository.

Use these settings:

- Runtime: `Python`
- Build command: `pip install "mcp[cli]>=2.2.0" "httpx>=0.27.0"`
- Start command: `python server.py`

Render provides the `PORT` environment variable automatically. After deployment, the MCP endpoint is:

```text
https://YOUR-RENDER-SERVICE.onrender.com/mcp
```

Use that URL in an MCP-compatible client.

## Security

This server currently accepts the Nexploy access token as a tool argument. That is suitable for local testing, but a public deployment should add authentication for MCP clients before it is shared publicly.

Never commit access tokens, `.env` files, private keys, or credentials to GitHub. Rotate any token that has been exposed.

## Project structure

```text
server.py       MCP server and fetch_user tool
pyproject.toml  Python project metadata and dependencies
uv.lock         Locked dependency versions
```
