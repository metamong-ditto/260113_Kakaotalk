#!/usr/bin/env python3
"""
PyInstaller 빌드 스크립트

사용법:
    python build.py          # 기본 빌드
    python build.py --clean  # 클린 빌드 (이전 빌드 삭제)
    python build.py --onedir # 단일 디렉토리 모드로 빌드
"""

import argparse
import os
import shutil
import subprocess
import sys


def clean_build():
    """이전 빌드 파일 삭제"""
    dirs_to_remove = ['build', 'dist', '__pycache__']
    files_to_remove = ['kakao_openchat.spec.bak']

    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            print(f"삭제 중: {dir_name}/")
            shutil.rmtree(dir_name)

    for file_name in files_to_remove:
        if os.path.exists(file_name):
            print(f"삭제 중: {file_name}")
            os.remove(file_name)

    # .pyc 파일 삭제
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                filepath = os.path.join(root, file)
                print(f"삭제 중: {filepath}")
                os.remove(filepath)


def build_exe(onedir: bool = False):
    """실행 파일 빌드"""
    print("\n" + "=" * 50)
    print("카카오 오픈채팅 인원 확인 도구 빌드")
    print("=" * 50 + "\n")

    # 의존성 확인
    try:
        import PyInstaller
        print(f"PyInstaller 버전: {PyInstaller.__version__}")
    except ImportError:
        print("오류: PyInstaller가 설치되지 않았습니다.")
        print("설치: pip install pyinstaller")
        sys.exit(1)

    # spec 파일 사용 또는 직접 빌드
    if os.path.exists('kakao_openchat.spec') and not onedir:
        # spec 파일로 빌드
        cmd = ['pyinstaller', '--clean', 'kakao_openchat.spec']
    else:
        # 직접 빌드
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

        # hidden imports 추가
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

        # 데이터 파일 추가
        cmd.extend(['--collect-data', 'selenium'])
        cmd.extend(['--collect-data', 'certifi'])

        cmd.append('main.py')

    print(f"빌드 명령: {' '.join(cmd)}\n")

    # 빌드 실행
    result = subprocess.run(cmd)

    if result.returncode == 0:
        print("\n" + "=" * 50)
        print("빌드 완료!")
        print("=" * 50)

        # 결과 파일 위치 안내
        if onedir:
            exe_path = os.path.join('dist', 'kakao_openchat')
        else:
            if sys.platform == 'win32':
                exe_path = os.path.join('dist', 'kakao_openchat.exe')
            else:
                exe_path = os.path.join('dist', 'kakao_openchat')

        print(f"\n실행 파일 위치: {exe_path}")
        print("\n사용법:")
        print(f"  {exe_path} \"검색어\"")
        print(f"  {exe_path}  # 대화형 모드")
    else:
        print("\n빌드 실패!")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="PyInstaller 빌드 스크립트")
    parser.add_argument(
        '--clean',
        action='store_true',
        help='이전 빌드 파일 삭제 후 빌드'
    )
    parser.add_argument(
        '--clean-only',
        action='store_true',
        help='빌드 없이 정리만 수행'
    )
    parser.add_argument(
        '--onedir',
        action='store_true',
        help='단일 디렉토리 모드로 빌드 (기본: 단일 파일)'
    )

    args = parser.parse_args()

    if args.clean or args.clean_only:
        clean_build()
        if args.clean_only:
            print("\n정리 완료!")
            return

    build_exe(onedir=args.onedir)


if __name__ == '__main__':
    main()
