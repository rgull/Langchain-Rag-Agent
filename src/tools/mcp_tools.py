from pathlib import Path
from langchain_mcp_adapters.client import MultiServerMCPClient

# Get the project root directory (3 levels up from this file: src/tools -> src -> root)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MATH_SERVER_PATH = BASE_DIR / "mcp_servers" / "math_server.py"

client = MultiServerMCPClient(
    {
        "math": {
            "transport": "stdio",
            "command": "python",
            "args": [str(MATH_SERVER_PATH)],
        },
        "weather": {
            "transport": "http",
            "url": "http://127.0.0.1:8000/mcp",
        }
    }
)

async def get_mcp_tools():
    return await client.get_tools()
