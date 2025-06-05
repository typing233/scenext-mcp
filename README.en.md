# Scenext MCP Server

[中文](README.zh.md) | **English**

An MCP server that integrates with [Scenext](https://scenext.cn) AI video generation platform to create educational explanation videos based on topics.


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
Some clients do not support the headers field. You can manually configure and add the request header "Authorization=Bearer your_actual_api_key_here".

Remote access(streamable-http):

```json
{
  "mcpServers": {
    "scenext": {
      "type": "streamable-http",
      "url": "https://mcp.scenext.cn/mcp/",
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

## License

MIT License