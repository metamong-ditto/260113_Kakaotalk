# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Kakao OpenChat Member Counter
"""

import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Selenium과 webdriver-manager의 숨겨진 import 수집
hidden_imports = [
    'selenium',
    'selenium.webdriver',
    'selenium.webdriver.chrome',
    'selenium.webdriver.chrome.service',
    'selenium.webdriver.chrome.options',
    'selenium.webdriver.common',
    'selenium.webdriver.common.by',
    'selenium.webdriver.support',
    'selenium.webdriver.support.ui',
    'selenium.webdriver.support.expected_conditions',
    'webdriver_manager',
    'webdriver_manager.chrome',
    'webdriver_manager.core',
    'webdriver_manager.core.download_manager',
    'webdriver_manager.core.driver_cache',
    'webdriver_manager.core.os_manager',
    'bs4',
    'urllib3',
    'certifi',
    'requests',
]

# 데이터 파일 수집
datas = []
datas += collect_data_files('selenium')
datas += collect_data_files('certifi')

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
    console=True,  # 콘솔 앱으로 빌드
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 아이콘 파일이 있으면 여기에 경로 지정
)
