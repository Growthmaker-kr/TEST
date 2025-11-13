"""
시각화 모듈
광고 성과 데이터를 다양한 차트로 시각화합니다.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, List


class Visualizer:
    """광고 성과를 시각화하는 클래스"""

    def __init__(self, style: str = 'seaborn-v0_8', figsize: tuple = (12, 8), dpi: int = 100):
        """
        Visualizer 초기화

        Args:
            style: matplotlib 스타일
            figsize: 그래프 크기
            dpi: 해상도
        """
        self.style = style
        self.figsize = figsize
        self.dpi = dpi

        # 스타일 설정
        try:
            plt.style.use(style)
        except:
            plt.style.use('default')

        sns.set_palette("husl")

    def plot_campaign_comparison(self, data: pd.DataFrame, metric: str = 'ctr',
                                  group_by: str = 'campaign_id',
                                  save_path: Optional[str] = None):
        """
        캠페인별 성과 비교 막대 그래프

        Args:
            data: 분석 데이터
            metric: 비교할 지표
            group_by: 그룹화 기준
            save_path: 저장 경로
        """
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)

        # 그룹별 집계
        grouped = data.groupby(group_by).agg({
            'impressions': 'sum',
            'clicks': 'sum',
            'cost': 'sum'
        }).reset_index()

        if metric == 'ctr':
            grouped['value'] = (grouped['clicks'] / grouped['impressions'] * 100)
            ylabel = 'CTR (%)'
        elif metric == 'cpc':
            grouped['value'] = (grouped['cost'] / grouped['clicks'])
            ylabel = 'CPC (₩)'
        else:
            grouped['value'] = grouped[metric] if metric in grouped.columns else 0
            ylabel = metric

        # 막대 그래프 그리기
        bars = ax.bar(grouped[group_by], grouped['value'], color=sns.color_palette("husl", len(grouped)))

        # 값 레이블 추가
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.2f}',
                   ha='center', va='bottom')

        ax.set_xlabel(group_by.replace('_', ' ').title())
        ax.set_ylabel(ylabel)
        ax.set_title(f'{ylabel} by {group_by.replace("_", " ").title()}')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            print(f"✓ 차트 저장: {save_path}")

        plt.close()

    def plot_trend(self, data: pd.DataFrame, metrics: List[str] = ['impressions', 'clicks'],
                   save_path: Optional[str] = None):
        """
        시간대별 트렌드 선 그래프

        Args:
            data: 분석 데이터 (date 컬럼 필요)
            metrics: 표시할 지표 리스트
            save_path: 저장 경로
        """
        if 'date' not in data.columns:
            print("✗ date 컬럼이 필요합니다.")
            return

        fig, axes = plt.subplots(len(metrics), 1, figsize=(self.figsize[0], self.figsize[1] * len(metrics) / 2),
                                dpi=self.dpi)

        if len(metrics) == 1:
            axes = [axes]

        data_sorted = data.copy()
        data_sorted['date'] = pd.to_datetime(data_sorted['date'])
        daily = data_sorted.groupby('date')[metrics].sum().reset_index()

        for idx, metric in enumerate(metrics):
            axes[idx].plot(daily['date'], daily[metric], marker='o', linewidth=2)
            axes[idx].set_ylabel(metric.replace('_', ' ').title())
            axes[idx].set_title(f'{metric.replace("_", " ").title()} Trend')
            axes[idx].grid(True, alpha=0.3)

        axes[-1].set_xlabel('Date')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            print(f"✓ 차트 저장: {save_path}")

        plt.close()

    def plot_platform_distribution(self, data: pd.DataFrame, metric: str = 'cost',
                                   save_path: Optional[str] = None):
        """
        플랫폼별 분포 파이 차트

        Args:
            data: 분석 데이터
            metric: 표시할 지표
            save_path: 저장 경로
        """
        if 'platform' not in data.columns:
            print("✗ platform 컬럼이 필요합니다.")
            return

        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)

        platform_data = data.groupby('platform')[metric].sum()

        colors = sns.color_palette("husl", len(platform_data))
        wedges, texts, autotexts = ax.pie(platform_data, labels=platform_data.index,
                                           autopct='%1.1f%%', colors=colors,
                                           startangle=90)

        # 텍스트 스타일 개선
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        ax.set_title(f'{metric.replace("_", " ").title()} Distribution by Platform')
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            print(f"✓ 차트 저장: {save_path}")

        plt.close()

    def plot_funnel(self, impressions: int, clicks: int, conversions: int,
                   save_path: Optional[str] = None):
        """
        전환 퍼널 차트

        Args:
            impressions: 노출수
            clicks: 클릭수
            conversions: 전환수
            save_path: 저장 경로
        """
        fig, ax = plt.subplots(figsize=(10, 8), dpi=self.dpi)

        stages = ['Impressions', 'Clicks', 'Conversions']
        values = [impressions, clicks, conversions]
        percentages = [100, (clicks/impressions*100) if impressions > 0 else 0,
                      (conversions/impressions*100) if impressions > 0 else 0]

        colors = ['#3498db', '#2ecc71', '#e74c3c']

        # 퍼널 그리기
        for i, (stage, value, pct, color) in enumerate(zip(stages, values, percentages, colors)):
            width = pct / 100
            ax.barh(i, width, height=0.8, color=color, alpha=0.8)
            ax.text(0.5, i, f'{stage}\n{value:,} ({pct:.1f}%)',
                   ha='center', va='center', fontweight='bold', fontsize=12)

        ax.set_xlim(0, 1)
        ax.set_ylim(-0.5, len(stages) - 0.5)
        ax.set_yticks([])
        ax.set_xticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.set_title('Conversion Funnel', fontsize=16, fontweight='bold')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            print(f"✓ 차트 저장: {save_path}")

        plt.close()

    def plot_heatmap(self, data: pd.DataFrame, save_path: Optional[str] = None):
        """
        시간대별/요일별 성과 히트맵

        Args:
            data: 분석 데이터 (date 컬럼 필요)
            save_path: 저장 경로
        """
        if 'date' not in data.columns:
            print("✗ date 컬럼이 필요합니다.")
            return

        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)

        data_copy = data.copy()
        data_copy['date'] = pd.to_datetime(data_copy['date'])
        data_copy['weekday'] = data_copy['date'].dt.day_name()
        data_copy['week'] = data_copy['date'].dt.isocalendar().week

        # 요일별, 주별 CTR 계산
        heatmap_data = data_copy.groupby(['weekday', 'week']).agg({
            'impressions': 'sum',
            'clicks': 'sum'
        }).reset_index()

        heatmap_data['ctr'] = (heatmap_data['clicks'] / heatmap_data['impressions'] * 100)

        pivot = heatmap_data.pivot(index='weekday', columns='week', values='ctr')

        # 요일 순서 정렬
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        pivot = pivot.reindex([day for day in weekday_order if day in pivot.index])

        sns.heatmap(pivot, annot=True, fmt='.2f', cmap='YlOrRd', ax=ax, cbar_kws={'label': 'CTR (%)'})
        ax.set_title('CTR Heatmap by Weekday and Week')
        ax.set_xlabel('Week Number')
        ax.set_ylabel('Day of Week')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            print(f"✓ 차트 저장: {save_path}")

        plt.close()

    def create_dashboard(self, data: pd.DataFrame, results: dict, output_dir: str = './data/reports/'):
        """
        모든 차트를 포함한 대시보드 생성

        Args:
            data: 분석 데이터
            results: 분석 결과
            output_dir: 출력 디렉토리
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        print("대시보드 차트 생성 중...")

        # 1. 캠페인별 CTR 비교
        if 'campaign_id' in data.columns:
            self.plot_campaign_comparison(data, metric='ctr', group_by='campaign_id',
                                         save_path=f'{output_dir}/campaign_ctr.png')

        # 2. 트렌드 차트
        if 'date' in data.columns:
            self.plot_trend(data, metrics=['impressions', 'clicks', 'cost'],
                          save_path=f'{output_dir}/trend.png')

        # 3. 플랫폼 분포
        if 'platform' in data.columns:
            self.plot_platform_distribution(data, metric='cost',
                                          save_path=f'{output_dir}/platform_distribution.png')

        # 4. 전환 퍼널
        if 'total_metrics' in results:
            metrics = results['total_metrics']
            if 'conversions' in metrics:
                self.plot_funnel(metrics['impressions'], metrics['clicks'], metrics['conversions'],
                               save_path=f'{output_dir}/funnel.png')

        # 5. 히트맵
        if 'date' in data.columns and len(data) > 7:
            self.plot_heatmap(data, save_path=f'{output_dir}/heatmap.png')

        print(f"✓ 대시보드 차트 생성 완료: {output_dir}")
