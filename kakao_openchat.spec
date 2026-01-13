# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Kakao OpenChat Member Counter (PC Automation)
"""

import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Hidden imports for pyautogui, pywinauto, etc.
hidden_imports = [
    'pyautogui',
    'pyperclip',
    'PIL',
    'PIL.Image',
    'pytesseract',
    'pywinauto',
    'pywinauto.application',
    'pywinauto.findwindows',
    'pyscreeze',
    'mouseinfo',
]

# Collect data files
datas = []
datas += collect_data_files('pyautogui')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
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
    name='kakao_openchat',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
