@echo off
REM Run single strategy (choose CURRENT or SIMPLIFIED)
echo ========================================================================
echo 🎯 SINGLE STRATEGY RUNNER
echo ========================================================================
echo.

REM Activate virtual environment and run
call .venv\Scripts\activate.bat
python -u run_single_strategy.py

echo.
echo Press any key to exit...
pause >nul
