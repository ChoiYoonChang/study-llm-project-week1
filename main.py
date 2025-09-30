"""
암호화폐 분석 프로젝트 메인 실행 파일
사용자 인터페이스 및 메뉴 시스템 제공
"""

def print_welcome_message():
    """프로젝트 시작 환영 메시지"""
    print("=" * 60)
    print("🚀 암호화폐 분석 프로젝트에 오신 것을 환영합니다!")
    print("=" * 60)
    print("이 프로젝트는 업비트 API를 활용한 암호화폐 분석 도구입니다.")
    print()


def show_menu():
    """메인 메뉴 출력"""
    print("\n📋 메뉴를 선택하세요:")
    print("1. 포트폴리오 분석기 (Phase 2)")
    print("2. 가격 알림 시스템 (Phase 3)")
    print("3. 수익률 계산기 (Phase 4)")
    print("4. 종료")
    print("-" * 40)


def main():
    """메인 실행 함수"""
    print_welcome_message()

    while True:
        show_menu()
        try:
            choice = input("선택 (1-4): ").strip()

            if choice == '1':
                print("\n📊 포트폴리오 분석기")
                print("🚧 Phase 2에서 구현 예정입니다.")
                # TODO: Phase 2 구현 후 import 및 함수 호출 추가
                # from src.portfolio_analyzer import run_portfolio_analyzer
                # run_portfolio_analyzer()

            elif choice == '2':
                print("\n🔔 가격 알림 시스템")
                print("🚧 Phase 3에서 구현 예정입니다.")
                # TODO: Phase 3 구현 후 import 및 함수 호출 추가
                # from src.price_alert import run_price_alert
                # run_price_alert()

            elif choice == '3':
                print("\n📈 수익률 계산기")
                print("🚧 Phase 4에서 구현 예정입니다.")
                # TODO: Phase 4 구현 후 import 및 함수 호출 추가
                # from src.return_calculator import run_return_calculator
                # run_return_calculator()

            elif choice == '4':
                print("\n👋 프로그램을 종료합니다. 감사합니다!")
                break

            else:
                print("❌ 잘못된 선택입니다. 1-4 사이의 숫자를 입력하세요.")

        except KeyboardInterrupt:
            print("\n\n👋 프로그램을 종료합니다.")
            break
        except Exception as e:
            print(f"❌ 오류가 발생했습니다: {e}")


if __name__ == "__main__":
    main()