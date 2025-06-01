"""
版本管理模块
遵循语义化版本控制 (Semantic Versioning)
"""

# 版本格式: MAJOR.MINOR.PATCH
# MAJOR: 重大破坏性变更
# MINOR: 新功能，向后兼容
# PATCH: 错误修复，向后兼容

__version__ = "1.0.0"

def get_version():
    """获取当前版本号"""
    return __version__

def bump_patch():
    """提升补丁版本号 (1.0.0 -> 1.0.1)"""
    major, minor, patch = __version__.split('.')
    return f"{major}.{minor}.{int(patch) + 1}"

def bump_minor():
    """提升次版本号 (1.0.0 -> 1.1.0)"""
    major, minor, patch = __version__.split('.')
    return f"{major}.{int(minor) + 1}.0"

def bump_major():
    """提升主版本号 (1.0.0 -> 2.0.0)"""
    major, minor, patch = __version__.split('.')
    return f"{int(major) + 1}.0.0"
