@echo off
chcp 65001 >nul
REM Windows Build Script
REM Usage: build.bat

echo ========================================
echo Kakao OpenChat Member Counter - Build
echo ========================================
echo.

REM Activate virtual environment if exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Build
echo.
echo Starting build...
python build.py --clean

echo.
echo Done! Check kakao_openchat.exe in dist folder.
pause
