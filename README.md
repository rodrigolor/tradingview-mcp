# TradingView MCP

A Model Context Protocol (MCP) server that provides TradingView market data and technical analysis tools to AI assistants.

> Fork of [atilaahmettaner/tradingview-mcp](https://github.com/atilaahmettaner/tradingview-mcp) with additional features and improvements.

## Features

- 📈 **Real-time market data** — Fetch quotes, OHLCV data, and market summaries
- 🔍 **Symbol search** — Search for stocks, crypto, forex, and other instruments
- 📊 **Technical analysis** — Access TradingView's built-in technical indicators and signals
- 🕯️ **Candlestick data** — Retrieve historical OHLCV data across multiple timeframes
- 🌍 **Multi-market support** — Stocks, crypto, forex, futures, and indices

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Installation

### Using uv (recommended)

```bash
uv pip install tradingview-mcp
```

### From source

```bash
git clone https://github.com/your-username/tradingview-mcp.git
cd tradingview-mcp
uv sync
```

## Configuration

Copy `.env.example` to `.env` and adjust settings:

```bash
cp .env.example .env
```

## Usage

### Running the MCP server

```bash
uv run python -m tradingview_mcp
```

### Claude Desktop integration

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "tradingview": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/tradingview-mcp",
        "run",
        "python",
        "-m",
        "tradingview_mcp"
      ]
    }
  }
}
```

### Docker

```bash
docker build -t tradingview-mcp .
docker run --env-file .env tradingview-mcp
```

## Available Tools

| Tool | Description |
|------|-------------|
| `get_quote` | Get current price and basic quote data for a symbol |
| `search_symbols` | Search for trading symbols by name or ticker |
| `get_technical_analysis` | Get technical analysis summary (buy/sell signals) |
| `get_candlestick_data` | Retrieve OHLCV candlestick data for a symbol |
| `get_market_overview` | Get an overview of major market indices |

## Supported Timeframes

`1m`, `5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `1d`, `1W`, `1M`

> **Note:** I primarily use `1d` and `1W` for position trading and macro trend analysis. `4h` is useful for entry timing once a daily trend is confirmed. `1h` is handy for crypto since it tends to move faster than equities.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)
