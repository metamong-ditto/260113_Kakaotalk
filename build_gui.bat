@echo off
chcp 65001 >nul
echo ========================================
echo   Building GUI version...
echo ========================================
echo.

pip install -r requirements.txt

echo.
pyinstaller --clean --onefile --windowed --name=kakao_openchat_gui ^
    --hidden-import=pyautogui ^
    --hidden-import=pyperclip ^
    --hidden-import=PIL ^
    --hidden-import=PIL.Image ^
    --hidden-import=pytesseract ^
    --hidden-import=pywinauto ^
    --hidden-import=pyscreeze ^
    gui.py

echo.
echo ========================================
echo   Build completed!
echo   Output: dist\kakao_openchat_gui.exe
echo ========================================
pause
