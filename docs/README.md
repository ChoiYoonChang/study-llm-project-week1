# 📚 암호화폐 분석 프로젝트 문서

업비트 API를 활용한 암호화폐 데이터 분석 및 포트폴리오 관리 시스템의 완전한 설계 문서입니다.

---

## 📋 문서 목차

### 🚀 프로젝트 기본 정보
| 문서 | 설명 | 상태 |
|------|------|------|
| [📖 seedprompt.md](prompt/seedprompt.md) | 원본 프로젝트 요구사항 | ✅ 완료 |
| [🔍 code-review-report.md](codereview/code-review-report.md) | 시니어 개발자 코드 리뷰 보고서 | ✅ 완료 |

### 🏗️ 구현 가이드 (Phase별)
| Phase | 문서 | 주요 내용 | 예상 시간 |
|-------|------|-----------|----------|
| **Phase 1** | [🔧 phase1-project-setup.md](phase/phase1-project-setup.md) | 프로젝트 초기 설정 및 기반 구조 | 4-6시간 |
| **Phase 2** | [📊 phase2-portfolio-analyzer.md](phase/phase2-portfolio-analyzer.md) | 포트폴리오 분석기 (필수과제) | 6-8시간 |
| **Phase 3** | [🔔 phase3-price-alert-system.md](phase/phase3-price-alert-system.md) | 가격 알림 시스템 (필수과제) | 8-10시간 |
| **Phase 4** | [📈 phase4-return-calculator.md](phase/phase4-return-calculator.md) | 수익률 계산기 (도전과제) | 10-12시간 |

### 📐 시스템 설계 다이어그램
| 다이어그램 | 문서 | 내용 |
|------------|------|------|
| **Flow Chart** | [🔄 flowchart.md](diagram/flowchart.md) | 전체 시스템 및 Phase별 흐름도 |
| **Sequence Diagram** | [⏰ sequence-diagram.md](diagram/sequence-diagram.md) | 객체 간 상호작용 시퀀스 |
| **Class Diagram** | [🏗️ class-diagram.md](diagram/class-diagram.md) | 클래스 구조 및 관계도 |

---

## 🎯 프로젝트 개요

### 🔍 **프로젝트 목적**
- 파이썬 기초 과정 종합 실습
- 업비트 API를 활용한 실시간 암호화폐 데이터 분석
- 포트폴리오 관리 및 투자 수익률 계산
- 가격 알림 시스템을 통한 모니터링

### 🏆 **학습 목표**
- ✅ 외부 API 연동 및 데이터 처리
- ✅ 객체지향 프로그래밍 실습
- ✅ 모듈화 및 패키지 구조 설계
- ✅ 에러 처리 및 예외 상황 대응
- ✅ 데이터 시각화 및 결과 출력

### 🛠️ **기술 스택**
- **언어**: Python 3.9+
- **주요 라이브러리**: requests, datetime, typing
- **API**: 업비트 (Upbit) REST API
- **아키텍처**: 모듈화된 MVC 패턴

---

## 📊 프로젝트 구조

```
week1-python-project/
├── docs/                          # 📚 프로젝트 문서
│   ├── README.md                   # 문서 메인 인덱스
│   ├── seedprompt.md              # 원본 요구사항
│   ├── phase1-project-setup.md    # Phase 1 가이드
│   ├── phase2-portfolio-analyzer.md # Phase 2 가이드
│   ├── phase3-price-alert-system.md # Phase 3 가이드
│   ├── phase4-return-calculator.md # Phase 4 가이드
│   ├── flowchart.md               # 플로우 차트
│   ├── sequence-diagram.md        # 시퀀스 다이어그램
│   ├── class-diagram.md           # 클래스 다이어그램
│   └── code-review-report.md      # 코드 리뷰 보고서
├── src/                           # 🎯 비즈니스 로직
│   ├── portfolio_analyzer.py      # 포트폴리오 분석기
│   ├── price_alert.py            # 가격 알림 시스템
│   └── return_calculator.py       # 수익률 계산기
├── utils/                         # 🔧 공통 유틸리티
│   ├── api_client.py             # API 클라이언트
│   ├── date_utils.py             # 날짜/시간 처리
│   └── format_utils.py           # 데이터 포맷팅
├── config/                        # ⚙️ 설정 관리
│   └── settings.py               # 전역 설정
├── tests/                         # 🧪 테스트
│   └── test_*.py                 # 각 모듈별 테스트
└── main.py                       # 🚀 메인 진입점
```

