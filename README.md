# 카카오톡 오픈채팅방 인원 수 확인 도구

카카오톡 PC 버전에서 오픈채팅방을 검색하고, 채팅방 이름과 인원 수를 확인하는 프로그램입니다.
PyAutoGUI를 사용한 GUI 자동화 방식으로 동작합니다.

## 기능

- 카카오톡 PC에서 오픈채팅방 검색
- 채팅방별 인원 수 확인 (OCR)
- 인원 수 기준 정렬
- 통계 정보 제공 (총 인원, 평균, 최대/최소)
- CSV 파일로 결과 저장
- 대화형 모드 지원

## 필수 조건

1. **Windows OS** (카카오톡 PC 버전 필요)
2. **카카오톡 PC** 설치 및 로그인
3. **Python 3.10 이상**
4. **Tesseract OCR** 설치

### Tesseract OCR 설치

OCR(문자 인식)을 위해 Tesseract가 필요합니다.

1. [Tesseract 다운로드](https://github.com/UB-Mannheim/tesseract/wiki)에서 설치
2. 설치 시 "Additional language data" 에서 **Korean** 선택
3. 설치 후 시스템 PATH에 추가 (기본: `C:\Program Files\Tesseract-OCR`)

## 설치

```bash
pip install -r requirements.txt
```

## 사용법

### 사전 준비

1. 카카오톡 PC를 실행하고 로그인합니다
2. 오픈채팅 탭이 보이는 상태로 둡니다

### 대화형 모드

```bash
python main.py
```

### 직접 검색

```bash
# 기본 검색
python main.py "파이썬"

# CSV로 저장
python main.py "영어" -o result.csv
```

### 옵션

| 옵션 | 설명 |
|------|------|
| `keyword` | 검색할 키워드 (없으면 대화형 모드) |
| `-o`, `--output` | 결과를 저장할 CSV 파일명 |

## 출력 예시

```
============================================================
'파이썬' 검색 결과: 총 10개 채팅방
============================================================

1. 파이썬 코딩 스터디
   인원: 2,345명

2. 파이썬 개발자 모임
   인원: 1,890명

...

============================================================
통계:
  - 총 채팅방 수: 10개
  - 총 인원 수: 8,500명
  - 평균 인원 수: 850.0명
  - 최대 인원: 2,345명
  - 최소 인원: 120명
============================================================
```

## 모듈로 사용

```python
from kakao_openchat_scraper import search_openchat, print_results

# 검색 실행
rooms = search_openchat("파이썬")

# 결과 출력
print_results(rooms, "파이썬")

# 개별 채팅방 정보 접근
for room in rooms:
    print(f"{room.name}: {room.member_count}명")
```

## 실행 파일 빌드 (PyInstaller)

```bash
# 의존성 설치
pip install -r requirements.txt

# 빌드 실행
python build.py --clean
```

빌드 완료 후 `dist/kakao_openchat.exe` 생성

## 동작 방식

1. 카카오톡 PC 창을 찾아 활성화
2. 오픈채팅 탭으로 이동
3. 검색창에 키워드 입력
4. 검색 결과 화면 캡처
5. OCR로 텍스트 추출
6. 채팅방 이름과 인원 수 파싱

## 문제 해결

### "카카오톡이 실행되어 있지 않습니다"
- 카카오톡 PC를 실행하고 로그인하세요

### "Tesseract가 설치되어 있는지 확인하세요"
- Tesseract OCR을 설치하고 PATH에 추가하세요

### 인원 수가 정확하지 않음
- OCR 인식률에 따라 오차가 있을 수 있습니다
- 카카오톡 창 크기를 키우면 인식률이 향상됩니다

## 주의 사항

- 이 도구는 교육 및 개인적인 용도로만 사용해주세요
- 카카오 서비스 이용 약관을 준수해주세요
- 프로그램 실행 중 마우스/키보드가 자동 조작됩니다
- 실행 중에는 다른 작업을 하지 마세요

## 라이선스

MIT License
