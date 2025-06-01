from setuptools import setup, find_packages
import os

# 读取README文件
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# 读取requirements文件
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="scenext-mcp",
    version="1.0.0",
    author="Scenext Developer",
    author_email="developer@scenext.cn",
    description="Scenext MCP Server - AI视频生成服务的模型上下文协议服务器",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/scenext/scenext-mcp",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Multimedia :: Video",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "scenext-mcp=scenext_mcp.server:main",
        ],
    },
    include_package_data=True,
    package_data={
        "scenext_mcp": ["*.json", "*.md"],
    },
    keywords="mcp, model-context-protocol, ai, video, generation, scenext",
    project_urls={
        "Bug Reports": "https://github.com/scenext/scenext-mcp/issues",
        "Source": "https://github.com/scenext/scenext-mcp",
        "Documentation": "https://github.com/scenext/scenext-mcp#readme",
    },
)
