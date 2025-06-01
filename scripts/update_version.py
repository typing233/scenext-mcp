#!/usr/bin/env python3
"""
版本更新脚本
用于自动更新包版本号和相关文件
"""

import os
import sys
import re
import argparse
from pathlib import Path
from datetime import datetime

# 获取项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
os.chdir(PROJECT_ROOT)

def get_current_version():
    """获取当前版本号"""
    version_file = PROJECT_ROOT / "scenext_mcp" / "_version.py"
    
    if not version_file.exists():
        return "1.0.0"
    
    with open(version_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正则表达式查找版本号
    match = re.search(r'__version__ = ["\']([^"\']+)["\']', content)
    if match:
        return match.group(1)
    
    return "1.0.0"

def parse_version(version_str):
    """解析版本号"""
    try:
        parts = version_str.split('.')
        return [int(p) for p in parts]
    except ValueError:
        raise ValueError(f"无效的版本号格式: {version_str}")

def bump_version(current_version, bump_type):
    """提升版本号"""
    major, minor, patch = parse_version(current_version)
    
    if bump_type == "patch":
        patch += 1
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    else:
        raise ValueError(f"无效的提升类型: {bump_type}")
    
    return f"{major}.{minor}.{patch}"

def update_version_file(new_version):
    """更新版本文件"""
    version_file = PROJECT_ROOT / "scenext_mcp" / "_version.py"
    
    with open(version_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正则表达式替换版本号
    new_content = re.sub(
        r'__version__ = ["\'][^"\']+["\']',
        f'__version__ = "{new_version}"',
        content
    )
    
    with open(version_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ 更新版本文件: {new_version}")

def update_changelog(new_version):
    """更新变更日志"""
    changelog_file = PROJECT_ROOT / "CHANGELOG.md"
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    new_entry = f"""## [{new_version}] - {current_date}

### Added
- 请在此添加新功能

### Changed
- 请在此添加变更内容

### Fixed
- 请在此添加修复内容

### Removed
- 请在此添加移除的功能

"""
    
    if changelog_file.exists():
        with open(changelog_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 在第一个## 之前插入新版本
        first_version_pos = content.find('\n## [')
        if first_version_pos != -1:
            content = content[:first_version_pos] + '\n' + new_entry + content[first_version_pos:]
        else:
            content += '\n' + new_entry
    else:
        # 创建新的变更日志
        content = f"""# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

{new_entry}"""
    
    with open(changelog_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 更新变更日志: {new_version}")

def update_publish_success(new_version):
    """更新发布成功文档"""
    success_file = PROJECT_ROOT / "PUBLISH_SUCCESS.md"
    
    if success_file.exists():
        with open(success_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 更新PyPI链接
        content = re.sub(
            r'https://pypi\.org/project/scenext-mcp/[\d\.]+/',
            f'https://pypi.org/project/scenext-mcp/{new_version}/',
            content
        )
        
        # 更新版本信息
        content = re.sub(
            r'scenext-mcp [\d\.]+',
            f'scenext-mcp {new_version}',
            content
        )
        
        # 更新发布历史
        current_date = datetime.now().strftime("%Y-%m-%d")
        new_history_entry = f"- **v{new_version}** ({current_date}): 版本更新\n  - 请添加此版本的更新内容\n\n"
        
        # 在发布历史部分添加新条目
        history_pos = content.find("## 发布历史")
        if history_pos != -1:
            next_section_pos = content.find("\n## ", history_pos + 1)
            if next_section_pos == -1:
                next_section_pos = content.find("\n---", history_pos + 1)
            
            if next_section_pos != -1:
                # 找到第一个版本条目的位置
                first_version_pos = content.find("- **v", history_pos)
                if first_version_pos != -1 and first_version_pos < next_section_pos:
                    content = content[:first_version_pos] + new_history_entry + content[first_version_pos:]
                else:
                    # 在发布历史标题后添加
                    insert_pos = content.find("\n", history_pos) + 1
                    content = content[:insert_pos] + "\n" + new_history_entry + content[insert_pos:]
        
        with open(success_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 更新发布成功文档: {new_version}")

def main():
    parser = argparse.ArgumentParser(description="更新包版本号")
    parser.add_argument(
        "bump_type",
        choices=["patch", "minor", "major"],
        help="版本提升类型"
    )
    parser.add_argument(
        "--version",
        help="直接指定版本号（忽略bump_type）"
    )
    parser.add_argument(
        "--no-changelog",
        action="store_true",
        help="不更新变更日志"
    )
    
    args = parser.parse_args()
    
    current_version = get_current_version()
    print(f"📦 当前版本: {current_version}")
    
    if args.version:
        new_version = args.version
        parse_version(new_version)  # 验证版本号格式
    else:
        new_version = bump_version(current_version, args.bump_type)
    
    print(f"🚀 新版本: {new_version}")
    
    # 更新版本文件
    update_version_file(new_version)
    
    # 更新变更日志
    if not args.no_changelog:
        update_changelog(new_version)
    
    # 更新发布成功文档
    update_publish_success(new_version)
    
    print(f"\n✅ 版本更新完成: {current_version} -> {new_version}")
    print("\n📋 接下来的步骤:")
    print("1. 编辑 CHANGELOG.md 添加具体的变更内容")
    print("2. 编辑 PUBLISH_SUCCESS.md 添加版本更新说明")
    print("3. 提交变更:")
    print(f"   git add .")
    print(f"   git commit -m \"chore: bump version to {new_version}\"")
    print(f"4. 创建标签: git tag v{new_version}")
    print("5. 推送变更: git push origin main --tags")
    print("6. 构建和发布: python scripts/publish.py")

if __name__ == "__main__":
    main()