---

## 🚀 빠른 시작 가이드

### 1️⃣ **환경 설정**
```bash
# 1. 프로젝트 클론 또는 다운로드
cd week1-python-project

# 2. 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# 3. 의존성 설치
pip install -r requirements.txt
```

### 2️⃣ **Phase별 구현**
1. **[Phase 1](phase/phase1-project-setup.md)** - 프로젝트 기반 구조 설정
2. **[Phase 2](phase/phase2-portfolio-analyzer.md)** - 포트폴리오 분석기 구현
3. **[Phase 3](phase/phase3-price-alert-system.md)** - 가격 알림 시스템 구현
4. **[Phase 4](phase/phase4-return-calculator.md)** - 수익률 계산기 구현

### 3️⃣ **실행**
```bash
# 메인 프로그램 실행
python main.py

# 개별 테스트 실행
python tests/test_api_client.py
```

---

## 🎨 주요 기능

### 📊 **포트폴리오 분석기** (Phase 2)
- 보유 암호화폐와 수량을 딕셔너리로 정의
- 각 암호화폐의 현재 가치 계산
- 전체 포트폴리오 가치 및 비중 계산
- 테이블 형태의 상세 분석 결과 출력

### 🔔 **가격 알림 시스템** (Phase 3)
- 목표가 설정 (상한가, 하한가)
- 실시간 현재가 모니터링
- 목표가 도달 시 알림 메시지 출력
- 모니터링 히스토리 기록

### 📈 **수익률 계산기** (Phase 4)
- 과거 특정 시점 투자 시나리오 분석
- 투자 시점과 현재 가격 비교
- 수익률 및 수익금 계산
- 연간 수익률 환산 (복리 기준)

---

## 🔧 고급 기능 (확장 가능)

### 🚀 **성능 최적화**
- Rate Limiting으로 API 제한 준수
- 캐싱 시스템으로 응답 속도 개선
- 비동기 처리로 사용자 경험 향상

### 🔒 **보안 강화**
- 환경변수 기반 설정 관리
- API 키 보안 저장
- 입력 데이터 검증 강화

### 📊 **모니터링**
- 구조화된 로깅 시스템
- 메모리 사용량 모니터링
- 에러 추적 및 알림

---

## 📈 학습 로드맵

### 🎯 **초급자** (Python 기초 학습자)
1. **Phase 1** - 기본 구조 이해
2. **Phase 2** - API 호출 및 데이터 처리
3. 기본 기능 테스트 및 실행

### 🎯 **중급자** (Python 경험자)
1. **Phase 1-4** 전체 구현
2. 에러 처리 및 예외 상황 대응
3. 코드 리뷰 보고서 참고하여 개선

### 🎯 **고급자** (실무 적용 희망자)
1. 전체 Phase 구현
2. [코드 리뷰 보고서](codereview/code-review-report.md) 보완사항 적용
3. 추가 기능 확장 (웹 인터페이스, DB 연동 등)

---

## 📞 지원 및 문의

### 🐛 **문제 해결**
1. **[코드 리뷰 보고서](codereview/code-review-report.md)** - 알려진 이슈와 해결방안
2. **각 Phase 문서의 "완료 후 확인사항"** - 체크리스트 활용
3. **테스트 파일** - 기능별 동작 확인

### 📚 **추가 학습 자료**
- 업비트 API 공식 문서: https://docs.upbit.com/
- Python requests 라이브러리: https://requests.readthedocs.io/
- Python typing 모듈: https://docs.python.org/3/library/typing.html

---

## 📜 라이센스 및 주의사항

### ⚠️ **주의사항**
- 이 프로젝트는 **교육 목적**으로 제작되었습니다
- 실제 투자 결정시 참고용으로만 활용하세요
- 업비트 API 이용약관 및 제한사항을 준수하세요
- API 호출 빈도 제한을 반드시 지켜주세요

### 📄 **면책조항**
- 이 도구로 인한 투자 손실에 대해 책임지지 않습니다
- 실제 거래시에는 수수료, 세금 등을 별도 고려해야 합니다
- 과거 수익률이 미래 수익률을 보장하지 않습니다

---

## 🎉 마무리

이 프로젝트를 통해 Python 기초부터 실무 적용까지 단계적으로 학습할 수 있습니다.
각 Phase를 차근차근 따라하시면서 암호화폐 데이터 분석의 전체 과정을 경험해보세요!

**Good Luck with Your Crypto Analysis Journey! 🚀📈**