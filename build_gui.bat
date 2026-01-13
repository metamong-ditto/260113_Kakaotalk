@echo off
chcp 65001 >nul
echo ========================================
echo   Building GUI version...
echo ========================================
echo.

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Building with spec file...
pyinstaller --clean kakao_openchat_gui.spec

echo.
echo ========================================
echo   Build completed!
echo   Output: dist\kakao_openchat_gui.exe
echo ========================================
pause
