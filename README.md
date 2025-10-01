# 🚀 암호화폐 분석 프로젝트

업비트 API를 활용한 Python 기반 암호화폐 데이터 분석 및 포트폴리오 관리 시스템

---

## 🎯 프로젝트 개요

이 프로젝트는 파이썬 기초 과정에서 배운 내용들을 종합하여 **실제 업비트 API**를 통해 암호화폐 데이터를 분석하는 실습 프로젝트입니다.

### ✨ 주요 기능
- 📊 **포트폴리오 분석기** - 보유 암호화폐 현황 및 비중 분석
- 🔔 **가격 알림 시스템** - 목표가 도달시 실시간 알림  
- 📈 **수익률 계산기** - 과거 투자 시나리오 수익률 분석

### 🎮 실행 방법
```bash
# 메인 프로그램 실행
python3 main.py

# 개별 모듈 실행
python3 src/portfolio_analyzer.py
python3 src/price_alert.py  
python3 src/return_calculator.py

# 테스트 실행
python3 tests/test_portfolio_analyzer.py
python3 tests/test_price_alert.py
python3 tests/test_return_calculator.py
```

---

## 🏗️ 프로젝트 구조

```
study-llm-project-week1/
├── 📚 docs/                    # 📖 완전한 설계 문서
│   ├── README.md               # 문서 메인 인덱스
│   ├── phase/                  # Phase별 구현 가이드
│   │   ├── phase1-project-setup.md
│   │   ├── phase2-portfolio-analyzer.md
│   │   ├── phase3-price-alert-system.md
│   │   └── phase4-return-calculator.md
│   ├── diagram/                # 시스템 다이어그램
│   │   ├── flowchart.md
│   │   ├── sequence-diagram.md
│   │   └── class-diagram.md
│   ├── codereview/             # 코드 리뷰
│   │   └── code-review-report.md
│   ├── test/                   # 테스트 가이드
│   │   └── testing-guide.md
│   └── prompt/                 # 프롬프트 템플릿
│       └── seedprompt.md
├── 🎯 src/                     # ✅ 비즈니스 로직 (완성)
│   ├── __init__.py
│   ├── portfolio_analyzer.py   # 📊 포트폴리오 분석기
│   ├── price_alert.py          # 🔔 가격 알림 시스템
│   └── return_calculator.py    # 📈 수익률 계산기
├── 🔧 utils/                   # ✅ 공통 유틸리티 (완성)
│   ├── __init__.py
│   ├── api_client.py           # 🌐 업비트 API 클라이언트
│   ├── date_utils.py           # 📅 날짜/시간 처리
│   └── format_utils.py         # 🎨 데이터 포맷팅
├── ⚙️ config/                  # ✅ 설정 관리 (완성)
│   ├── __init__.py
│   └── settings.py             # ⚙️ 프로젝트 설정
├── 🧪 tests/                   # ✅ 테스트 코드 (완성)
│   ├── __init__.py
│   ├── conftest.py
│   ├── helpers/                # 테스트 헬퍼
│   ├── test_api_client.py      # API 클라이언트 테스트
│   ├── test_portfolio_analyzer.py # 포트폴리오 분석기 테스트
│   ├── test_price_alert.py     # 가격 알림 시스템 테스트
│   ├── test_return_calculator.py # 수익률 계산기 테스트
│   └── requirements-test.txt   # 테스트 의존성
├── 📜 scripts/                 # ✅ 실행 스크립트 (완성)
│   ├── __init__.py
│   └── run_tests.py           # 테스트 실행 스크립트
├── 🚀 main.py                  # ✅ 메인 진입점 (완성)
├── 📋 requirements.txt         # ✅ 프로젝트 의존성
├── 🧪 pytest.ini              # ✅ 테스트 설정
└── 📖 README.md               # 프로젝트 메인 문서
```

---

## 🔄 시스템 플로우차트

```
┌─────────────────┐
│   사용자 시작    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│   main.py 실행   │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│   메뉴 선택     │
│ 1. 포트폴리오    │
│ 2. 가격알림      │
│ 3. 수익률계산    │
└─────────┬───────┘
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
┌─────────┐ ┌─────────┐
│포트폴리오│ │가격알림  │
│분석기   │ │시스템    │
└────┬────┘ └────┬────┘
     │           │
     ▼           ▼
┌─────────┐ ┌─────────┐
│API 호출 │ │실시간   │
│현재가   │ │모니터링 │
└────┬────┘ └────┬────┘
     │           │
     ▼           ▼
┌─────────┐ ┌─────────┐
│분석결과 │ │알림발생 │
│출력     │ │메시지   │
└─────────┘ └─────────┘
     │           │
     └─────┬─────┘
           │
           ▼
┌─────────────────┐
│   수익률계산기   │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  과거데이터조회  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  수익률계산및   │
│   결과출력      │
└─────────────────┘
```

## ⏰ 시퀀스 다이어그램

```
사용자    main.py    portfolio    api_client    upbit_api
  │         │           │            │            │
  │────────▶│           │            │            │
  │   실행   │           │            │            │
  │         │           │            │            │
  │◀────────│   메뉴    │            │            │
  │  선택요청│           │            │            │
  │         │           │            │            │
  │────────▶│ 1번선택   │            │            │
  │         │           │            │            │
  │         │──────────▶│            │            │
  │         │  포트폴리오│            │            │
  │         │   분석요청│            │            │
  │         │           │            │            │
  │         │           │──────────▶│            │
  │         │           │  현재가요청│            │
  │         │           │            │            │
  │         │           │            │──────────▶│
  │         │           │            │   API요청  │
  │         │           │            │            │
  │         │           │            │◀──────────│
  │         │           │            │  가격데이터│
  │         │           │◀──────────│            │
  │         │           │  가격응답  │            │
  │         │           │            │            │
  │         │           │  분석완료  │            │
  │         │◀──────────│            │            │
  │         │  결과반환 │            │            │
  │         │           │            │            │
  │◀────────│  결과출력 │            │            │
  │         │           │            │            │
```

