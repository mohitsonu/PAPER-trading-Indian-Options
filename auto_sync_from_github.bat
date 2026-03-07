@echo off
echo ========================================
echo Auto-Sync Trading Files from GitHub
echo ========================================
echo.
echo This will pull files from GitHub every 5 minutes
echo Press Ctrl+C to stop
echo.
pause

:loop
echo.
echo [%date% %time%] Pulling latest files from GitHub...
git pull origin main

if %errorlevel% equ 0 (
    echo [%date% %time%] ✅ Files synced successfully!
    echo You can now view trading_report.html
) else (
    echo [%date% %time%] ⚠️ Sync failed
)

echo.
echo Waiting 5 minutes before next sync...
timeout /t 300 /nobreak > nul
goto loop
