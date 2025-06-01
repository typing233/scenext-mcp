# Scenext MCP 包更新脚本
# PowerShell版本的便捷更新工具

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("patch", "minor", "major")]
    [string]$BumpType,
    
    [string]$Version,
    [switch]$NoChangelog,
    [switch]$TestOnly,
    [switch]$Force
)

Write-Host "🔄 Scenext MCP 版本更新工具" -ForegroundColor Green
Write-Host "=" * 50

# 确保在正确的目录
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir
Set-Location $projectRoot

Write-Host "📁 项目目录: $projectRoot" -ForegroundColor Gray

# 激活虚拟环境
if (Test-Path "myenv\Scripts\Activate.ps1") {
    Write-Host "🔧 激活虚拟环境..." -ForegroundColor Yellow
    & "myenv\Scripts\Activate.ps1"
} else {
    Write-Warning "未找到虚拟环境，使用系统Python"
}

try {
    # 第一步：更新版本
    Write-Host "`n📦 更新版本号..." -ForegroundColor Cyan
    
    $versionArgs = @($BumpType)
    if ($Version) {
        $versionArgs = @("patch", "--version", $Version)
    }
    if ($NoChangelog) {
        $versionArgs += "--no-changelog"
    }
    
    & python scripts/update_version.py @versionArgs
    
    if ($LASTEXITCODE -ne 0) {
        throw "版本更新失败"
    }
    
    # 第二步：询问是否继续发布
    if (-not $Force) {
        $response = Read-Host "`n🚀 是否立即构建并发布新版本? (y/N)"
        if ($response -ne "y" -and $response -ne "Y") {
            Write-Host "✅ 版本更新完成。稍后可运行以下命令发布:" -ForegroundColor Green
            Write-Host "   python scripts/publish.py" -ForegroundColor White
            return
        }
    }
    
    # 第三步：发布
    Write-Host "`n🔨 构建并发布包..." -ForegroundColor Cyan
    
    $publishArgs = @()
    if ($TestOnly) {
        $publishArgs += "--test-only"
    }
    if ($Force) {
        $publishArgs += "--force"
    }
    
    & python scripts/publish.py @publishArgs
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n🎉 发布成功！" -ForegroundColor Green
    } else {
        throw "发布失败"
    }
    
} catch {
    Write-Host "`n❌ 错误: $_" -ForegroundColor Red
    exit 1
}

Write-Host "`n✨ 操作完成！" -ForegroundColor Green
