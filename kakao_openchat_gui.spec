# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Kakao OpenChat GUI
"""

from PyInstaller.utils.hooks import collect_all, collect_submodules

block_cipher = None

# Collect all data and binaries from packages
pyautogui_datas, pyautogui_binaries, pyautogui_hiddenimports = collect_all('pyautogui')
pyscreeze_datas, pyscreeze_binaries, pyscreeze_hiddenimports = collect_all('pyscreeze')
pyperclip_datas, pyperclip_binaries, pyperclip_hiddenimports = collect_all('pyperclip')
pillow_datas, pillow_binaries, pillow_hiddenimports = collect_all('PIL')
pywinauto_datas, pywinauto_binaries, pywinauto_hiddenimports = collect_all('pywinauto')

# Combine all
datas = pyautogui_datas + pyscreeze_datas + pyperclip_datas + pillow_datas + pywinauto_datas
binaries = pyautogui_binaries + pyscreeze_binaries + pyperclip_binaries + pillow_binaries + pywinauto_binaries

hidden_imports = [
    'pyautogui',
    'pyautogui._pyautogui_win',
    'pyscreeze',
    'pyperclip',
    'PIL',
    'PIL.Image',
    'PIL._imaging',
    'pytesseract',
    'pywinauto',
    'pywinauto.application',
    'pywinauto.findwindows',
    'pywinauto.controls',
    'pywinauto.controls.hwndwrapper',
    'mouseinfo',
    'tkinter',
    'tkinter.ttk',
    'tkinter.messagebox',
    'tkinter.filedialog',
]
hidden_imports += pyautogui_hiddenimports
hidden_imports += pyscreeze_hiddenimports
hidden_imports += pyperclip_hiddenimports
hidden_imports += pillow_hiddenimports
hidden_imports += pywinauto_hiddenimports

a = Analysis(
    ['gui.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='kakao_openchat_gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
