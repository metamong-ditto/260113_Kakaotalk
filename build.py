#!/usr/bin/env python3
"""
PyInstaller Build Script

Usage:
    python build.py          # Default build
    python build.py --clean  # Clean build (remove previous build)
    python build.py --onedir # Build in one-directory mode
"""

import argparse
import os
import shutil
import subprocess
import sys


def clean_build():
    """Remove previous build files"""
    dirs_to_remove = ['build', 'dist', '__pycache__']
    files_to_remove = ['kakao_openchat.spec.bak']

    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            print(f"Removing: {dir_name}/")
            shutil.rmtree(dir_name)

    for file_name in files_to_remove:
        if os.path.exists(file_name):
            print(f"Removing: {file_name}")
            os.remove(file_name)

    # Remove .pyc files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                filepath = os.path.join(root, file)
                print(f"Removing: {filepath}")
                os.remove(filepath)


def build_exe(onedir: bool = False):
    """Build executable"""
    print("\n" + "=" * 50)
    print("Kakao OpenChat Member Counter - Build")
    print("=" * 50 + "\n")

    # Check dependencies
    try:
        import PyInstaller
        print(f"PyInstaller version: {PyInstaller.__version__}")
    except ImportError:
        print("Error: PyInstaller is not installed.")
        print("Install: pip install pyinstaller")
        sys.exit(1)

    # Use spec file or build directly
    if os.path.exists('kakao_openchat.spec') and not onedir:
        # Build with spec file
        cmd = ['pyinstaller', '--clean', 'kakao_openchat.spec']
    else:
        # Build directly
        cmd = [
            'pyinstaller',
            '--clean',
            '--name=kakao_openchat',
            '--console',
            '--noconfirm',
        ]

        if onedir:
            cmd.append('--onedir')
        else:
            cmd.append('--onefile')

        # Add hidden imports
        hidden_imports = [
            'selenium',
            'selenium.webdriver',
            'selenium.webdriver.chrome.service',
            'selenium.webdriver.chrome.options',
            'webdriver_manager',
            'webdriver_manager.chrome',
            'bs4',
        ]
        for imp in hidden_imports:
            cmd.extend(['--hidden-import', imp])

        # Add data files
        cmd.extend(['--collect-data', 'selenium'])
        cmd.extend(['--collect-data', 'certifi'])

        cmd.append('main.py')

    print(f"Build command: {' '.join(cmd)}\n")

    # Run build
    result = subprocess.run(cmd)

    if result.returncode == 0:
        print("\n" + "=" * 50)
        print("Build completed!")
        print("=" * 50)

        # Show output file location
        if onedir:
            exe_path = os.path.join('dist', 'kakao_openchat')
        else:
            if sys.platform == 'win32':
                exe_path = os.path.join('dist', 'kakao_openchat.exe')
            else:
                exe_path = os.path.join('dist', 'kakao_openchat')

        print(f"\nExecutable location: {exe_path}")
        print("\nUsage:")
        print(f'  {exe_path} "keyword"')
        print(f"  {exe_path}  # Interactive mode")
    else:
        print("\nBuild failed!")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="PyInstaller Build Script")
    parser.add_argument(
        '--clean',
        action='store_true',
        help='Remove previous build files before building'
    )
    parser.add_argument(
        '--clean-only',
        action='store_true',
        help='Only clean without building'
    )
    parser.add_argument(
        '--onedir',
        action='store_true',
        help='Build in one-directory mode (default: one-file)'
    )

    args = parser.parse_args()

    if args.clean or args.clean_only:
        clean_build()
        if args.clean_only:
            print("\nClean completed!")
            return

    build_exe(onedir=args.onedir)


if __name__ == '__main__':
    main()
