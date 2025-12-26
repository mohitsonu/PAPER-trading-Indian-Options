@echo off
REM Start the optimized trading algorithm (CONTRARIAN only)
echo ========================================================================
echo 🎯 STARTING OPTIMIZED TRADING ALGORITHM
echo ========================================================================
echo.
echo Strategy: CONTRARIAN (Only profitable strategy)
echo Win Rate: 41.3%% | Total P&L: +Rs.23,346
echo.
echo All losing strategies have been disabled!
echo.
echo ========================================================================
echo.

REM Activate virtual environment and run
call .venv\Scripts\activate.bat
python -u run_high_accuracy.py

echo.
echo Press any key to exit...
pause >nul
