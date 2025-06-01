# 设置PyPI API令牌的交互式脚本
# Setup PyPI API Token Interactive Script

Write-Host "🔑 PyPI API令牌设置向导" -ForegroundColor Green
Write-Host "=" * 50

$pypirc_path = "$env:USERPROFILE\.pypirc"

Write-Host "`n📋 说明：" -ForegroundColor Yellow
Write-Host "1. 你需要在 https://pypi.org/manage/account/token/ 创建API令牌"
Write-Host "2. 令牌名称建议：scenext-mcp-upload"
Write-Host "3. 范围选择：Entire account (或项目创建后选择特定项目)"
Write-Host "4. TestPyPI令牌在 https://test.pypi.org/manage/account/token/ 创建"

Write-Host "`n请输入你的API令牌：" -ForegroundColor Cyan

# 获取PyPI令牌
$pypi_token = Read-Host "PyPI API令牌 (以pypi-开头)"
if ([string]::IsNullOrWhiteSpace($pypi_token)) {
    Write-Host "❌ PyPI令牌不能为空" -ForegroundColor Red
    exit 1
}

# 获取TestPyPI令牌（可选）
Write-Host "`n测试PyPI令牌（可选，用于测试发布）："
$testpypi_token = Read-Host "TestPyPI API令牌 (按Enter跳过)"

# 创建.pypirc内容
$pypirc_content = @"
[distutils]
index-servers = 
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = $pypi_token

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = $testpypi_token
"@

# 写入文件
try {
    $pypirc_content | Out-File -FilePath $pypirc_path -Encoding UTF8
    Write-Host "`n✅ API令牌配置成功！" -ForegroundColor Green
    Write-Host "配置文件位置: $pypirc_path" -ForegroundColor Gray
    
    # 设置文件权限（仅当前用户可读）
    $acl = Get-Acl $pypirc_path
    $acl.SetAccessRuleProtection($true, $false)
    $accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule(
        $env:USERNAME, "FullControl", "Allow"
    )
    $acl.SetAccessRule($accessRule)
    Set-Acl $pypirc_path $acl
    
    Write-Host "🔒 文件权限已设置为仅当前用户可访问" -ForegroundColor Green
    
    Write-Host "`n🚀 现在你可以运行发布脚本：" -ForegroundColor Yellow
    Write-Host ".\publish.ps1" -ForegroundColor White
    
} catch {
    Write-Host "❌ 配置失败: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "`n📝 下一步：" -ForegroundColor Cyan
Write-Host "1. 运行 .\publish.ps1 发布包到PyPI"
Write-Host "2. 或者手动运行：python -m twine upload dist/*"
