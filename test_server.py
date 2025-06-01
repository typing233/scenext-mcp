#!/usr/bin/env python3
"""
Scenext MCP服务器测试脚本
"""
import asyncio
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import gen_video, query_video_status, get_video_result

async def test_video_generation():
    """测试视频生成功能"""
    print("🎬 测试视频生成功能...")
    
    result = await gen_video(
        question="什么是机器学习？",
        answer="机器学习是人工智能的一个分支，通过算法和统计模型让计算机从数据中学习模式。",
        quality="m"
    )
    
    print(f"生成结果: {result}")
    
    if "task_id" in result:
        task_id = result["task_id"]
        print(f"✅ 视频生成请求成功，任务ID: {task_id}")
        return task_id
    else:
        print(f"❌ 视频生成请求失败: {result.get('error', '未知错误')}")
        return None

async def test_status_query(task_id):
    """测试状态查询功能"""
    if not task_id:
        print("⏭️ 跳过状态查询测试（没有有效的任务ID）")
        return
    
    print("📊 测试状态查询功能...")
    
    status = await query_video_status(task_id)
    print(f"状态查询结果: {status}")
    
    if "error" in status:
        print(f"❌ 状态查询失败: {status['error']}")
    else:
        print(f"✅ 状态查询成功，当前状态: {status.get('status', '未知')}")

async def test_result_retrieval(task_id):
    """测试结果获取功能"""
    if not task_id:
        print("⏭️ 跳过结果获取测试（没有有效的任务ID）")
        return
    
    print("📁 测试结果获取功能...")
    
    result = await get_video_result(task_id)
    print(f"结果获取: {result}")
    
    if "error" in result:
        print(f"❌ 结果获取失败: {result['error']}")
    else:
        print(f"✅ 结果获取成功")

async def main():
    """主测试函数"""
    print("🚀 开始测试Scenext MCP服务器")
    print("=" * 50)
    
    # 检查API密钥配置
    from app import API_KEY
    if API_KEY == "YOUR_API_KEY":
        print("⚠️  警告: API密钥未配置，测试可能会失败")
        print("请在.env文件中设置SCENEXT_API_KEY")
    else:
        print(f"🔑 API密钥已配置: {API_KEY[:10]}...")
    
    print()
    
    # 测试视频生成
    task_id = await test_video_generation()
    print()
    
    # 测试状态查询
    await test_status_query(task_id)
    print()
    
    # 测试结果获取
    await test_result_retrieval(task_id)
    print()
    
    print("=" * 50)
    print("🏁 测试完成")

if __name__ == "__main__":
    asyncio.run(main())
