# 카카오톡 오픈채팅방 인원 수 확인 도구

카카오톡 PC 버전에서 오픈채팅방을 검색하고, 채팅방 이름과 인원 수를 확인하는 프로그램입니다.

## 기능

- 카카오톡 PC에서 오픈채팅방 검색
- 채팅방별 인원 수 확인 (OCR)
- 인원 수 기준 정렬
- 통계 정보 제공 (총 인원, 평균, 최대/최소)
- CSV 파일로 결과 저장
- **GUI 버전** 및 **CLI 버전** 제공

## 스크린샷

```
┌─────────────────────────────────────────────────────┐
│  카카오톡 오픈채팅 인원 확인                          │
├─────────────────────────────────────────────────────┤
│  검색어: [파이썬        ]  [검색]  [CSV 저장]        │
├─────────────────────────────────────────────────────┤
│  순위 │ 채팅방 이름              │ 인원 수          │
│  ─────┼──────────────────────────┼─────────────────│
│   1   │ 파이썬 코딩 스터디        │ 2,345명         │
│   2   │ 파이썬 개발자 모임        │ 1,890명         │
│   3   │ 파이썬 입문자 환영        │ 1,234명         │
├─────────────────────────────────────────────────────┤
│  검색 완료: 10개 채팅방  │  총: 8,500명 평균: 850명 │
└─────────────────────────────────────────────────────┘
```

## 필수 조건

1. **Windows OS** (카카오톡 PC 버전 필요)
2. **카카오톡 PC** 설치 및 로그인
3. **Tesseract OCR** 설치

### Tesseract OCR 설치

OCR(문자 인식)을 위해 Tesseract가 필요합니다.

1. [Tesseract 다운로드](https://github.com/UB-Mannheim/tesseract/wiki)에서 설치
2. 설치 시 "Additional language data" 에서 **Korean** 선택
3. 설치 후 시스템 PATH에 추가 (기본: `C:\Program Files\Tesseract-OCR`)

## 실행 파일 빌드 (.exe)

### 빠른 빌드 (GUI 버전만)

```batch
build_gui.bat
```

### 선택적 빌드

```batch
build.bat
```

실행하면 메뉴가 표시됩니다:
```
[1] Build GUI version (kakao_openchat_gui.exe)
[2] Build CLI version (kakao_openchat.exe)
[3] Build both versions
[4] Exit
```

### 빌드 결과

| 파일 | 설명 |
|------|------|
| `dist/kakao_openchat_gui.exe` | GUI 버전 (창 프로그램) |
| `dist/kakao_openchat.exe` | CLI 버전 (명령줄) |

## 사용법

### GUI 버전

1. `kakao_openchat_gui.exe` 실행 (또는 `python gui.py`)
2. 검색어 입력
3. "검색" 버튼 클릭
4. 결과 확인 후 필요시 "CSV 저장"

### CLI 버전

```bash
# 대화형 모드
kakao_openchat.exe

# 직접 검색
kakao_openchat.exe "파이썬"

# CSV로 저장
kakao_openchat.exe "영어" -o result.csv
```

## Python으로 직접 실행

### 설치

```bash
pip install -r requirements.txt
```

### 실행

```bash
# GUI 버전
python gui.py

# CLI 버전
python main.py
python main.py "파이썬"
```

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

### GUI가 멈춘 것처럼 보임
- 검색 중에는 카카오톡이 자동 조작됩니다
- 잠시 기다려주세요

## 주의 사항

- 이 도구는 교육 및 개인적인 용도로만 사용해주세요
- 카카오 서비스 이용 약관을 준수해주세요
- 프로그램 실행 중 마우스/키보드가 자동 조작됩니다
- 실행 중에는 다른 작업을 하지 마세요

## 파일 구조

```
├── gui.py                    # GUI 메인
├── main.py                   # CLI 메인
├── kakao_openchat_scraper.py # 핵심 로직
├── build.bat                 # 빌드 메뉴
├── build_gui.bat             # GUI 빌드 (빠른 실행)
├── requirements.txt          # 의존성
└── dist/
    ├── kakao_openchat_gui.exe
    └── kakao_openchat.exe
```

## 라이선스

MIT License
