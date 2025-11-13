"""
리포트 생성 모듈
광고 성과 분석 결과를 다양한 형식의 리포트로 생성합니다.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
import pandas as pd


class ReportGenerator:
    """광고 성과 분석 리포트를 생성하는 클래스"""

    def __init__(self, output_dir: str = './data/reports/'):
        """
        ReportGenerator 초기화

        Args:
            output_dir: 리포트 출력 디렉토리
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_report(self, results: Dict, format: str = 'html') -> str:
        """
        분석 결과 리포트 생성

        Args:
            results: 분석 결과 딕셔너리
            format: 리포트 형식 ('html', 'json', 'text')

        Returns:
            생성된 리포트 파일 경로
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        if format == 'html':
            return self.generate_html_report(results, f'report_{timestamp}.html')
        elif format == 'json':
            return self.generate_json_report(results, f'report_{timestamp}.json')
        elif format == 'text':
            return self.generate_text_report(results, f'report_{timestamp}.txt')
        else:
            print(f"✗ 지원하지 않는 형식: {format}")
            return ""

    def generate_html_report(self, results: Dict, filename: str) -> str:
        """
        HTML 형식 리포트 생성

        Args:
            results: 분석 결과
            filename: 파일명

        Returns:
            파일 경로
        """
        output_path = self.output_dir / filename

        total_metrics = results.get('total_metrics', {})

        html_content = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>이미지 광고 성과 분석 리포트</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        h1 {{
            margin: 0;
            font-size: 2.5em;
        }}
        .subtitle {{
            margin-top: 10px;
            opacity: 0.9;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .metric-card {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }}
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }}
        .metric-label {{
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .metric-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }}
        .section {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h2 {{
            color: #667eea;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #667eea;
            color: white;
            font-weight: bold;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .footer {{
            text-align: center;
            color: #666;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
        }}
        .chart-placeholder {{
            background: #f9f9f9;
            border: 2px dashed #ddd;
            padding: 40px;
            text-align: center;
            border-radius: 10px;
            margin: 20px 0;
            color: #999;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 이미지 광고 성과 분석 리포트</h1>
        <div class="subtitle">Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
    </div>

    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-label">총 노출수</div>
            <div class="metric-value">{total_metrics.get('impressions', 0):,}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">총 클릭수</div>
            <div class="metric-value">{total_metrics.get('clicks', 0):,}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">평균 CTR</div>
            <div class="metric-value">{total_metrics.get('ctr', 0):.2f}%</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">총 광고 비용</div>
            <div class="metric-value">₩{total_metrics.get('cost', 0):,.0f}</div>
        </div>
"""

        # 전환 데이터가 있으면 추가
        if 'conversions' in total_metrics:
            html_content += f"""
        <div class="metric-card">
            <div class="metric-label">총 전환수</div>
            <div class="metric-value">{total_metrics.get('conversions', 0):,}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">평균 CVR</div>
            <div class="metric-value">{total_metrics.get('cvr', 0):.2f}%</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">평균 CPA</div>
            <div class="metric-value">₩{total_metrics.get('cpa', 0):,.0f}</div>
        </div>
"""

        # ROAS 데이터가 있으면 추가
        if 'roas' in total_metrics:
            html_content += f"""
        <div class="metric-card">
            <div class="metric-label">ROAS</div>
            <div class="metric-value">{total_metrics.get('roas', 0):.0f}%</div>
        </div>
"""

        html_content += """
    </div>
"""

        # 캠페인별 성과
        if 'by_campaign' in results and results['by_campaign']:
            html_content += """
    <div class="section">
        <h2>캠페인별 성과</h2>
        <table>
            <thead>
                <tr>
                    <th>캠페인 ID</th>
                    <th>노출수</th>
                    <th>클릭수</th>
                    <th>CTR (%)</th>
                    <th>비용 (₩)</th>
                    <th>CPC (₩)</th>
                </tr>
            </thead>
            <tbody>
"""
            for campaign in results['by_campaign']:
                html_content += f"""
                <tr>
                    <td>{campaign.get('campaign_id', '-')}</td>
                    <td>{campaign.get('impressions', 0):,}</td>
                    <td>{campaign.get('clicks', 0):,}</td>
                    <td>{campaign.get('ctr', 0):.2f}</td>
                    <td>₩{campaign.get('cost', 0):,.0f}</td>
                    <td>₩{campaign.get('cpc', 0):,.0f}</td>
                </tr>
"""
            html_content += """
            </tbody>
        </table>
    </div>
"""

        # 플랫폼별 성과
        if 'by_platform' in results and results['by_platform']:
            html_content += """
    <div class="section">
        <h2>플랫폼별 성과</h2>
        <table>
            <thead>
                <tr>
                    <th>플랫폼</th>
                    <th>노출수</th>
                    <th>클릭수</th>
                    <th>CTR (%)</th>
                    <th>비용 (₩)</th>
                </tr>
            </thead>
            <tbody>
"""
            for platform in results['by_platform']:
                html_content += f"""
                <tr>
                    <td>{platform.get('platform', '-')}</td>
                    <td>{platform.get('impressions', 0):,}</td>
                    <td>{platform.get('clicks', 0):,}</td>
                    <td>{platform.get('ctr', 0):.2f}</td>
                    <td>₩{platform.get('cost', 0):,.0f}</td>
                </tr>
"""
            html_content += """
            </tbody>
        </table>
    </div>
"""

        html_content += """
    <div class="footer">
        <p>이미지 광고 성과 분석 시스템 v1.0</p>
        <p>© 2025 Growthmaker. All rights reserved.</p>
    </div>
</body>
</html>
"""

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✓ HTML 리포트 생성 완료: {output_path}")
        return str(output_path)

    def generate_json_report(self, results: Dict, filename: str) -> str:
        """
        JSON 형식 리포트 생성

        Args:
            results: 분석 결과
            filename: 파일명

        Returns:
            파일 경로
        """
        output_path = self.output_dir / filename

        report_data = {
            'generated_at': datetime.now().isoformat(),
            'results': results
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        print(f"✓ JSON 리포트 생성 완료: {output_path}")
        return str(output_path)

    def generate_text_report(self, results: Dict, filename: str) -> str:
        """
        텍스트 형식 리포트 생성

        Args:
            results: 분석 결과
            filename: 파일명

        Returns:
            파일 경로
        """
        output_path = self.output_dir / filename

        total_metrics = results.get('total_metrics', {})

        text_content = f"""
{'=' * 60}
이미지 광고 성과 분석 리포트
{'=' * 60}

생성 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'=' * 60}
전체 성과 요약
{'=' * 60}

총 노출수:      {total_metrics.get('impressions', 0):,}
총 클릭수:      {total_metrics.get('clicks', 0):,}
평균 CTR:       {total_metrics.get('ctr', 0):.2f}%
총 광고 비용:   ₩{total_metrics.get('cost', 0):,.0f}
평균 CPC:       ₩{total_metrics.get('cpc', 0):,.0f}
"""

        if 'conversions' in total_metrics:
            text_content += f"""
총 전환수:      {total_metrics.get('conversions', 0):,}
평균 CVR:       {total_metrics.get('cvr', 0):.2f}%
평균 CPA:       ₩{total_metrics.get('cpa', 0):,.0f}
"""

        if 'roas' in total_metrics:
            text_content += f"""
ROAS:           {total_metrics.get('roas', 0):.0f}%
"""

        if 'by_campaign' in results and results['by_campaign']:
            text_content += f"""
{'=' * 60}
캠페인별 성과
{'=' * 60}
"""
            for campaign in results['by_campaign']:
                text_content += f"""
캠페인: {campaign.get('campaign_id', '-')}
  노출수: {campaign.get('impressions', 0):,}
  클릭수: {campaign.get('clicks', 0):,}
  CTR: {campaign.get('ctr', 0):.2f}%
  비용: ₩{campaign.get('cost', 0):,.0f}
"""

        text_content += f"\n{'=' * 60}\n"

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text_content)

        print(f"✓ 텍스트 리포트 생성 완료: {output_path}")
        return str(output_path)

    def export_to_excel(self, data: pd.DataFrame, results: Dict, filename: str = 'report.xlsx') -> str:
        """
        Excel 형식으로 데이터 및 분석 결과 내보내기

        Args:
            data: 원본 데이터
            results: 분석 결과
            filename: 파일명

        Returns:
            파일 경로
        """
        output_path = self.output_dir / filename

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # 원본 데이터
            data.to_excel(writer, sheet_name='Raw Data', index=False)

            # 전체 요약
            if 'total_metrics' in results:
                summary_df = pd.DataFrame([results['total_metrics']])
                summary_df.to_excel(writer, sheet_name='Summary', index=False)

            # 캠페인별 성과
            if 'by_campaign' in results and results['by_campaign']:
                campaign_df = pd.DataFrame(results['by_campaign'])
                campaign_df.to_excel(writer, sheet_name='By Campaign', index=False)

            # 플랫폼별 성과
            if 'by_platform' in results and results['by_platform']:
                platform_df = pd.DataFrame(results['by_platform'])
                platform_df.to_excel(writer, sheet_name='By Platform', index=False)

        print(f"✓ Excel 리포트 생성 완료: {output_path}")
        return str(output_path)
