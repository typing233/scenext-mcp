# PowerShell启动脚本
Write-Host "启动Scenext MCP服务器..." -ForegroundColor Green
Set-Location "d:\Scenext-MCP"
& "myenv\Scripts\Activate.ps1"
python app.py
