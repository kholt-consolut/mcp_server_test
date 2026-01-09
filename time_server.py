from mcp.server.fastmcp import FastMCP
from datetime import datetime

# Create an instance of the FastMCP server
mcp = FastMCP("TimeServer", stateless_http=True)

@mcp.tool(description="Provides the current time in ISO format as a string")
def get_current_time() -> str:
    """
    Use this tool to get the current time in ISO format as a string.

    Returns:
    str: Current time in ISO format. The full format looks like 'YYYY-MM-DD HH:MM:SS.mmmmmm'. The default separator between date and time is 'T'. e.g 2025-10-17T17:04:22.739427. 
    """
    return datetime.now().isoformat()

