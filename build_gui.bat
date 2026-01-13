@echo off
chcp 65001 >nul
echo ========================================
echo   Building GUI version...
echo ========================================
echo.

echo [Step 1/3] Installing dependencies...
pip install --upgrade pip
pip install pyautogui pyscreeze mouseinfo pygetwindow pyrect pywinauto pyperclip pillow pytesseract pyinstaller

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)

echo.
echo [Step 2/3] Verifying pyautogui installation...
python -c "import pyautogui; print('pyautogui OK:', pyautogui.__version__)"

if %errorlevel% neq 0 (
    echo.
    echo ERROR: pyautogui not properly installed!
    pause
    exit /b 1
)

echo.
echo [Step 3/3] Building with spec file...
pyinstaller --clean --noconfirm kakao_openchat_gui.spec

echo.
echo ========================================
echo   Build completed!
echo   Output: dist\kakao_openchat_gui.exe
echo ========================================
pause
