# Scenext MCP Server

[中文](README.zh.md) | **English**

An MCP server that integrates with [Scenext](https://scenext.cn) AI video generation platform to create educational explanation videos based on topics.

## Installation

```bash
pip install scenext-mcp
```

## Configuration

Add the following to your Claude Desktop configuration file:

Local access(UVX mode):

```json
{
  "mcpServers": {
    "scenext": {
      "command": "uvx", 
      "args": ["scenext-mcp"],
      "env": {
        "SCENEXT_API_KEY": "your_actual_api_key_here"
      }
    }
  }
}
```

Remote access(SSE):

```json
{
  "mcpServers": {
    "scenext": {
      "type":"sse",
      "url":"https://mcp.scenext.cn/sse?api_key=your_actual_api_key_here"
    }
  }
}
```

or:

```json
{
  "mcpServers": {
    "scenext": {
      "type": "sse",
      "url": "https://mcp.scenext.cn/sse",
      "headers": {
        "Authorization": "Bearer your_actual_api_key_here"
      }
    }
  }
}
```

## Getting API Key

### Step 1: Register Account

Visit [scenext.cn](https://scenext.cn) to register your account.

### Step 2: Obtain API Key

1. After logging in, go to the user center
2. Find "API Keys Management"
3. Click "Create API Key"
4. Save your API key (please keep it safe)

## Features

- `gen_video` - Generate educational videos
- `query_video_status` - Query video generation status

## Development

```bash
# Clone repository
git clone https://github.com/typing233/scenext-mcp.git
cd scenext-mcp

# Install dependencies
pip install -e .

# Run tests
python tests/test_basic.py
```

## Release New Version

1. Edit the version number in `scenext_mcp/_version.py`
2. Commit changes and create tag:
   ```bash
   git add .
   git commit -m "Release version x.x.x"
   git tag vx.x.x
   git push origin main
   git push origin vx.x.x
   ```
3. GitHub Actions will automatically publish to PyPI

## License

MIT License