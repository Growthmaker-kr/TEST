"""
AdAnalyzer 테스트
"""

import unittest
import sys
from pathlib import Path
import pandas as pd

# src 모듈 임포트
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analyzer import AdAnalyzer


class TestAdAnalyzer(unittest.TestCase):
    """AdAnalyzer 클래스 테스트"""

    def setUp(self):
        """테스트 설정"""
        self.analyzer = AdAnalyzer()

        # 테스트 데이터 생성
        self.test_data = pd.DataFrame({
            'campaign_id': ['CAMP_001', 'CAMP_001', 'CAMP_002'],
            'impressions': [10000, 15000, 20000],
            'clicks': [250, 375, 400],
            'conversions': [15, 22, 20],
            'cost': [50000, 75000, 100000],
            'revenue': [150000, 220000, 300000],
            'platform': ['instagram', 'instagram', 'facebook'],
            'date': ['2025-11-01', '2025-11-02', '2025-11-01']
        })

    def test_calculate_ctr(self):
        """CTR 계산 테스트"""
        ctr = self.analyzer.calculate_ctr(10000, 250)
        self.assertEqual(ctr, 2.5)

        # 노출수가 0인 경우
        ctr_zero = self.analyzer.calculate_ctr(0, 250)
        self.assertEqual(ctr_zero, 0)

    def test_calculate_cvr(self):
        """CVR 계산 테스트"""
        cvr = self.analyzer.calculate_cvr(250, 15)
        self.assertEqual(cvr, 6.0)

        # 클릭수가 0인 경우
        cvr_zero = self.analyzer.calculate_cvr(0, 15)
        self.assertEqual(cvr_zero, 0)

    def test_calculate_cpc(self):
        """CPC 계산 테스트"""
        cpc = self.analyzer.calculate_cpc(50000, 250)
        self.assertEqual(cpc, 200)

        # 클릭수가 0인 경우
        cpc_zero = self.analyzer.calculate_cpc(50000, 0)
        self.assertEqual(cpc_zero, 0)

    def test_calculate_cpa(self):
        """CPA 계산 테스트"""
        cpa = self.analyzer.calculate_cpa(50000, 15)
        self.assertAlmostEqual(cpa, 3333.33, places=2)

        # 전환수가 0인 경우
        cpa_zero = self.analyzer.calculate_cpa(50000, 0)
        self.assertEqual(cpa_zero, 0)

    def test_calculate_roas(self):
        """ROAS 계산 테스트"""
        roas = self.analyzer.calculate_roas(150000, 50000)
        self.assertEqual(roas, 300)

        # 비용이 0인 경우
        roas_zero = self.analyzer.calculate_roas(150000, 0)
        self.assertEqual(roas_zero, 0)

    def test_load_data(self):
        """데이터 로드 테스트"""
        self.analyzer.load_data(self.test_data)
        self.assertIsNotNone(self.analyzer.data)
        self.assertEqual(len(self.analyzer.data), 3)

    def test_calculate_metrics(self):
        """지표 계산 테스트"""
        self.analyzer.load_data(self.test_data)
        result = self.analyzer.calculate_metrics()

        # CTR, CPC 컬럼이 추가되었는지 확인
        self.assertIn('ctr', result.columns)
        self.assertIn('cpc', result.columns)
        self.assertIn('cvr', result.columns)
        self.assertIn('cpa', result.columns)
        self.assertIn('roas', result.columns)

    def test_analyze(self):
        """전체 분석 테스트"""
        self.analyzer.load_data(self.test_data)
        results = self.analyzer.analyze()

        # 결과에 total_metrics가 있는지 확인
        self.assertIn('total_metrics', results)

        total = results['total_metrics']
        self.assertIn('impressions', total)
        self.assertIn('clicks', total)
        self.assertIn('ctr', total)
        self.assertIn('conversions', total)
        self.assertIn('cvr', total)

        # 총 노출수 검증
        self.assertEqual(total['impressions'], 45000)

        # 총 클릭수 검증
        self.assertEqual(total['clicks'], 1025)

    def test_analyze_by_campaign(self):
        """캠페인별 분석 테스트"""
        self.analyzer.load_data(self.test_data)
        results = self.analyzer.analyze()

        # 캠페인별 분석 결과가 있는지 확인
        self.assertIn('by_campaign', results)

        # 2개의 캠페인이 있는지 확인
        self.assertEqual(len(results['by_campaign']), 2)

    def test_analyze_by_platform(self):
        """플랫폼별 분석 테스트"""
        self.analyzer.load_data(self.test_data)
        results = self.analyzer.analyze()

        # 플랫폼별 분석 결과가 있는지 확인
        self.assertIn('by_platform', results)

        # 2개의 플랫폼이 있는지 확인
        self.assertEqual(len(results['by_platform']), 2)


if __name__ == '__main__':
    unittest.main()
