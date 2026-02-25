@echo off
REM ========================================
REM PUSH TRADE JOURNAL TO GITHUB
REM ========================================

echo.
echo ========================================
echo   PUSH TRADE JOURNAL TO GITHUB
echo ========================================
echo.
echo This will upload your organized trade journal to GitHub
echo.
echo Files to be uploaded:
echo   - trade_journal/csv/ (64 CSV files)
echo   - trade_journal/json/ (68 JSON files)
echo   - trade_journal/logs/ (folder)
echo   - trade_journal/README.md
echo.
echo ========================================
echo.

pause

echo.
echo Adding files to git...
git add trade_journal/

echo.
echo Committing files...
git commit -m "📊 Organize trade journal - Move all CSV and JSON files to organized folders"

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo   ✅ DONE!
echo ========================================
echo.
echo Your trade journal has been uploaded to GitHub!
echo.
echo To view:
echo 1. Go to your GitHub repository
echo 2. Click on "trade_journal" folder
echo 3. Browse csv/ and json/ folders
echo.
echo ========================================
echo.

pause
