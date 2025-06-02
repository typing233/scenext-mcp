# Scenext MCP Server

[English](README.en.md) | [中文](README.zh.md)

---

An MCP server that integrates with [Scenext](https://scenext.cn) AI video generation platform to create educational explanation videos based on topics.

一个集成 [Scenext](https://scenext.cn) AI 视频生成平台的 MCP 服务器，可以根据题目生成教学讲解视频。

## Quick Start / 快速开始

本地接入（uvx模式）：

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

远程接入（SSE）：

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

或者：

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

For detailed documentation:
- [English Documentation](README.en.md)
- [中文文档](README.zh.md)

## License / 许可证

MIT License