# Scenext MCP Server

**中文** | [English](README.en.md)

一个集成 [Scenext](https://scenext.cn) AI 视频生成平台的 MCP 服务器，可以根据题目生成教学讲解视频。

## 配置

在 Claude Desktop 的配置文件中添加：

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
      "url": "https://mcp.scenext.cn/mcp",
      "headers": {
        "Authorization": "Bearer your_actual_api_key_here"
      }
    }
  }
}
```

## 获取API KEY

### 第一步：注册账户

访问 [scenext.cn](https://scenext.cn) 注册您的账户。

### 第二步：获取API密钥

1. 登录后进入个人中心
2. 找到"API Keys管理"
3. 点击"创建API密钥"
4. 保存您的API密钥（请妥善保管）

## 功能

- `gen_video` - 生成教学视频
- `query_video_status` - 查询视频生成状态

## 许可证

MIT License