@echo off
echo ========================================
echo Prompt Engineering MCP Server Setup
echo ========================================
echo.

echo [1/3] Installing dependencies...
call npm install
if errorlevel 1 (
    echo ERROR: npm install failed
    pause
    exit /b 1
)
echo.

echo [2/3] Building TypeScript...
call npm run build
if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)
echo.

echo [3/3] Setup complete!
echo.
echo ========================================
echo Next Steps:
echo ========================================
echo.
echo 1. Add this to your Claude Desktop config:
echo    File: %%APPDATA%%\Claude\claude_desktop_config.json
echo.
echo {
echo   "mcpServers": {
echo     "prompt-engineering": {
echo       "command": "node",
echo       "args": ["%~dp0dist\index.js"]
echo     }
echo   }
echo }
echo.
echo 2. Restart Claude Desktop completely
echo.
echo 3. Test by asking Claude to list frameworks
echo.
echo ========================================
pause
