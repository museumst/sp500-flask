# 🚀 실시간 LSTM 주가 예측 시뮬레이터

Yahoo Finance API를 사용한 실시간 주가 데이터 기반 LSTM 주가 예측 시뮬레이터입니다.

## 📋 필요한 것들
- Python 3.7+
- 인터넷 연결 (Yahoo Finance API 사용)

## 🛠️ 설치 및 실행

### 1단계: 파일 다운로드
```
lstm-stock-predictor/
├── app.py              # Flask 백엔드 서버
├── index.html          # 프론트엔드 웹 페이지
├── requirements.txt    # Python 패키지 목록
└── README.md          # 이 파일
```

### 2단계: Python 패키지 설치
```bash
# 가상환경 생성 (권장)
python -m venv venv

# 가상환경 활성화
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt
```

### 3단계: Flask 서버 실행
```bash
python app.py
```

### 4단계: 웹 페이지 열기
브라우저에서 `index.html` 파일을 열면 됩니다.

## 🎯 사용 방법

1. **종목 코드 입력**
   - 미국 주식: AAPL, GOOGL, TSLA, MSFT
   - 한국 주식: 005930.KS (삼성전자)
   - 암호화폐: BTC-USD

2. **날짜 선택**
   - 달력에서 7일 이전의 날짜 선택
   - 충분한 거래 데이터가 있는 날짜 권장

3. **예측 실행**
   - 예측 버튼 클릭하여 결과 확인

## 🔧 API 엔드포인트

- `GET /api/health` - 서버 상태 확인
- `GET /api/stock/<ticker>` - 주가 데이터 조회
- `GET /api/stock/<ticker>/info` - 종목 상세 정보

## ❗ 문제 해결

### 서버 연결 실패
- Flask 서버 실행 상태 확인
- 포트 5000 사용 가능 여부 확인

### 종목 조회 실패
- 올바른 종목 코드 입력
- 인터넷 연결 확인

## 🌟 주요 기능

- ✅ **실시간 데이터**: Yahoo Finance API 연동
- ✅ **시간 여행 백테스트**: 과거 날짜 기준 예측
- ✅ **LSTM 시뮬레이션**: 5일 데이터로 다음날 예측
- ✅ **시각화**: Chart.js 그래프
- ✅ **정확도 측정**: 실제 vs 예측 비교

## 📊 지원 종목

- **미국 주식**: AAPL, GOOGL, TSLA, MSFT, AMZN, NVDA
- **한국 주식**: 005930.KS, 000660.KS, 035420.KS
- **ETF**: SPY, QQQ, VTI
- **암호화폐**: BTC-USD, ETH-USD
- **지수**: ^IXIC, ^GSPC, ^DJI

## 💡 사용 팁

- 대형주일수록 예측 정확도 향상
- 평일 거래일 기준 날짜 선택
- 안정적인 트렌드 구간에서 높은 정확도
- 여러 날짜로 테스트해보기 권장

즐거운 주가 예측 시뮬레이션을 경험해보세요! 🚀📈