# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Kakao OpenChat GUI (onefile mode)
"""

from PyInstaller.utils.hooks import collect_all, collect_submodules, collect_data_files

block_cipher = None

# Collect all from packages
datas = []
binaries = []
hiddenimports = []

packages = ['pyautogui', 'pyscreeze', 'pyperclip', 'PIL', 'pywinauto', 'pygetwindow', 'pyrect', 'mouseinfo']

for pkg in packages:
    try:
        pkg_datas, pkg_binaries, pkg_hiddenimports = collect_all(pkg)
        datas += pkg_datas
        binaries += pkg_binaries
        hiddenimports += pkg_hiddenimports
    except:
        pass

# Additional hidden imports
hiddenimports += [
    'pyautogui',
    'pyautogui._pyautogui_win',
    'pyscreeze',
    'pyperclip',
    'PIL',
    'PIL.Image',
    'pytesseract',
    'pywinauto',
    'pywinauto.application',
    'tkinter',
    'tkinter.ttk',
]

a = Analysis(
    ['gui.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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

# onefile mode
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
