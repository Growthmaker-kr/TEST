#!/usr/bin/env python3
"""
이미지 광고 성과 분석 시스템
메인 실행 파일
"""

import sys
import argparse
from pathlib import Path

# src 모듈 임포트
sys.path.insert(0, str(Path(__file__).parent))

from src.data_loader import DataLoader
from src.analyzer import AdAnalyzer
from src.visualizer import Visualizer
from src.report_generator import ReportGenerator


def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(
        description='이미지 광고 성과 분석 시스템',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  %(prog)s --data data/raw/sample_ad_data.csv
  %(prog)s --data data/raw/sample_ad_data.csv --format html
  %(prog)s --data data/raw/sample_ad_data.csv --visualize
        """
    )

    parser.add_argument(
        '--data',
        type=str,
        default='data/raw/sample_ad_data.csv',
        help='분석할 데이터 파일 경로 (기본값: data/raw/sample_ad_data.csv)'
    )

    parser.add_argument(
        '--format',
        type=str,
        choices=['html', 'json', 'text', 'excel'],
        default='html',
        help='리포트 형식 (기본값: html)'
    )

    parser.add_argument(
        '--visualize',
        action='store_true',
        help='시각화 차트 생성'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='./data/reports/',
        help='출력 디렉토리 (기본값: ./data/reports/)'
    )

    args = parser.parse_args()

    print("=" * 60)
    print("이미지 광고 성과 분석 시스템")
    print("=" * 60)
    print()

    # 1. 데이터 로드
    print("📂 1단계: 데이터 로드")
    print("-" * 60)
    loader = DataLoader()
    data = loader.load_data(args.data)

    if data.empty:
        print("✗ 데이터 로드에 실패했습니다.")
        return 1

    # 데이터 유효성 검사
    if not loader.validate_data():
        print("✗ 데이터 유효성 검사에 실패했습니다.")
        return 1

    # 데이터 요약 출력
    summary = loader.get_data_summary()
    print(f"\n데이터 요약:")
    print(f"  - 총 레코드 수: {summary.get('total_records', 0):,}")
    print(f"  - 캠페인 수: {summary.get('campaigns', 0)}")
    print(f"  - 플랫폼: {', '.join(summary.get('platforms', []))}")
    if summary.get('date_range', {}).get('start'):
        print(f"  - 기간: {summary['date_range']['start']} ~ {summary['date_range']['end']}")
    print()

    # 2. 성과 분석
    print("📊 2단계: 성과 분석")
    print("-" * 60)
    analyzer = AdAnalyzer()
    analyzer.load_data(data)
    results = analyzer.analyze()

    # 주요 지표 출력
    total = results.get('total_metrics', {})
    print(f"\n전체 성과:")
    print(f"  - 총 노출수: {total.get('impressions', 0):,}")
    print(f"  - 총 클릭수: {total.get('clicks', 0):,}")
    print(f"  - 평균 CTR: {total.get('ctr', 0):.2f}%")
    print(f"  - 총 광고 비용: ₩{total.get('cost', 0):,.0f}")
    print(f"  - 평균 CPC: ₩{total.get('cpc', 0):,.0f}")

    if 'conversions' in total:
        print(f"  - 총 전환수: {total.get('conversions', 0):,}")
        print(f"  - 평균 CVR: {total.get('cvr', 0):.2f}%")
        print(f"  - 평균 CPA: ₩{total.get('cpa', 0):,.0f}")

    if 'roas' in total:
        print(f"  - ROAS: {total.get('roas', 0):.0f}%")

    print()

    # 3. 시각화 (옵션)
    if args.visualize:
        print("📈 3단계: 시각화 차트 생성")
        print("-" * 60)
        visualizer = Visualizer()
        visualizer.create_dashboard(analyzer.data, results, args.output)
        print()

    # 4. 리포트 생성
    print("📝 4단계: 리포트 생성")
    print("-" * 60)
    report_gen = ReportGenerator(args.output)

    if args.format == 'excel':
        report_path = report_gen.export_to_excel(analyzer.data, results)
    else:
        report_path = report_gen.generate_report(results, args.format)

    print()
    print("=" * 60)
    print("✓ 분석 완료!")
    print(f"리포트 위치: {report_path}")
    print("=" * 60)

    return 0


if __name__ == '__main__':
    sys.exit(main())
