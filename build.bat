@echo off
REM Windows 빌드 스크립트
REM 사용법: build.bat

echo ========================================
echo 카카오 오픈채팅 인원 확인 도구 빌드
echo ========================================
echo.

REM 가상환경 활성화 (있는 경우)
if exist "venv\Scripts\activate.bat" (
    echo 가상환경 활성화 중...
    call venv\Scripts\activate.bat
)

REM 의존성 설치
echo 의존성 설치 중...
pip install -r requirements.txt

REM 빌드
echo.
echo 빌드 시작...
python build.py --clean

echo.
echo 완료! dist 폴더에서 kakao_openchat.exe를 확인하세요.
pause
