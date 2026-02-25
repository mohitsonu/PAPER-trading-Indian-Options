@echo off
REM ========================================
REM AUTO TRADER SCHEDULER - WINDOWS STARTUP
REM ========================================
REM This script starts the automatic trading scheduler
REM The scheduler will run the algorithm during market hours
REM Monday-Friday: 9:15 AM - 3:30 PM

echo.
echo ========================================
echo   AUTO TRADER SCHEDULER
echo ========================================
echo.
echo Starting automatic trading scheduler...
echo.
echo The algorithm will:
echo   - Start automatically at 9:15 AM
echo   - Stop automatically at 3:30 PM
echo   - Run Monday to Friday only
echo   - Restart if it crashes
echo.
echo Press Ctrl+C to stop the scheduler
echo.
echo ========================================
echo.

REM Activate virtual environment if it exists
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)

REM Run the scheduler
python auto_trader_scheduler.py

pause
