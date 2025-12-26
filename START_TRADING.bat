@echo off
REM Start trading with CURRENT strategy (no rate limits)
echo ========================================================================
echo 🎯 HIGH ACCURACY TRADING - CURRENT STRATEGY
echo ========================================================================
echo.
echo Running SINGLE strategy to avoid API rate limits
echo.
echo Strategy: CURRENT (Complex, Min Score 90)
echo Strikes: 30 (25400-26850)
echo Cycle Time: 3 minutes
echo.
echo ========================================================================
echo.

REM Activate virtual environment and run
call .venv\Scripts\activate.bat
python -u run_current_only.py

echo.
echo Press any key to exit...
pause >nul
