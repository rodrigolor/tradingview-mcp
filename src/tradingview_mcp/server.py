"""TradingView MCP Server - Main entry point for the Model Context Protocol server.

This module implements the MCP server that exposes TradingView data
and analysis tools to AI assistants.
"""

import asyncio
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    CallToolResult,
    ListToolsResult,
)

from .tools import get_ticker_info, get_technical_analysis, search_symbols, get_screener_data

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize the MCP server
app = Server("tradingview-mcp")


@app.list_tools()
async def list_tools() -> ListToolsResult:
    """Return the list of available TradingView tools."""
    return ListToolsResult(
        tools=[
            Tool(
                name="get_ticker_info",
                description="Retrieve detailed information about a stock or crypto ticker symbol from TradingView, including price, volume, market cap, and fundamental data.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "The ticker symbol (e.g., BTCUSDT', 'EU)",
                        },": {
                            "n                            "description": "The exchange (e.g., 'NASDAQBINANCE'). Optional.",
                        },
                    },
                    "required": ["symbol"],
                },
            ),
            Tool(
                name="get_technical_analysis",
                description="Get technical analysis summary for a symbol including oscillators, moving averages, and overall buy/sell/neutral signals.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "The ticker symbol to analyze",
                        },
                        "interval":            "description '1m', '5m', '15md', '1W', '1M'",
                            "default": "1d",
                        },
                        "exchange": {
                            "type": "string",
                            "description": "The exchange. Optional.",
                        },
                    },
                    "required": ["symbol"],
                },
            ),
            Tool(
                name="search_symbols",
                description="Search for ticker symbols on TradingView by name or keyword.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query (company name, symbol, or keyword)",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results to return (default: 10)",
                            "default": 10,
                        },
                    },
                    "required": ["query"],
                },
            ),
            Tool(
                name="get_screener_data",
                description="Screen stocks based on various filters using TradingView's screener.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "screener": {
                            "type": "string",
                            "description": "Market screener: 'america', 'crypto', 'forex', 'india', 'uk', etc.",
                            "default": "america",
                        },
                        "category": {
                            "type": "string",
                            "description": "Asset category: 'stock', 'crypto', 'forex', 'cfd'",
                            "default": "stock",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Number of results to return (default: 20, max: 100)",
                            "default": 20,
                        },
                    },
                    "required": [],
                },
            ),
        ]
    )


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> CallToolResult:
    """Handle tool calls from the MCP client."""
    logger.info("Tool called: %s with arguments: %s", name, arguments)

    try:
        if name == "get_ticker_info":
            result = await get_ticker_info(
                symbol=arguments["symbol"],
                exchange=arguments.get("exchange"),
            )
        elif name == "get_technical_analysis":
            result = await get_technical_analysis(
                symbol=arguments["symbol"],
                interval=arguments.get("interval", "1d"),
                exchange=arguments.get("exchange"),
            )
        elif name == "search_symbols":
            result = await search_symbols(
                query=arguments["query"],
                limit=arguments.get("limit", 10),
            )
        elif name == "get_screener_data":
            result = await get_screener_data(
                screener=arguments.get("screener", "america"),
                category=arguments.get("category", "stock"),
                limit=arguments.get("limit", 20),
            )
        else:
            raise ValueError(f"Unknown tool: {name}")

        return CallToolResult(
            content=[TextContent(type="text", text=result)]
        )

    except Exception as e:
        logger.error("Error executing tool %s: %s", name, str(e))
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error: {str(e)}")],
            isError=True,
        )


async def main() -> None:
    """Run the TradingView MCP server."""
    logger.info("Starting TradingView MCP server...")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
