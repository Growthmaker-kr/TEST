"""
광고 성과 분석 모듈
광고 데이터를 분석하고 주요 지표를 계산합니다.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from scipy import stats


class AdAnalyzer:
    """광고 성과를 분석하는 클래스"""

    def __init__(self):
        """AdAnalyzer 초기화"""
        self.data = None
        self.results = {}

    def load_data(self, data: pd.DataFrame):
        """
        분석할 데이터 로드

        Args:
            data: pandas DataFrame
        """
        self.data = data.copy()
        # 날짜 컬럼이 있으면 datetime으로 변환
        if 'date' in self.data.columns:
            self.data['date'] = pd.to_datetime(self.data['date'])

    @staticmethod
    def calculate_ctr(impressions: float, clicks: float) -> float:
        """
        클릭률(CTR) 계산

        Args:
            impressions: 노출수
            clicks: 클릭수

        Returns:
            클릭률 (%)
        """
        return (clicks / impressions * 100) if impressions > 0 else 0

    @staticmethod
    def calculate_cvr(clicks: float, conversions: float) -> float:
        """
        전환율(CVR) 계산

        Args:
            clicks: 클릭수
            conversions: 전환수

        Returns:
            전환율 (%)
        """
        return (conversions / clicks * 100) if clicks > 0 else 0

    @staticmethod
    def calculate_cpc(cost: float, clicks: float) -> float:
        """
        클릭당 비용(CPC) 계산

        Args:
            cost: 총 비용
            clicks: 클릭수

        Returns:
            클릭당 비용
        """
        return cost / clicks if clicks > 0 else 0

    @staticmethod
    def calculate_cpa(cost: float, conversions: float) -> float:
        """
        전환당 비용(CPA) 계산

        Args:
            cost: 총 비용
            conversions: 전환수

        Returns:
            전환당 비용
        """
        return cost / conversions if conversions > 0 else 0

    @staticmethod
    def calculate_roas(revenue: float, cost: float) -> float:
        """
        광고 수익률(ROAS) 계산

        Args:
            revenue: 수익
            cost: 비용

        Returns:
            광고 수익률 (%)
        """
        return (revenue / cost * 100) if cost > 0 else 0

    def calculate_metrics(self) -> pd.DataFrame:
        """
        모든 주요 지표 계산

        Returns:
            계산된 지표가 포함된 DataFrame
        """
        if self.data is None or self.data.empty:
            print("✗ 데이터가 없습니다.")
            return pd.DataFrame()

        # 필수 컬럼 확인
        required_columns = ['impressions', 'clicks', 'cost']
        if not all(col in self.data.columns for col in required_columns):
            print("✗ 필수 컬럼이 누락되었습니다.")
            return self.data

        # CTR 계산
        self.data['ctr'] = self.data.apply(
            lambda row: self.calculate_ctr(row['impressions'], row['clicks']), axis=1
        )

        # CPC 계산
        self.data['cpc'] = self.data.apply(
            lambda row: self.calculate_cpc(row['cost'], row['clicks']), axis=1
        )

        # CVR, CPA, ROAS는 해당 컬럼이 있을 때만 계산
        if 'conversions' in self.data.columns:
            self.data['cvr'] = self.data.apply(
                lambda row: self.calculate_cvr(row['clicks'], row['conversions']), axis=1
            )
            self.data['cpa'] = self.data.apply(
                lambda row: self.calculate_cpa(row['cost'], row['conversions']), axis=1
            )

        if 'revenue' in self.data.columns:
            self.data['roas'] = self.data.apply(
                lambda row: self.calculate_roas(row['revenue'], row['cost']), axis=1
            )

        return self.data

    def analyze(self) -> Dict:
        """
        전체 성과 분석 실행

        Returns:
            분석 결과 딕셔너리
        """
        if self.data is None or self.data.empty:
            print("✗ 분석할 데이터가 없습니다.")
            return {}

        # 지표 계산
        self.calculate_metrics()

        # 전체 요약
        total_impressions = self.data['impressions'].sum()
        total_clicks = self.data['clicks'].sum()
        total_cost = self.data['cost'].sum()

        self.results = {
            'total_metrics': {
                'impressions': int(total_impressions),
                'clicks': int(total_clicks),
                'cost': float(total_cost),
                'ctr': self.calculate_ctr(total_impressions, total_clicks),
                'cpc': self.calculate_cpc(total_cost, total_clicks)
            }
        }

        # 전환 데이터가 있으면 추가
        if 'conversions' in self.data.columns:
            total_conversions = self.data['conversions'].sum()
            self.results['total_metrics']['conversions'] = int(total_conversions)
            self.results['total_metrics']['cvr'] = self.calculate_cvr(total_clicks, total_conversions)
            self.results['total_metrics']['cpa'] = self.calculate_cpa(total_cost, total_conversions)

        # 수익 데이터가 있으면 추가
        if 'revenue' in self.data.columns:
            total_revenue = self.data['revenue'].sum()
            self.results['total_metrics']['revenue'] = float(total_revenue)
            self.results['total_metrics']['roas'] = self.calculate_roas(total_revenue, total_cost)

        # 캠페인별 분석
        if 'campaign_id' in self.data.columns:
            self.results['by_campaign'] = self._analyze_by_group('campaign_id')

        # 플랫폼별 분석
        if 'platform' in self.data.columns:
            self.results['by_platform'] = self._analyze_by_group('platform')

        # 일별 트렌드 분석
        if 'date' in self.data.columns:
            self.results['daily_trend'] = self._analyze_daily_trend()

        return self.results

    def _analyze_by_group(self, group_by: str) -> Dict:
        """
        특정 그룹별로 분석

        Args:
            group_by: 그룹화할 컬럼명

        Returns:
            그룹별 분석 결과
        """
        grouped = self.data.groupby(group_by).agg({
            'impressions': 'sum',
            'clicks': 'sum',
            'cost': 'sum'
        }).reset_index()

        # 지표 계산
        grouped['ctr'] = grouped.apply(
            lambda row: self.calculate_ctr(row['impressions'], row['clicks']), axis=1
        )
        grouped['cpc'] = grouped.apply(
            lambda row: self.calculate_cpc(row['cost'], row['clicks']), axis=1
        )

        return grouped.to_dict('records')

    def _analyze_daily_trend(self) -> Dict:
        """
        일별 트렌드 분석

        Returns:
            일별 트렌드 데이터
        """
        daily = self.data.groupby('date').agg({
            'impressions': 'sum',
            'clicks': 'sum',
            'cost': 'sum'
        }).reset_index()

        daily['date'] = daily['date'].dt.strftime('%Y-%m-%d')
        daily['ctr'] = daily.apply(
            lambda row: self.calculate_ctr(row['impressions'], row['clicks']), axis=1
        )

        return daily.to_dict('records')

    def compare_ab_test(self, group_a_filter: dict, group_b_filter: dict) -> Dict:
        """
        A/B 테스트 결과 비교

        Args:
            group_a_filter: A 그룹 필터 조건
            group_b_filter: B 그룹 필터 조건

        Returns:
            A/B 테스트 비교 결과
        """
        # 그룹 필터링
        group_a = self.data.copy()
        for key, value in group_a_filter.items():
            group_a = group_a[group_a[key] == value]

        group_b = self.data.copy()
        for key, value in group_b_filter.items():
            group_b = group_b[group_b[key] == value]

        # 각 그룹의 CTR 계산
        a_ctr = self.calculate_ctr(group_a['impressions'].sum(), group_a['clicks'].sum())
        b_ctr = self.calculate_ctr(group_b['impressions'].sum(), group_b['clicks'].sum())

        # 카이제곱 검정
        contingency_table = np.array([
            [group_a['clicks'].sum(), group_a['impressions'].sum() - group_a['clicks'].sum()],
            [group_b['clicks'].sum(), group_b['impressions'].sum() - group_b['clicks'].sum()]
        ])

        chi2, p_value, _, _ = stats.chi2_contingency(contingency_table)

        return {
            'group_a': {
                'impressions': int(group_a['impressions'].sum()),
                'clicks': int(group_a['clicks'].sum()),
                'ctr': a_ctr
            },
            'group_b': {
                'impressions': int(group_b['impressions'].sum()),
                'clicks': int(group_b['clicks'].sum()),
                'ctr': b_ctr
            },
            'statistical_test': {
                'chi2': float(chi2),
                'p_value': float(p_value),
                'significant': p_value < 0.05,
                'winner': 'A' if a_ctr > b_ctr else 'B' if b_ctr > a_ctr else 'Tie'
            }
        }

    def get_top_performers(self, metric: str = 'ctr', top_n: int = 5, group_by: str = 'campaign_id') -> pd.DataFrame:
        """
        최고 성과를 낸 캠페인/광고 조회

        Args:
            metric: 정렬 기준 지표
            top_n: 조회할 개수
            group_by: 그룹화 기준

        Returns:
            상위 성과 DataFrame
        """
        if group_by not in self.data.columns or metric not in self.data.columns:
            print(f"✗ 컬럼을 찾을 수 없습니다: {group_by} 또는 {metric}")
            return pd.DataFrame()

        return self.data.nlargest(top_n, metric)[[group_by, metric, 'impressions', 'clicks', 'cost']]
