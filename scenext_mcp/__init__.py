"""
Scenext MCP Server Package
AI视频生成服务的模型上下文协议服务器

这个包提供了与Scenext AI视频生成平台集成的MCP服务器，
允许通过模型上下文协议生成教学视频。
"""

from ._version import __version__

__author__ = "Scenext"
__email__ = "support@lynkframe.com"
__description__ = "Scenext MCP Server - AI视频生成服务的模型上下文协议服务器"

from scenext_mcp.server import main

__all__ = ["main", "__version__"]
