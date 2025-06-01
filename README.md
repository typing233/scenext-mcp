# Scenext MCP Server

一个基于MCP (Model Context Protocol) 的Scenext视频生成服务器，提供视频生成和状态查询功能。

## 功能特性

- 🎬 **视频生成**: 根据问题和答案生成教学视频
- 📊 **状态查询**: 实时查询视频生成进度
- 📁 **结果获取**: 获取已完成视频的下载链接
- 🔧 **错误处理**: 完善的错误处理和日志记录
- ⚙️ **配置管理**: 支持环境变量配置
- 📦 **PyPI发布**: 支持uvx一键安装

## 🚀 快速安装

### 方式1: 使用uvx (推荐)

```bash
# 一键运行，无需安装
uvx scenext-mcp

# 或者安装后使用
pip install scenext-mcp
scenext-mcp
```

### 方式2: 传统安装

```bash
pip install scenext-mcp
```

## 安装和配置

### 1. 环境变量配置

设置你的Scenext API密钥：

```bash
# Windows
set SCENEXT_API_KEY=your_actual_api_key_here

# Linux/Mac
export SCENEXT_API_KEY=your_actual_api_key_here
```

### 2. MCP客户端配置

在MCP客户端（如Claude Desktop）中配置：

```json
{
  "mcpServers": {
    "scenext": {
      "command": "uvx", 
      "args": ["scenext-mcp", "-y"],
      "env": {
        "SCENEXT_API_KEY": "your_actual_api_key_here",
        "SCENEXT_DEFAULT_QUALITY": "h"
      }
    }
  }
}
```

配置文件位置：
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

## 本地开发

如果你想从源码运行或开发：

### 1. 克隆项目

```bash
git clone <repository-url>
cd Scenext-MCP
```

### 2. 创建虚拟环境

```bash
python -m venv myenv
# Windows
myenv\Scripts\activate
# Linux/Mac
source myenv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

复制环境变量模板：
```bash
copy .env.example .env
```

编辑 `.env` 文件，设置你的API密钥：
```env
SCENEXT_API_KEY=your_actual_api_key_here
```

### 5. 启动服务器

```bash
# 使用脚本启动
start.bat  # Windows
./start.ps1  # PowerShell

# 或直接运行
python app.py
```

## 使用方法

### 启动服务器

```bash
python app.py
```

### MCP工具

#### 1. gen_video - 生成视频

生成教学视频。

**参数:**
- `question` (必填): 问题内容
- `answer` (可选): 答案内容
- `question_images` (可选): 问题相关图片URL列表
- `answer_images` (可选): 答案相关图片URL列表
- `quality` (可选): 视频质量 (l/m/h，默认m)
- `notify_url` (可选): 回调通知URL

**示例:**
```python
result = await gen_video(
    question="什么是傅里叶级数？",
    answer="傅里叶级数是数学分析中的一个重要概念...",
    quality="h"
)
```

#### 2. query_video_status - 查询状态

查询视频生成任务的状态。

**参数:**
- `task_id` (必填): 任务ID

**示例:**
```python
status = await query_video_status("task_123456")
```

#### 3. get_video_result - 获取结果

获取已完成视频的结果信息。

**参数:**
- `task_id` (必填): 任务ID

**示例:**
```python
result = await get_video_result("task_123456")
```

## API响应格式

### 成功响应
```json
{
    "task_id": "task_123456",
    "status": "processing|completed|failed",
    "video_url": "https://example.com/video.mp4",
    "thumbnail_url": "https://example.com/thumb.jpg"
}
```

### 错误响应
```json
{
    "error": "错误描述",
    "details": "详细错误信息"
}
```

## 视频质量说明

- `l` (低质量): 快速生成，文件较小
- `m` (中等质量): 平衡质量和速度 (默认)
- `h` (高质量): 最佳质量，生成时间较长

## 状态说明

- `pending`: 任务排队中
- `processing`: 正在生成视频
- `completed`: 生成完成
- `failed`: 生成失败

## 错误处理

服务器提供完善的错误处理机制：

- 网络请求错误
- API认证错误
- 参数验证错误
- 超时处理
- 详细的错误日志

## 日志配置

可以通过环境变量 `SCENEXT_LOG_LEVEL` 设置日志级别：
- `DEBUG`: 详细调试信息
- `INFO`: 一般信息 (默认)
- `WARNING`: 警告信息
- `ERROR`: 错误信息

## 依赖项

- `mcp[cli]==1.9.2`: MCP服务器框架
- `aiohttp==3.12.6`: 异步HTTP客户端
- `python-dotenv==1.0.0`: 环境变量管理

## 开发和贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 许可证

[MIT License](LICENSE)
