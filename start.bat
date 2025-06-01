@echo off
echo 启动Scenext MCP服务器...
cd /d "d:\Scenext-MCP"
call myenv\Scripts\activate
python app.py
pause
