"""
데이터 로드 모듈
CSV, JSON, Excel 파일에서 광고 데이터를 로드합니다.
"""

import pandas as pd
import json
from pathlib import Path
from typing import Optional, Union


class DataLoader:
    """광고 성과 데이터를 다양한 소스에서 로드하는 클래스"""

    def __init__(self, config_path: str = "config.json"):
        """
        DataLoader 초기화

        Args:
            config_path: 설정 파일 경로
        """
        self.config = self._load_config(config_path)
        self.data = None

    def _load_config(self, config_path: str) -> dict:
        """설정 파일 로드"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"설정 파일을 찾을 수 없습니다: {config_path}")
            return {}

    def load_csv(self, file_path: str) -> pd.DataFrame:
        """
        CSV 파일에서 데이터 로드

        Args:
            file_path: CSV 파일 경로

        Returns:
            pandas DataFrame
        """
        try:
            self.data = pd.read_csv(file_path)
            print(f"✓ CSV 파일 로드 완료: {file_path}")
            print(f"  - 레코드 수: {len(self.data)}")
            print(f"  - 컬럼: {list(self.data.columns)}")
            return self.data
        except Exception as e:
            print(f"✗ CSV 파일 로드 실패: {e}")
            return pd.DataFrame()

    def load_json(self, file_path: str) -> pd.DataFrame:
        """
        JSON 파일에서 데이터 로드

        Args:
            file_path: JSON 파일 경로

        Returns:
            pandas DataFrame
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # JSON이 리스트인 경우와 단일 객체인 경우 처리
            if isinstance(data, list):
                self.data = pd.DataFrame(data)
            else:
                self.data = pd.DataFrame([data])

            print(f"✓ JSON 파일 로드 완료: {file_path}")
            print(f"  - 레코드 수: {len(self.data)}")
            return self.data
        except Exception as e:
            print(f"✗ JSON 파일 로드 실패: {e}")
            return pd.DataFrame()

    def load_excel(self, file_path: str, sheet_name: str = 0) -> pd.DataFrame:
        """
        Excel 파일에서 데이터 로드

        Args:
            file_path: Excel 파일 경로
            sheet_name: 시트 이름 또는 인덱스

        Returns:
            pandas DataFrame
        """
        try:
            self.data = pd.read_excel(file_path, sheet_name=sheet_name)
            print(f"✓ Excel 파일 로드 완료: {file_path}")
            print(f"  - 레코드 수: {len(self.data)}")
            return self.data
        except Exception as e:
            print(f"✗ Excel 파일 로드 실패: {e}")
            return pd.DataFrame()

    def load_data(self, file_path: str) -> pd.DataFrame:
        """
        파일 확장자에 따라 자동으로 데이터 로드

        Args:
            file_path: 파일 경로

        Returns:
            pandas DataFrame
        """
        path = Path(file_path)

        if not path.exists():
            print(f"✗ 파일을 찾을 수 없습니다: {file_path}")
            return pd.DataFrame()

        extension = path.suffix.lower()

        if extension == '.csv':
            return self.load_csv(file_path)
        elif extension == '.json':
            return self.load_json(file_path)
        elif extension in ['.xlsx', '.xls']:
            return self.load_excel(file_path)
        else:
            print(f"✗ 지원하지 않는 파일 형식: {extension}")
            return pd.DataFrame()

    def validate_data(self) -> bool:
        """
        데이터 유효성 검사

        Returns:
            유효성 검사 통과 여부
        """
        if self.data is None or self.data.empty:
            print("✗ 데이터가 비어있습니다.")
            return False

        required_columns = ['campaign_id', 'impressions', 'clicks', 'cost']
        missing_columns = [col for col in required_columns if col not in self.data.columns]

        if missing_columns:
            print(f"✗ 필수 컬럼이 누락되었습니다: {missing_columns}")
            return False

        print("✓ 데이터 유효성 검사 통과")
        return True

    def get_data_summary(self) -> dict:
        """
        데이터 요약 정보 반환

        Returns:
            데이터 요약 딕셔너리
        """
        if self.data is None or self.data.empty:
            return {}

        return {
            'total_records': len(self.data),
            'columns': list(self.data.columns),
            'date_range': {
                'start': self.data['date'].min() if 'date' in self.data.columns else None,
                'end': self.data['date'].max() if 'date' in self.data.columns else None
            },
            'campaigns': self.data['campaign_id'].nunique() if 'campaign_id' in self.data.columns else 0,
            'platforms': self.data['platform'].unique().tolist() if 'platform' in self.data.columns else []
        }
