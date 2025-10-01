#!/usr/bin/env python3
"""
테스트 실행 자동화 스크립트
다양한 테스트 시나리오를 자동으로 실행하고 결과를 정리

사용법:
    python scripts/run_tests.py --all              # 모든 테스트 실행
    python scripts/run_tests.py --unit             # 단위 테스트만
    python scripts/run_tests.py --integration      # 통합 테스트만
    python scripts/run_tests.py --e2e              # E2E 테스트만
    python scripts/run_tests.py --coverage         # 커버리지 포함
    python scripts/run_tests.py --performance      # 성능 테스트 포함
"""

import os
import sys
import subprocess
import argparse
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

class TestRunner:
    """테스트 실행 관리 클래스"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.test_results: Dict[str, Any] = {}
        self.start_time = datetime.now()

    def run_command(self, cmd: List[str], description: str) -> Dict[str, Any]:
        """
        명령어 실행 및 결과 수집

        Args:
            cmd: 실행할 명령어 리스트
            description: 명령어 설명
        """
        print(f"\n🔄 {description}")
        print(f"   Command: {' '.join(cmd)}")

        start_time = time.time()

        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300  # 5분 타임아웃
            )

            end_time = time.time()
            duration = end_time - start_time

            return {
                "description": description,
                "command": " ".join(cmd),
                "returncode": result.returncode,
                "duration": duration,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0
            }

        except subprocess.TimeoutExpired:
            return {
                "description": description,
                "command": " ".join(cmd),
                "returncode": -1,
                "duration": 300,
                "stdout": "",
                "stderr": "Test timed out after 5 minutes",
                "success": False
            }
        except Exception as e:
            return {
                "description": description,
                "command": " ".join(cmd),
                "returncode": -1,
                "duration": 0,
                "stdout": "",
                "stderr": str(e),
                "success": False
            }

    def run_unit_tests(self, coverage: bool = False) -> Dict[str, Any]:
        """단위 테스트 실행"""
        cmd = ["python", "-m", "pytest", "tests/unit/", "-v", "--tb=short"]

        if coverage:
            cmd.extend([
                "--cov=src",
                "--cov=utils",
                "--cov=config",
                "--cov-report=html:tests/coverage_html_unit",
                "--cov-report=term-missing"
            ])

        cmd.extend(["-m", "unit"])  # 단위 테스트 마커

        return self.run_command(cmd, "단위 테스트 실행")

    def run_integration_tests(self, coverage: bool = False) -> Dict[str, Any]:
        """통합 테스트 실행"""
        cmd = ["python", "-m", "pytest", "tests/integration/", "-v", "--tb=short"]

        if coverage:
            cmd.extend([
                "--cov=src",
                "--cov=utils",
                "--cov=config",
                "--cov-report=html:tests/coverage_html_integration",
                "--cov-report=term-missing"
            ])

        cmd.extend(["-m", "integration"])  # 통합 테스트 마커

        return self.run_command(cmd, "통합 테스트 실행")

    def run_e2e_tests(self) -> Dict[str, Any]:
        """E2E 테스트 실행"""
        cmd = [
            "python", "-m", "pytest",
            "tests/e2e/", "-v", "--tb=short",
            "-m", "e2e",
            "--durations=0"  # 모든 테스트 실행 시간 표시
        ]

        return self.run_command(cmd, "E2E 테스트 실행")

    def run_performance_tests(self) -> Dict[str, Any]:
        """성능 테스트 실행"""
        cmd = [
            "python", "-m", "pytest",
            "tests/", "-v", "--tb=short",
            "-m", "slow",  # 성능 테스트 마커
            "--benchmark-only",  # 벤치마크만 실행
            "--benchmark-json=tests/benchmark_results.json"
        ]

        return self.run_command(cmd, "성능 테스트 실행")

    def run_all_tests(self, coverage: bool = False, performance: bool = False) -> List[Dict[str, Any]]:
        """모든 테스트 실행"""
        results = []

        print("🚀 전체 테스트 스위트 실행 시작")

        # 1. 단위 테스트
        results.append(self.run_unit_tests(coverage=coverage))

        # 2. 통합 테스트
        results.append(self.run_integration_tests(coverage=coverage))

        # 3. E2E 테스트
        results.append(self.run_e2e_tests())

        # 4. 성능 테스트 (옵션)
        if performance:
            results.append(self.run_performance_tests())

        return results

    def generate_report(self, results: List[Dict[str, Any]]) -> str:
        """테스트 결과 리포트 생성"""
        total_duration = (datetime.now() - self.start_time).total_seconds()
        successful_tests = sum(1 for r in results if r["success"])
        total_tests = len(results)

        report = f"""
