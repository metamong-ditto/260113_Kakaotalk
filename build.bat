@echo off
chcp 65001 >nul
REM ========================================
REM Kakao OpenChat Member Counter - Build
REM ========================================

echo.
echo ========================================
echo   Kakao OpenChat - Build Tool
echo ========================================
echo.
echo [1] Build GUI version (kakao_openchat_gui.exe)
echo [2] Build CLI version (kakao_openchat.exe)
echo [3] Build both versions
echo [4] Exit
echo.

set /p choice="Select option (1-4): "

if "%choice%"=="1" goto build_gui
if "%choice%"=="2" goto build_cli
if "%choice%"=="3" goto build_both
if "%choice%"=="4" goto end
goto end

:install_deps
echo.
echo Installing dependencies...
pip install -r requirements.txt
goto :eof

:build_gui
call :install_deps
echo.
echo Building GUI version...
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
echo Done! Check: dist\kakao_openchat_gui.exe
goto end

:build_cli
call :install_deps
echo.
echo Building CLI version...
pyinstaller --clean --onefile --console --name=kakao_openchat ^
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
    main.py
echo.
echo Done! Check: dist\kakao_openchat.exe
goto end

:build_both
call :install_deps
echo.
echo Building GUI version...
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
echo Building CLI version...
pyinstaller --clean --onefile --console --name=kakao_openchat ^
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
    main.py

echo.
echo ========================================
echo Build completed!
echo ========================================
echo.
echo GUI version: dist\kakao_openchat_gui.exe
echo CLI version: dist\kakao_openchat.exe
goto end

:end
echo.
pause
