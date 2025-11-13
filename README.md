# 이미지 광고 성과 분석 시스템

## 📊 프로젝트 개요

이미지 광고 성과 분석 시스템은 디지털 마케팅 캠페인의 이미지 광고 성과를 추적하고 분석하는 도구입니다. 다양한 지표를 통해 광고 효율성을 측정하고, 데이터 기반 의사결정을 지원합니다.

## 🎯 주요 기능

### 1. 성과 지표 추적
- **노출수(Impressions)**: 광고가 표시된 총 횟수
- **클릭수(Clicks)**: 사용자가 광고를 클릭한 횟수
- **클릭률(CTR)**: 클릭수 / 노출수 × 100
- **전환수(Conversions)**: 광고를 통해 발생한 전환 횟수
- **전환율(CVR)**: 전환수 / 클릭수 × 100
- **광고 비용(Cost)**: 광고 캠페인에 사용된 총 비용
- **클릭당 비용(CPC)**: 총 비용 / 클릭수
- **전환당 비용(CPA)**: 총 비용 / 전환수
- **광고 수익률(ROAS)**: 광고로 인한 수익 / 광고 비용 × 100

### 2. 이미지 분석
- **이미지 형식**: JPG, PNG, GIF, WebP 등
- **이미지 크기**: 파일 크기 및 해상도 분석
- **이미지 타입**: 정적 이미지, 애니메이션, 반응형 이미지
- **A/B 테스트**: 다양한 이미지 변형 성과 비교

### 3. 캠페인 관리
- 캠페인별 성과 비교
- 시간대별 성과 분석
- 타겟 오디언스별 성과 분석
- 플랫폼별 성과 비교 (Facebook, Instagram, Google Display Network 등)

## 📋 설치 방법

```bash
# 저장소 클론
git clone https://github.com/Growthmaker-kr/TEST.git
cd TEST

# 의존성 설치
npm install
# 또는
pip install -r requirements.txt
```

## 🚀 사용 방법

### 기본 사용

```python
# Python 예시
from image_ad_analyzer import AdAnalyzer

# 분석기 초기화
analyzer = AdAnalyzer()

# 광고 데이터 로드
analyzer.load_data('ad_performance_data.csv')

# 성과 분석 실행
results = analyzer.analyze()

# 결과 출력
analyzer.generate_report(results)
```

```javascript
// JavaScript 예시
const AdAnalyzer = require('./image-ad-analyzer');

// 분석기 초기화
const analyzer = new AdAnalyzer();

// 광고 데이터 로드
await analyzer.loadData('ad_performance_data.json');

// 성과 분석 실행
const results = await analyzer.analyze();

// 결과 출력
analyzer.generateReport(results);
```

## 📊 데이터 형식

### 입력 데이터 예시 (CSV/JSON)

```json
{
  "campaign_id": "CAMP_001",
  "ad_id": "AD_12345",
  "image_url": "https://example.com/ad-image.jpg",
  "impressions": 10000,
  "clicks": 250,
  "conversions": 15,
  "cost": 50000,
  "revenue": 150000,
  "date": "2025-11-13",
  "platform": "instagram"
}
```

## 📈 분석 리포트 예시

### 캠페인 성과 요약

| 지표 | 값 |
|------|-----|
| 총 노출수 | 100,000 |
| 총 클릭수 | 2,500 |
| 평균 CTR | 2.5% |
| 총 전환수 | 150 |
| 평균 CVR | 6.0% |
| 총 광고 비용 | ₩500,000 |
| 평균 CPC | ₩200 |
| 평균 CPA | ₩3,333 |
| ROAS | 300% |

## 🔧 설정

### config.json 예시

```json
{
  "data_source": "database",
  "database": {
    "host": "localhost",
    "port": 5432,
    "name": "ad_analytics"
  },
  "analysis": {
    "time_range": "last_30_days",
    "metrics": ["impressions", "clicks", "conversions", "cost"],
    "groupby": ["campaign_id", "platform"]
  },
  "report": {
    "format": "pdf",
    "include_charts": true,
    "export_path": "./reports/"
  }
}
```

## 📁 프로젝트 구조

```
.
├── README.md
├── config.json
├── data/
│   ├── raw/              # 원본 데이터
│   ├── processed/        # 가공된 데이터
│   └── reports/          # 생성된 리포트
├── src/
│   ├── analyzer.py       # 핵심 분석 로직
│   ├── data_loader.py    # 데이터 로드 모듈
│   ├── visualizer.py     # 시각화 모듈
│   └── report_generator.py  # 리포트 생성 모듈
├── tests/
│   └── test_analyzer.py
└── requirements.txt
```

## 🔍 주요 분석 방법론

### 1. 성과 지표 계산

```python
def calculate_ctr(impressions, clicks):
    """클릭률 계산"""
    return (clicks / impressions * 100) if impressions > 0 else 0

def calculate_cvr(clicks, conversions):
    """전환율 계산"""
    return (conversions / clicks * 100) if clicks > 0 else 0

def calculate_roas(revenue, cost):
    """광고 수익률 계산"""
    return (revenue / cost * 100) if cost > 0 else 0
```

### 2. A/B 테스트 분석

- 통계적 유의성 검정 (카이제곱 검정)
- 신뢰 구간 계산
- 승자 결정 알고리즘

### 3. 트렌드 분석

- 시계열 분석
- 이동 평균 계산
- 이상치 탐지

## 📊 시각화

지원되는 차트 유형:
- 막대 그래프 (Bar Chart): 캠페인별 성과 비교
- 선 그래프 (Line Chart): 시간대별 트렌드
- 파이 차트 (Pie Chart): 플랫폼별 비중
- 히트맵 (Heatmap): 시간대별/요일별 성과
- 퍼널 차트 (Funnel Chart): 전환 퍼널 분석

## 🤝 기여 방법

1. 이 저장소를 포크합니다
2. 새 브랜치를 생성합니다 (`git checkout -b feature/new-feature`)
3. 변경사항을 커밋합니다 (`git commit -m 'Add new feature'`)
4. 브랜치에 푸시합니다 (`git push origin feature/new-feature`)
5. Pull Request를 생성합니다

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 📞 문의

- 이메일: contact@growthmaker.kr
- 이슈 트래커: https://github.com/Growthmaker-kr/TEST/issues

## 📚 참고 자료

- [디지털 광고 성과 측정 가이드](https://example.com)
- [이미지 광고 최적화 베스트 프랙티스](https://example.com)
- [데이터 기반 마케팅 전략](https://example.com)

---

**Last Updated**: 2025-11-13
