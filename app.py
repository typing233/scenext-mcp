# Scenext MCP Server - 视频生成服务
from mcp.server.fastmcp import FastMCP
import aiohttp
import json
import os
from typing import List, Optional, Dict, Any
import logging
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
log_level = os.getenv("SCENEXT_LOG_LEVEL", "INFO")
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)

# 版本信息
__version__ = "1.0.0"

# 创建MCP服务器
mcp = FastMCP(
    "Scenext", 
    description=f"Scenext视频生成服务器 v{__version__} - 提供视频生成和状态查询功能"
)

# 配置
API_BASE_URL = os.getenv("SCENEXT_API_BASE_URL", "https://api.scenext.cn/api")
API_KEY = os.getenv("SCENEXT_API_KEY", "YOUR_API_KEY")
DEFAULT_QUALITY = os.getenv("SCENEXT_DEFAULT_QUALITY", "m")

@mcp.tool()
async def gen_video(
    question: str,
    answer: str = "",
    question_images: Optional[List[str]] = None,
    answer_images: Optional[List[str]] = None,
    quality: str = DEFAULT_QUALITY,
    notify_url: Optional[str] = None
) -> Dict[str, Any]:
    """
    生成教学视频
    
    Args:
        question: 问题内容（必填）
        answer: 答案内容（可选）
        question_images: 问题相关图片URL列表（可选）
        answer_images: 答案相关图片URL列表（可选）
        quality: 视频质量，可选值：l(低)、m(中)、h(高)，默认为m
        notify_url: 回调通知URL（可选）
    
    Returns:
        包含任务ID和状态的字典
    """
    if not question.strip():
        return {"error": "问题内容不能为空"}
    
    url = f"{API_BASE_URL}/gen_video"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "question": question,
        "answer": answer,
        "questionImages": question_images or [],
        "answerImages": answer_images or [],
        "quality": quality,
    }
    
    if notify_url:
        data["notify_url"] = notify_url

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info(f"视频生成请求成功: {result}")
                    return result
                else:
                    error_text = await response.text()
                    logger.error(f"API请求失败: {response.status} - {error_text}")
                    return {
                        "error": f"API请求失败: {response.status}",
                        "details": error_text
                    }
    except aiohttp.ClientError as e:
        logger.error(f"网络请求错误: {e}")
        return {"error": f"网络请求错误: {str(e)}"}
    except Exception as e:
        logger.error(f"未知错误: {e}")
        return {"error": f"未知错误: {str(e)}"}

@mcp.tool()
async def query_video_status(task_id: str) -> Dict[str, Any]:
    """
    查询视频生成状态
    
    Args:
        task_id: 视频生成任务ID
    
    Returns:
        包含任务状态信息的字典
    """
    if not task_id.strip():
        return {"error": "任务ID不能为空"}
    
    url = f"{API_BASE_URL}/get_status/{task_id}"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info(f"状态查询成功: {result}")
                    return result
                else:
                    error_text = await response.text()
                    logger.error(f"状态查询失败: {response.status} - {error_text}")
                    return {
                        "error": f"状态查询失败: {response.status}",
                        "details": error_text
                    }
    except aiohttp.ClientError as e:
        logger.error(f"网络请求错误: {e}")
        return {"error": f"网络请求错误: {str(e)}"}
    except Exception as e:
        logger.error(f"未知错误: {e}")
        return {"error": f"未知错误: {str(e)}"}

@mcp.tool()
async def get_video_result(task_id: str) -> Dict[str, Any]:
    """
    获取已完成视频的结果
    
    Args:
        task_id: 视频生成任务ID
    
    Returns:
        包含视频下载链接和相关信息的字典
    """
    if not task_id.strip():
        return {"error": "任务ID不能为空"}
    
    # 首先查询状态
    status_result = await query_video_status(task_id)
    
    if "error" in status_result:
        return status_result
    
    # 检查任务是否完成
    if status_result.get("status") == "completed":
        return {
            "task_id": task_id,
            "status": "completed",
            "video_url": status_result.get("video_url"),
            "thumbnail_url": status_result.get("thumbnail_url"),
            "duration": status_result.get("duration"),
            "created_at": status_result.get("created_at"),
            "completed_at": status_result.get("completed_at")
        }
    else:
        return {
            "task_id": task_id,
            "status": status_result.get("status", "unknown"),
            "message": "视频还未完成生成，请稍后再试"
        }

@mcp.tool()
async def health_check() -> Dict[str, Any]:
    """
    健康检查 - 检查服务器和API连接状态
    
    Returns:
        服务器状态信息
    """
    import time
    
    health_info = {
        "server_version": __version__,
        "server_status": "running",
        "timestamp": time.time(),
        "api_base_url": API_BASE_URL,
        "api_key_configured": API_KEY != "YOUR_API_KEY"
    }
    
    # 简单的API连通性测试
    try:
        async with aiohttp.ClientSession() as session:
            # 尝试访问API根路径或健康检查端点
            test_url = f"{API_BASE_URL.replace('/api', '')}"
            async with session.get(test_url, timeout=5) as response:
                health_info["api_connectivity"] = response.status < 500
                health_info["api_response_status"] = response.status
    except Exception as e:
        health_info["api_connectivity"] = False
        health_info["api_error"] = str(e)
    
    return health_info

# 启动服务器
if __name__ == "__main__":
    import asyncio
    
    # 检查API密钥
    if API_KEY == "YOUR_API_KEY":
        print("警告: 请设置环境变量 SCENEXT_API_KEY 或修改代码中的API_KEY")
    
    print("启动Scenext MCP服务器...")
    print(f"API密钥: {API_KEY[:10]}..." if len(API_KEY) > 10 else API_KEY)
    
    # 运行服务器
    mcp.run()



