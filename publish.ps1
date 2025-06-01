#!/usr/bin/env powershell
<#
.SYNOPSIS
    发布Scenext MCP包到PyPI

.DESCRIPTION
    这个脚本会构建和发布Scenext MCP包到PyPI，包括TestPyPI和正式PyPI

.EXAMPLE
    .\publish.ps1
#>

Write-Host "🚀 发布Scenext MCP包到PyPI" -ForegroundColor Green
Write-Host "=" * 60

# 检查API令牌配置
$pypirc_path = "$env:USERPROFILE\.pypirc"
if (!(Test-Path $pypirc_path)) {
    Write-Host "⚠️  未找到API令牌配置文件" -ForegroundColor Yellow
    Write-Host "请先运行令牌设置脚本：.\setup_tokens.ps1" -ForegroundColor Cyan
    $answer = Read-Host "是否现在运行设置脚本？(y/N)"
    if ($answer -eq "y" -or $answer -eq "Y") {
        .\setup_tokens.ps1
        if ($LASTEXITCODE -ne 0) {
            exit 1
        }
    } else {
        Write-Host "❌ 需要先配置API令牌才能发布" -ForegroundColor Red
        exit 1
    }
}

# 检查虚拟环境
if (!(Test-Path "myenv\Scripts\activate.ps1")) {
    Write-Error "❌ 虚拟环境不存在，请先创建虚拟环境"
    exit 1
}

# 激活虚拟环境
Write-Host "📦 激活虚拟环境..." -ForegroundColor Yellow
& "myenv\Scripts\Activate.ps1"

# 检查构建工具
Write-Host "🔧 检查构建工具..." -ForegroundColor Yellow
$buildInstalled = python -c "import build; print('ok')" 2>$null
$twineInstalled = python -c "import twine; print('ok')" 2>$null

if ($buildInstalled -ne "ok" -or $twineInstalled -ne "ok") {
    Write-Host "📥 安装构建工具..." -ForegroundColor Yellow
    python -m pip install build twine --upgrade
}

# 清理旧文件
Write-Host "🧹 清理旧构建文件..." -ForegroundColor Yellow
Remove-Item -Recurse -Force build, dist, scenext_mcp.egg-info -ErrorAction SilentlyContinue

# 构建包
Write-Host "🔨 构建包..." -ForegroundColor Yellow
python -m build

if ($LASTEXITCODE -ne 0) {
    Write-Error "❌ 包构建失败"
    exit 1
}

# 检查包质量
Write-Host "🔍 检查包质量..." -ForegroundColor Yellow
python -m twine check dist/*

if ($LASTEXITCODE -ne 0) {
    Write-Error "❌ 包质量检查失败"
    exit 1
}

# 显示构建的文件
Write-Host "📁 构建完成的文件:" -ForegroundColor Green
Get-ChildItem dist\ | ForEach-Object { Write-Host "   $($_.Name)" -ForegroundColor Cyan }

# 询问是否上传到TestPyPI
Write-Host ""
$uploadTest = Read-Host "🧪 是否上传到TestPyPI进行测试? (y/N)"
if ($uploadTest -eq "y" -or $uploadTest -eq "Y") {
    Write-Host "📤 上传到TestPyPI..." -ForegroundColor Yellow
    python -m twine upload --repository testpypi dist/*
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ TestPyPI上传成功！" -ForegroundColor Green
        Write-Host "🔗 测试链接: https://test.pypi.org/project/scenext-mcp/" -ForegroundColor Cyan
        Write-Host "📦 测试安装: pip install -i https://test.pypi.org/simple/ scenext-mcp" -ForegroundColor Cyan
    }
}

# 询问是否上传到正式PyPI
Write-Host ""
$uploadProd = Read-Host "🚀 是否上传到正式PyPI? (y/N)"
if ($uploadProd -eq "y" -or $uploadProd -eq "Y") {
    Write-Host "📤 上传到PyPI..." -ForegroundColor Yellow
    python -m twine upload dist/*
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "🎉 发布成功！" -ForegroundColor Green -BackgroundColor DarkGreen
        Write-Host "=" * 60
        Write-Host "📦 包名: scenext-mcp" -ForegroundColor Cyan
        Write-Host "🔗 PyPI链接: https://pypi.org/project/scenext-mcp/" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "💡 用户现在可以使用以下方式安装:" -ForegroundColor Yellow
        Write-Host "   pip install scenext-mcp" -ForegroundColor White
        Write-Host "   uvx scenext-mcp" -ForegroundColor White
        Write-Host ""
        Write-Host "🎯 MCP配置示例:" -ForegroundColor Yellow
        Write-Host @"
{
  "mcpServers": {
    "scenext": {
      "command": "uvx", 
      "args": ["scenext-mcp", "-y"],
      "env": {
        "SCENEXT_API_KEY": "your_actual_api_key_here",
        "SCENEXT_DEFAULT_QUALITY": "h"
      }
    }
  }
}
"@ -ForegroundColor White
    } else {
        Write-Error "❌ PyPI上传失败"
    }
}

Write-Host ""
Write-Host "📋 发布流程完成！" -ForegroundColor Green
