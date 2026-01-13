@echo off
chcp 65001 >nul
echo ========================================
echo   Building GUI version...
echo ========================================
echo.

echo [Step 1/3] Installing dependencies...
pip install pyautogui pyscreeze mouseinfo pygetwindow pyrect pywinauto pyperclip pillow pytesseract pyinstaller

echo.
echo [Step 2/3] Verifying installation...
python -c "import pyautogui; print('pyautogui:', pyautogui.__version__)"
python -c "import pywinauto; print('pywinauto: OK')"
python -c "import PIL; print('PIL: OK')"

echo.
echo [Step 3/3] Building exe...
pyinstaller --clean --noconfirm kakao_openchat_gui.spec

echo.
echo ========================================
echo   Build completed!
echo   Output: dist\kakao_openchat_gui.exe
echo ========================================
pause
