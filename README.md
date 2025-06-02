# Scenext MCP Server

一个集成 [Scenext](https://scenext.cn) AI 视频生成平台的 MCP 服务器，可以根据题目生成教学讲解视频。

## 安装

```bash
pip install scenext-mcp
```

## 配置

在 Claude Desktop 的配置文件中添加：

```json
{
  "mcpServers": {
    "scenext": {
      "command": "uvx",
      "args": ["scenext-mcp"],
      "env": {
        "SCENEXT_API_KEY": "your_api_key_here"
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

## 开发

```bash
# 克隆仓库
git clone https://github.com/your-username/scenext-mcp.git
cd scenext-mcp

# 安装依赖
pip install -e .

# 运行测试
python tests/test_basic.py
```

## 发布新版本

1. 编辑 `scenext_mcp/_version.py` 中的版本号
2. 提交更改并创建标签：
   ```bash
   git add .
   git commit -m "Release version x.x.x"
   git tag vx.x.x
   git push origin main
   git push origin vx.x.x
   ```
3. GitHub Actions 会自动发布到 PyPI

## 许可证

MIT License