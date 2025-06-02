#!/usr/bin/env python3
"""
Scenext MCP Server - AI视频生成服务
支持生成教学视频
"""

from mcp.server.fastmcp import FastMCP
import aiohttp
import os
import sys
import argparse
from typing import List, Optional, Dict, Any
import logging
from dotenv import load_dotenv
from scenext_mcp._version import __version__
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

# 加载环境变量
load_dotenv()

# 全局变量存储运行时API Key
RUNTIME_API_KEY = None

def setup_logging():
    """配置日志"""
    log_level = os.getenv("SCENEXT_LOG_LEVEL", "INFO")
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

logger = setup_logging()


class APIKeyAuthMiddleware(BaseHTTPMiddleware):
    """API Key认证中间件"""
    
    def __init__(self, app, require_auth_for_sse: bool = True):
        super().__init__(app)
        self.require_auth_for_sse = require_auth_for_sse
        
    async def extract_api_key(self, request: Request) -> Optional[str]:
        """从请求中提取API key"""
        # 方法1: 从URL查询参数获取
        api_key = request.query_params.get("api_key")
        if api_key:
            return api_key
            
        # 方法2: 从Authorization header获取
        auth_header = request.headers.get("authorization", "")
        if auth_header.startswith("Bearer "):
            return auth_header[7:]
            
        # 方法3: 从X-API-Key header获取
        api_key_header = request.headers.get("x-api-key")
        if api_key_header:
            return api_key_header
            
        return None
    
    async def dispatch(self, request: Request, call_next):
        # 只对SSE和streamable-http端点进行认证
        if not self.require_auth_for_sse:
            return await call_next(request)
            
        # 检查是否是需要认证的端点
        path = request.url.path
        if path in ["/sse", "/mcp"]:
            api_key = await self.extract_api_key(request)
            
            if not api_key:
                logger.warning(f"缺少API key: {path}")
                return JSONResponse(
                    {"error": "API key is required. Provide it via ?api_key=xxx, Authorization header, or X-API-Key header"},
                    status_code=401
                )
            
                
            # 将API key存储到全局变量中供工具函数使用
            global RUNTIME_API_KEY
            RUNTIME_API_KEY = api_key
            logger.info(f"API key获取成功: {api_key[:10]}...")
        
        response = await call_next(request)
        return response   

# 创建MCP服务器
mcp = FastMCP(
    "Scenext", 
    description=f"Scenext视频生成服务器 v{__version__} - 提供视频生成和状态查询功能",
    host="0.0.0.0",
    port=8000
)


# 配置
API_BASE_URL = "https://api.scenext.cn/api"
API_KEY = os.getenv("SCENEXT_API_KEY", "YOUR_API_KEY")
DEFAULT_QUALITY = os.getenv("SCENEXT_DEFAULT_QUALITY", "m")

def get_api_key():
    """获取API Key，优先使用运行时传入的"""
    return RUNTIME_API_KEY if RUNTIME_API_KEY else API_KEY

