# 📦 Scenext MCP PyPI 发布指南

## 🔑 第一步：获取 PyPI API 令牌

### 1. 注册 PyPI 账户
- 访问 [PyPI.org](https://pypi.org/account/register/) 注册账户
- 访问 [TestPyPI.org](https://test.pypi.org/account/register/) 注册测试账户

### 2. 创建 API 令牌
- 登录 PyPI，转到 Account settings > API tokens
- 点击 "Add API token"
- 名称：`scenext-mcp-upload`
- 范围：选择 "Entire account" 或创建项目后选择 "Project: scenext-mcp"
- 复制生成的令牌（以 `pypi-` 开头）

### 3. 配置认证（推荐）
创建 `~/.pypirc` 文件：
```ini
[distutils]
index-servers = 
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-your_actual_token_here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your_actual_testpypi_token_here
```

## 🚀 第二步：发布到 PyPI

### 方法1：使用PowerShell脚本
```powershell
# 运行发布脚本
.\publish.ps1
```

### 方法2：手动发布
```bash
# 1. 激活虚拟环境
myenv\Scripts\activate

# 2. 安装构建工具
pip install build twine --upgrade

# 3. 清理旧文件
Remove-Item -Recurse -Force build, dist, scenext_mcp.egg-info

# 4. 构建包
python -m build

# 5. 检查包质量
python -m twine check dist/*

# 6. 上传到TestPyPI（测试）
python -m twine upload --repository testpypi dist/*

# 7. 测试安装
pip install --index-url https://test.pypi.org/simple/ scenext-mcp

# 8. 上传到正式PyPI
python -m twine upload dist/*
```

## 🧪 第三步：测试安装

### 从 TestPyPI 测试
```bash
pip install --index-url https://test.pypi.org/simple/ scenext-mcp
scenext-mcp --version
```

### 从正式 PyPI 安装
```bash
pip install scenext-mcp
scenext-mcp --version
```

### 使用 uvx 运行
```bash
uvx scenext-mcp --help
```

## 📝 第四步：更新 MCP 配置

安装成功后，更新你的 MCP 配置：

```json
{
  "mcpServers": {
    "scenext": {
      "command": "uvx",
      "args": ["scenext-mcp", "-y"],
      "env": {
        "SCENEXT_API_KEY": "your_actual_api_key_here"
      }
    }
  }
}
```

## 🔄 版本更新流程

1. 更新 `pyproject.toml` 中的版本号
2. 重新构建和发布：
```bash
python -m build
python -m twine upload dist/*
```

## ⚠️ 注意事项

- **API令牌安全**：不要在代码中硬编码API令牌
- **版本号**：每次发布必须使用新的版本号
- **测试**：建议先发布到TestPyPI进行测试
- **依赖**：确保所有依赖都在 `pyproject.toml` 中正确列出

## 🆘 常见问题

### 403 Forbidden 错误
- 检查API令牌是否正确
- 确认账户有发布权限
- 检查项目名称是否已被占用

### 包名冲突
- 如果 `scenext-mcp` 已被占用，考虑使用其他名称如 `scenext-mcp-server`

### 版本冲突
- 确保每次发布使用新的版本号
- 可以使用语义化版本 (semver)：1.0.0 -> 1.0.1 -> 1.1.0
