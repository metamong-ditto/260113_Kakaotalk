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
    --hidden-import=pyautogui._pyautogui_win ^
    --hidden-import=pyperclip ^
    --hidden-import=PIL ^
    --hidden-import=PIL.Image ^
    --hidden-import=PIL._imaging ^
    --hidden-import=pytesseract ^
    --hidden-import=pywinauto ^
    --hidden-import=pywinauto.application ^
    --hidden-import=pywinauto.findwindows ^
    --hidden-import=pywinauto.controls ^
    --hidden-import=pyscreeze ^
    --hidden-import=mouseinfo ^
    --hidden-import=pynput ^
    --hidden-import=pynput.keyboard ^
    --hidden-import=pynput.mouse ^
    --collect-all=pyautogui ^
    --collect-all=pyscreeze ^
    --collect-all=pyperclip ^
    gui.py

echo.
echo ========================================
echo   Build completed!
echo   Output: dist\kakao_openchat_gui.exe
echo ========================================
pause
