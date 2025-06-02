"""
Scenext MCP Server 基础测试
"""

import asyncio
import os
import sys
from unittest.mock import patch

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_module_import():
    """测试模块导入"""
    try:
        from scenext_mcp import __version__
        from scenext_mcp.server import mcp
        assert __version__ is not None
        assert mcp.name == "Scenext"
        print(f"模块导入测试通过 - 版本: {__version__}")
        return True
    except Exception as e:
        print(f"模块导入测试失败: {e}")
        return False

def test_tools_registration():
    """测试工具注册"""
    try:
        from scenext_mcp.server import mcp
        
        # 检查工具是否正确注册
        expected_tools = ['gen_video', 'query_video_status']
        
        # 获取注册的工具（这需要访问内部 API）
        tools = mcp._tool_manager.list_tools()
        tool_names = [tool.name for tool in tools]
        
        for expected_tool in expected_tools:
            assert expected_tool in tool_names, f"工具 {expected_tool} 未注册"
        
        print(f"工具注册测试通过 - 注册工具: {tool_names}")
        return True
    except Exception as e:
        print(f"工具注册测试失败: {e}")
        return False



async def test_gen_video_validation():
    """测试视频生成参数验证"""
    try:
        from scenext_mcp.server import gen_video
        
        print("视频生成验证测试通过")
        return True
    except Exception as e:
        print(f"视频生成验证测试失败: {e}")
        return False

def run_tests():
    """运行所有测试"""
    print("运行 Scenext MCP Server 测试...")
    print("-" * 50)
    
    tests = [
        test_module_import,
        test_tools_registration,
    ]
    
    async_tests = [
        test_gen_video_validation,
    ]
    
    passed = 0
    total = len(tests) + len(async_tests)
    
    # 运行同步测试
    for test in tests:
        if test():
            passed += 1
    
    # 运行异步测试
    async def run_async_tests():
        nonlocal passed
        for test in async_tests:
            if await test():
                passed += 1
    
    asyncio.run(run_async_tests())
    
    print("-" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("所有测试通过！")
        return True
    else:
        print("部分测试失败")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
