# Scenext MCP Server

[English](README.en.md) | [中文](README.zh.md)

[![smithery badge](https://smithery.ai/badge/@typing233/scenext-mcp)](https://smithery.ai/server/@typing233/scenext-mcp)

---

An MCP server that integrates with [Scenext](https://scenext.cn) AI video generation platform to create educational explanation videos based on topics.

一个集成 [Scenext](https://scenext.cn) AI 视频生成平台的 MCP 服务器，可以根据题目生成教学讲解视频。

## Quick Start / 快速开始

### Installing via Smithery

To install scenext-mcp for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@typing233/scenext-mcp):

```bash
npx -y @smithery/cli install @typing233/scenext-mcp --client claude
```

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

远程接入（streamable-http）：

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
Some clients do not support the headers field. You can manually configure and add the request header "Authorization=Bearer your_actual_api_key_here".

For detailed documentation:
- [English Documentation](README.en.md)
- [中文文档](README.zh.md)

## License / 许可证

MIT License
