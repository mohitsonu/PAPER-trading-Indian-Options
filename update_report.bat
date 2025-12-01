@echo off
echo ========================================
echo   UPDATING TRADING REPORT
echo ========================================
echo.

REM Run the Python script to generate fresh report
python generate_dynamic_report.py

echo.
echo ========================================
echo   REPORT UPDATED!
echo ========================================
echo.
echo Opening report in browser...
echo.

REM Open the report in default browser
start trading_report.html

echo.
echo Press any key to close this window...
pause >nul