@mcp.tool()
async def gen_video(
    question: str = "",
    answer: str = "",
    question_images: Optional[List[str]] = None,
    answer_images: Optional[List[str]] = None,
    quality: str = DEFAULT_QUALITY
) -> Dict[str, Any]:
    """
    生成教学讲解视频
    
    Args:
        question: 问题内容（文本形式），question和questionImages中至少输入一个
        answer: 参考答案（文本形式）：确保生成的讲解内容准确（可选）
        question_images: 问题内容（图片形式），输入图片的URL或者base64（可选）
        answer_images: 参考答案（图片形式），输入图片的URL或者base64（可选）
        quality: 视频质量，可选值：l(低)、m(中)、h(高)，默认为配置的默认质量
    
    Returns:
        包含任务ID的字典
    """
    current_api_key = get_api_key()
    if current_api_key == "YOUR_API_KEY":
        return {"error": "请提供有效的API Key,若无API KEY请到scenext.cn平台申请"}
    # 验证至少有question或questionImages其中一个
    if not question.strip() and not (question_images and len(question_images) > 0):
        return {"error": "question和questionImages中至少输入一个"}
    
    url = f"{API_BASE_URL}/gen_video"
    headers = {
        "Authorization": f"Bearer {current_api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "question": question,
        "answer": answer,
        "questionImages": question_images or [],
        "answerImages": answer_images or [],
        "quality": quality,
    }


    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info(f"视频生成请求成功: {result}")
                    
                    # 根据API文档处理响应格式
                    if result.get("status") == "success":
                        return {
                            "status": "success",
                            "task_id": result.get("data", {}).get("task_id"),
                            "message": "视频生成任务创建成功"
                        }
                    else:
                        return {
                            "error": "API返回错误状态",
                            "details": result
                        }
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
        包含任务状态信息与任务结果的字典
        状态说明：
        - IN_PROGRESS: 任务正在处理中，可以继续轮询
        - COMPLETED: 任务已成功完成，返回信息会包含生成结果
        - FAILED: 任务处理失败，请检查错误信息
    """
    current_api_key = get_api_key()
    if current_api_key == "YOUR_API_KEY":
        return {"error": "请提供有效的API Key,若无API KEY请到scenext.cn平台申请"}
    if not task_id.strip():
        return {"error": "任务ID不能为空"}
    
    url = f"{API_BASE_URL}/get_status/{task_id}"
    headers = {
        "Authorization": f"Bearer {current_api_key}"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info(f"状态查询成功: {result}")
                    
                    # 根据API文档处理响应格式
                    if result.get("status") == "success":
                        return result.get("data", {})
                    else:
                        return {
                            "error": "API返回错误状态",
                            "details": result
                        }
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

def add_auth_middleware_to_app(transport_type: str, enable_auth: bool = True):
    """为指定的transport添加认证中间件"""
    if not enable_auth or transport_type == "stdio":
        return
        
    if transport_type == "sse":
        # 获取SSE应用并添加中间件
        sse_app = mcp.sse_app()
        sse_app.add_middleware(APIKeyAuthMiddleware, require_auth_for_sse=True)
        # 重新设置sse_app方法以返回带中间件的应用
        original_sse_app = mcp.sse_app
        mcp.sse_app = lambda mount_path=None: sse_app
        
    elif transport_type == "streamable-http":
        # 获取Streamable HTTP应用并添加中间件
        http_app = mcp.streamable_http_app()
        http_app.add_middleware(APIKeyAuthMiddleware, require_auth_for_sse=True)
        # 重新设置streamable_http_app方法以返回带中间件的应用
        original_http_app = mcp.streamable_http_app
        mcp.streamable_http_app = lambda: http_app

def main():
    """CLI入口点"""
    parser = argparse.ArgumentParser(
        description="Scenext MCP Server - AI视频生成服务",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  scenext-mcp                          # 使用默认配置启动
  scenext-mcp --log-level DEBUG       # 启用调试日志
  
环境变量配置:
  SCENEXT_API_KEY         - Scenext API密钥（必填）
  SCENEXT_DEFAULT_QUALITY - 默认视频质量：l/m/h（可选）
  SCENEXT_LOG_LEVEL       - 日志级别（可选）

SSE接入方式:
  在MCP客户端配置中使用: https://mcp.scenext.cn/sse?api_key=YOUR_API_KEY
        """
    )

    # 添加位置参数用于指定transport类型
    parser.add_argument(
        'transport', 
        nargs='?', 
        default='stdio', 
        choices=['stdio', 'sse', 'streamable-http'],
        help='传输类型 (stdio用于本地uvx, sse用于远程部署)'
    )
    
    parser.add_argument(
        "--log-level", 
        choices=["DEBUG", "INFO", "WARNING", "ERROR"], 
        default=os.getenv("SCENEXT_LOG_LEVEL", "INFO"),
        help="日志级别"
    )
    
    parser.add_argument(
        "--version", 
        action="version", 
        version=f"scenext-mcp {__version__}"
    )
    
    args = parser.parse_args()
    
    # 设置日志级别
    os.environ["SCENEXT_LOG_LEVEL"] = args.log_level
    
    # 重新配置日志
    global logger
    logger = setup_logging()
    
    if args.transport == "stdio":
        # STDIO模式：用于本地uvx调用
        logger.info(f"启动Scenext MCP服务器 v{__version__} (STDIO模式)")
        print(f"API密钥: {API_KEY[:10]}..." if len(API_KEY) > 10 else "未配置")
    elif args.transport == "sse":
        print(f"启动Scenext MCP服务器 v{__version__}")
        print(f"传输方式: SSE (远程接入)")
        print(f"API地址: {API_BASE_URL}")
        print(f"日志级别: {args.log_level}")
        print(f"默认质量: {DEFAULT_QUALITY}")
        print("-" * 60)
        add_auth_middleware_to_app("sse", True)
    elif args.transport == "streamable-http":
        print(f"启动Scenext MCP服务器 v{__version__}")
        print(f"传输方式: streamable-http (远程接入)")
        print(f"API地址: {API_BASE_URL}")
        print(f"日志级别: {args.log_level}")
        print(f"默认质量: {DEFAULT_QUALITY}")
        print("-" * 60)
        add_auth_middleware_to_app("streamable-http", True)
    
    try:
        mcp.run(transport=args.transport)
    except KeyboardInterrupt:
        if args.transport != "stdio":
            print("\n服务器已停止")
    except Exception as e:
        logger.error(f"服务器启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()