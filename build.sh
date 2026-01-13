#!/bin/bash
# Linux/Mac 빌드 스크립트
# 사용법: ./build.sh

echo "========================================"
echo "카카오 오픈채팅 인원 확인 도구 빌드"
echo "========================================"
echo

# 가상환경 활성화 (있는 경우)
if [ -f "venv/bin/activate" ]; then
    echo "가상환경 활성화 중..."
    source venv/bin/activate
fi

# 의존성 설치
echo "의존성 설치 중..."
pip install -r requirements.txt

# 빌드
echo
echo "빌드 시작..."
python build.py --clean

echo
echo "완료! dist 폴더에서 kakao_openchat을 확인하세요."
