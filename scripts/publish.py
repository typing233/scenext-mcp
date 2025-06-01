#!/usr/bin/env python3
"""
自动化发布脚本
用于构建和发布包到PyPI
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import argparse

# 获取项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
os.chdir(PROJECT_ROOT)

def run_command(cmd, check=True, shell=True):
    """运行命令"""
    print(f"🔧 执行: {cmd}")
    
    if shell and sys.platform == "win32":
        # Windows PowerShell
        result = subprocess.run(
            ["powershell", "-Command", cmd],
            capture_output=True,
            text=True
        )
    else:
        result = subprocess.run(cmd, shell=shell, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout.strip())
    
    if result.returncode != 0 and check:
        print(f"❌ 命令失败: {cmd}")
        if result.stderr:
            print(f"错误: {result.stderr.strip()}")
        sys.exit(1)
    
    return result

def clean_build():
    """清理构建文件"""
    print("🧹 清理旧构建文件...")
    
    dirs_to_clean = ["build", "dist", "*.egg-info"]
    for pattern in dirs_to_clean:
        for path in PROJECT_ROOT.glob(pattern):
            if path.is_dir():
                try:
                    shutil.rmtree(path)
                    print(f"   ✅ 删除目录: {path.name}")
                except Exception as e:
                    print(f"   ⚠️  无法删除 {path.name}: {e}")
            elif path.is_file():
                try:
                    path.unlink()
                    print(f"   ✅ 删除文件: {path.name}")
                except Exception as e:
                    print(f"   ⚠️  无法删除 {path.name}: {e}")

def check_environment():
    """检查环境和依赖"""
    print("🔍 检查构建环境...")
    
    # 检查Python版本
    python_version = sys.version_info
    if python_version < (3, 8):
        print(f"❌ Python版本过低: {python_version}，需要 >= 3.8")
        sys.exit(1)
    
    print(f"✅ Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")

def install_build_tools():
    """安装构建工具"""
    print("📦 检查构建工具...")
    
    required_packages = ["build", "twine"]
    for package in required_packages:
        result = run_command(f"python -m pip show {package}", check=False)
        if result.returncode != 0:
            print(f"📥 安装 {package}...")
            run_command(f"python -m pip install {package}")
        else:
            print(f"✅ {package} 已安装")

def get_current_version():
    """获取当前版本"""
    try:
        sys.path.insert(0, str(PROJECT_ROOT))
        from scenext_mcp._version import __version__
        return __version__
    except ImportError as e:
        print(f"❌ 无法获取版本信息: {e}")
        return "unknown"

def build_package():
    """构建包"""
    print("🔨 构建包...")
    run_command("python -m build")
    
    # 检查生成的文件
    dist_dir = PROJECT_ROOT / "dist"
    if dist_dir.exists():
        files = list(dist_dir.glob("*"))
        print(f"✅ 构建完成，生成 {len(files)} 个文件:")
        for file in files:
            print(f"   📦 {file.name}")
    else:
        print("❌ 构建失败，未找到dist目录")
        sys.exit(1)

def check_package():
    """检查包"""
    print("🔍 检查包质量...")
    result = run_command("python -m twine check dist/*")
    if result.returncode == 0:
        print("✅ 包检查通过")
    else:
        print("❌ 包检查失败")
        sys.exit(1)

def upload_to_testpypi():
    """上传到TestPyPI"""
    print("🧪 上传到TestPyPI...")
    result = run_command("python -m twine upload --repository testpypi dist/*", check=False)
    return result.returncode == 0

def upload_to_pypi():
    """上传到PyPI"""
    print("🚀 上传到PyPI...")
    result = run_command("python -m twine upload dist/*", check=False)
    return result.returncode == 0

def verify_upload(package_name, version, test=False):
    """验证上传是否成功"""
    base_url = "https://test.pypi.org" if test else "https://pypi.org"
    package_url = f"{base_url}/project/{package_name}/{version}/"
    
    print(f"🔗 包页面: {package_url}")
    
    if test:
        print("📋 测试安装命令:")
        print(f"   pip install -i https://test.pypi.org/simple/ {package_name}=={version}")
    else:
        print("📋 安装命令:")
        print(f"   pip install {package_name}=={version}")
        print(f"   uvx {package_name}")

def main():
    parser = argparse.ArgumentParser(description="自动化包发布")
    parser.add_argument(
        "--test-only",
        action="store_true",
        help="只发布到TestPyPI"
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="跳过构建步骤"
    )
    parser.add_argument(
        "--skip-check",
        action="store_true",
        help="跳过包检查"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="强制发布，不询问确认"
    )
    
    args = parser.parse_args()
    
    version = get_current_version()
    print(f"📦 准备发布版本: {version}")
    print("=" * 60)
    
    try:
        # 检查环境
        check_environment()
        
        # 安装构建工具
        install_build_tools()
        
        if not args.skip_build:
            # 清理旧文件
            clean_build()
            
            # 构建包
            build_package()
        
        if not args.skip_check:
            # 检查包
            check_package()
        
        # 发布流程
        if args.test_only:
            if not args.force:
                response = input("📤 是否上传到TestPyPI? (y/N): ")
                if response.lower() != 'y':
                    print("❌ 取消发布")
                    return
            
            if upload_to_testpypi():
                print("✅ TestPyPI 上传成功！")
                verify_upload("scenext-mcp", version, test=True)
            else:
                print("❌ TestPyPI 上传失败")
                sys.exit(1)
        else:
            # 先上传到TestPyPI
            if not args.force:
                response = input("📤 是否先上传到TestPyPI进行测试? (Y/n): ")
                if response.lower() != 'n':
                    if upload_to_testpypi():
                        print("✅ TestPyPI 上传成功！")
                        verify_upload("scenext-mcp", version, test=True)
                        
                        test_response = input("🧪 是否从TestPyPI测试安装? (Y/n): ")
                        if test_response.lower() != 'n':
                            print("请在另一个终端中运行测试安装命令，然后回来继续...")
                            input("按回车键继续发布到正式PyPI...")
                    else:
                        print("❌ TestPyPI 上传失败")
                        sys.exit(1)
            
            # 发布到正式PyPI
            if not args.force:
                response = input("🚀 是否发布到正式PyPI? (y/N): ")
                if response.lower() != 'y':
                    print("❌ 取消发布")
                    return
            
            if upload_to_pypi():
                print("🎉 PyPI 发布成功！")
                verify_upload("scenext-mcp", version, test=False)
                
                print("\n🎊 发布完成！")
                print("📋 后续步骤:")
                print("1. 更新PUBLISH_SUCCESS.md文档")
                print("2. 创建GitHub Release")
                print("3. 通知用户新版本发布")
            else:
                print("❌ PyPI 上传失败")
                sys.exit(1)
                
    except KeyboardInterrupt:
        print("\n❌ 发布被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 发布过程中出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