🧪 암호화폐 분석 프로젝트 테스트 결과 리포트
{'='*60}

📊 전체 결과 요약:
- 총 테스트 스위트: {total_tests}개
- 성공: {successful_tests}개
- 실패: {total_tests - successful_tests}개
- 전체 실행 시간: {total_duration:.2f}초

📋 상세 결과:
"""

        for i, result in enumerate(results, 1):
            status = "✅ 성공" if result["success"] else "❌ 실패"
            report += f"""
{i}. {result['description']}
   상태: {status}
   실행 시간: {result['duration']:.2f}초
   명령어: {result['command']}
"""

            if not result["success"]:
                report += f"   오류: {result['stderr'][:200]}...\n"

        # 권장사항
        report += f"""
{'='*60}

📝 권장사항:
"""
        if successful_tests == total_tests:
            report += "- 🎉 모든 테스트가 성공했습니다!"
        else:
            report += "- ⚠️ 실패한 테스트를 확인하고 수정해주세요."
            report += "- 🔍 상세 로그는 각 테스트 출력에서 확인 가능합니다."

        report += """
- 📊 커버리지 리포트: tests/coverage_html/index.html
- 🏃‍♂️ 성능 벤치마크: tests/benchmark_results.json
- 📁 테스트 로그: pytest.log

생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

        return report

    def save_report(self, report: str):
        """리포트를 파일로 저장"""
        report_dir = self.project_root / "tests" / "reports"
        report_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = report_dir / f"test_report_{timestamp}.txt"

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"📋 테스트 리포트 저장: {report_file}")

def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(
        description="암호화폐 분석 프로젝트 테스트 실행기",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  python scripts/run_tests.py --all --coverage     # 모든 테스트 + 커버리지
  python scripts/run_tests.py --unit               # 단위 테스트만
  python scripts/run_tests.py --integration        # 통합 테스트만
  python scripts/run_tests.py --e2e                # E2E 테스트만
  python scripts/run_tests.py --performance        # 성능 테스트만
        """
    )

    parser.add_argument("--all", action="store_true", help="모든 테스트 실행")
    parser.add_argument("--unit", action="store_true", help="단위 테스트만 실행")
    parser.add_argument("--integration", action="store_true", help="통합 테스트만 실행")
    parser.add_argument("--e2e", action="store_true", help="E2E 테스트만 실행")
    parser.add_argument("--performance", action="store_true", help="성능 테스트 포함")
    parser.add_argument("--coverage", action="store_true", help="코드 커버리지 포함")
    parser.add_argument("--report", action="store_true", default=True, help="리포트 생성 (기본값)")

    args = parser.parse_args()

    # 기본값: 아무 옵션도 없으면 모든 테스트 실행
    if not any([args.all, args.unit, args.integration, args.e2e, args.performance]):
        args.all = True

    runner = TestRunner()
    results = []

    try:
        if args.all:
            results = runner.run_all_tests(
                coverage=args.coverage,
                performance=args.performance
            )
        else:
            if args.unit:
                results.append(runner.run_unit_tests(coverage=args.coverage))
            if args.integration:
                results.append(runner.run_integration_tests(coverage=args.coverage))
            if args.e2e:
                results.append(runner.run_e2e_tests())
            if args.performance:
                results.append(runner.run_performance_tests())

        # 결과 출력
        for result in results:
            print(f"\n{'='*60}")
            print(f"📋 {result['description']} 결과:")
            if result["success"]:
                print("✅ 성공")
            else:
                print("❌ 실패")
                print(f"오류: {result['stderr']}")

            print(f"실행 시간: {result['duration']:.2f}초")

        # 리포트 생성 및 저장
        if args.report and results:
            report = runner.generate_report(results)
            print(report)
            runner.save_report(report)

    except KeyboardInterrupt:
        print("\n⚠️ 사용자에 의해 테스트가 중단되었습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 테스트 실행 중 오류 발생: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()