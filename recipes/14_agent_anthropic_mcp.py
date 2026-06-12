"""AI agent: let Claude drive the Sugra API through the hosted MCP endpoint.

The Anthropic Messages API can attach remote MCP servers directly - no local
install, no per-endpoint wiring. Claude discovers the right Sugra operation
and calls it on its own.

Setup:
    pip install anthropic
    export ANTHROPIC_API_KEY=...
    export ANTHROPIC_MODEL=...     # any current Claude model id
    export SUGRA_MCP_TOKEN=...     # OAuth token for https://app.sugra.ai/mcp

Run:
    python recipes/14_agent_anthropic_mcp.py
"""
import os

import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model=os.environ["ANTHROPIC_MODEL"],
    max_tokens=1024,
    betas=["mcp-client-2025-04-04"],
    mcp_servers=[
        {
            "type": "url",
            "url": "https://app.sugra.ai/mcp",
            "name": "sugra",
            "authorization_token": os.environ["SUGRA_MCP_TOKEN"],
        }
    ],
    messages=[
        {
            "role": "user",
            "content": "Which US sectors lead this month? Use the Sugra tools.",
        }
    ],
)

for block in response.content:
    if block.type == "text":
        print(block.text)
