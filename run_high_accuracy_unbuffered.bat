@echo off
REM Run High Accuracy Trading Algorithm
echo ========================================================================
echo 🎯 HIGH ACCURACY TRADING ALGORITHM
echo ========================================================================
echo.
echo Choose your strategy:
echo   1. CURRENT (Complex, Min Score 90)
echo   2. SIMPLIFIED (Price Action, Min Score 70)
echo.
echo ========================================================================
echo.

REM Activate virtual environment and run with unbuffered output
call .venv\Scripts\activate.bat
python -u run_high_accuracy.py

echo.
echo Press any key to exit...
pause >nul
