# 快速启动指南

## 🚀 快速开始

### 第一步：配置API密钥
1. 复制环境变量文件：
   ```powershell
   copy .env.example .env
   ```

2. 编辑 `.env` 文件，设置你的API密钥：
   ```
   SCENEXT_API_KEY=你的实际API密钥
   ```

### 第二步：启动服务器
选择以下任一方式启动：

**方式1：使用批处理文件**
```cmd
start.bat
```

**方式2：使用PowerShell脚本**
```powershell
.\start.ps1
```

**方式3：手动启动**
```powershell
cd "d:\Scenext-MCP"
myenv\Scripts\activate
python app.py
```

### 第三步：测试服务器
运行测试脚本验证功能：
```powershell
myenv\Scripts\activate
python test_server.py
```

## 🛠️ 主要功能

1. **gen_video** - 生成教学视频
2. **query_video_status** - 查询视频生成状态  
3. **get_video_result** - 获取完成的视频结果

## 📝 使用示例

### 生成视频
```python
result = await gen_video(
    question="什么是深度学习？",
    answer="深度学习是机器学习的一个分支...",
    quality="h"  # 高质量
)
```

### 查询状态
```python
status = await query_video_status(task_id)
```

### 获取结果
```python
video_info = await get_video_result(task_id)
```

## ⚙️ 配置选项

在 `.env` 文件中可配置：
- `SCENEXT_API_KEY`: API密钥（必填）
- `SCENEXT_API_BASE_URL`: API基础URL
- `SCENEXT_DEFAULT_QUALITY`: 默认视频质量 (l/m/h)
- `SCENEXT_LOG_LEVEL`: 日志级别 (DEBUG/INFO/WARNING/ERROR)

## 🔍 故障排除

### 常见问题：
1. **API密钥错误**：确保 `.env` 文件中的API密钥正确
2. **网络连接问题**：检查网络连接和防火墙设置
3. **依赖包问题**：运行 `pip install -r requirements.txt`

### 查看日志：
服务器运行时会显示详细的日志信息，帮助你诊断问题。