---

## 📋 구현 가이드

## 🎮 동작 방식

### 📊 **1. 포트폴리오 분석기**
```
사용자 입력 → 포트폴리오 검증 → API 호출 → 가격 조회 → 분석 계산 → 결과 출력
```
- **기능**: 보유 암호화폐의 총 가치, 개별 비중, 수익률 계산
- **특징**: 실시간 가격 조회, 존재하지 않는 마켓 처리, 0 수량 허용

### 🔔 **2. 가격 알림 시스템**
```
설정 입력 → 목표가 계산 → 실시간 모니터링 → 알림 조건 확인 → 알림 발생
```
- **기능**: 실시간 가격 모니터링 및 목표가 도달시 알림
- **특징**: 상한가/하한가 설정, 프리셋 모드, 연속 알림 방지

### 📈 **3. 수익률 계산기**
```
투자조건 입력 → 과거 데이터 조회 → 현재가 조회 → 수익률 계산 → 결과 분석
```
- **기능**: 과거 특정 시점 투자시 현재 수익률 계산
- **특징**: 연간 수익률 계산, 다중 시나리오 비교, 상세한 분석 리포트

## 🛠️ 구현 현황

| Phase | 상태 | 주요 기능 | 테스트 |
|-------|------|-----------|--------|
| **Phase 1** | ✅ 완료 | 프로젝트 기반 구조 설정 | ✅ 통과 |
| **Phase 2** | ✅ 완료 | 포트폴리오 분석기 구현 | ✅ 통과 |
| **Phase 3** | ✅ 완료 | 가격 알림 시스템 구현 | ✅ 통과 |
| **Phase 4** | ✅ 완료 | 수익률 계산기 구현 | ✅ 통과 |

### 📚 **문서 가이드**
- **[📖 docs/README.md](./docs/README.md)** - 전체 문서 인덱스
- **[🔧 phase1-project-setup.md](docs/phase/phase1-project-setup.md)** - Phase 1 가이드
- **[📊 phase2-portfolio-analyzer.md](docs/phase/phase2-portfolio-analyzer.md)** - Phase 2 가이드
- **[🔔 phase3-price-alert-system.md](docs/phase/phase3-price-alert-system.md)** - Phase 3 가이드
- **[📈 phase4-return-calculator.md](docs/phase/phase4-return-calculator.md)** - Phase 4 가이드
- **[🔍 code-review-report.md](docs/codereview/code-review-report.md)** - 코드 리뷰

---

## 🚀 빠른 시작

### 📋 **사전 요구사항**
- Python 3.9 이상
- 인터넷 연결 (업비트 API 접근)
- 기본적인 Python 문법 지식

### ⚡ **즉시 시작하기**

1. **프로젝트 설정**
   ```bash
   # 가상환경 생성 (권장)
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   # venv\Scripts\activate   # Windows

   # 의존성 설치
   pip install -r requirements.txt
   ```

2. **메인 프로그램 실행**
   ```bash
   # 전체 프로그램 실행
   python3 main.py
   ```

3. **개별 기능 테스트**
   ```bash
   # 포트폴리오 분석기
   python3 tests/test_portfolio_analyzer.py
   
   # 가격 알림 시스템
   python3 tests/test_price_alert.py
   
   # 수익률 계산기
   python3 tests/test_return_calculator.py
   ```

---

## 🎓 학습 목표

이 프로젝트를 완료하면 다음을 습득할 수 있습니다:

### 🎯 **기술적 역량**
- ✅ 외부 API 연동 및 데이터 처리
- ✅ 모듈화된 Python 프로젝트 구조 설계
- ✅ 에러 처리 및 예외 상황 대응
- ✅ 타입 힌트 활용한 안전한 코딩
- ✅ 테스트 코드 작성 및 품질 관리

### 💼 **실무 경험**
- ✅ 실제 API를 활용한 데이터 분석
- ✅ 사용자 친화적 인터페이스 설계
- ✅ 성능 최적화 및 메모리 관리
- ✅ 배포 가능한 수준의 코드 품질

---

## 🎨 주요 특징

### 🏆 **학습자 친화적 설계**
- 📝 단계별 상세 가이드 제공
- ✅ 체크리스트 기반 진행 관리
- 🔍 코드 작성 이유와 배경 설명
- 🧪 각 단계별 테스트 방법 제시

### 🚀 **실무 수준 품질**
- 🏗️ 확장 가능한 모듈화 아키텍처
- 🔒 보안 및 에러 처리 고려
- 📊 성능 최적화 방안 제시
- 📚 완전한 문서화

### 🔄 **점진적 학습**
- 🎯 초급자: 기본 구조 이해
- 🎯 중급자: 전체 기능 구현
- 🎯 고급자: 성능 최적화 및 확장

---

## 🛡️ 주의사항

### ⚠️ **사용 제한**
- 이 프로젝트는 **교육 목적**으로 제작되었습니다
- 실제 투자 결정시 참고용으로만 활용하세요
- 업비트 API 이용약관을 반드시 준수하세요

### 📞 **지원 및 문의**
- 구현 과정에서 문제 발생시 `docs/code-review-report.md` 참고
- 각 Phase 문서의 "완료 후 확인사항" 체크리스트 활용

---

## 🎉 시작하기

모든 준비가 완료되었습니다!

**👉 [docs/README.md](./docs/README.md)에서 상세한 구현 가이드를 확인하고 시작하세요!**

---

**Happy Coding! 🚀📈**# study-llm-project-week1
