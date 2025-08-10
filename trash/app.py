from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import logging

app = Flask(__name__)
CORS(app)

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    return """
    <h1>🚀 LSTM 주가 예측 API 서버</h1>
    <p>사용 가능한 엔드포인트:</p>
    <ul>
        <li><code>/api/stock/&lt;ticker&gt;</code> - 주가 데이터 조회</li>
        <li><code>/api/health</code> - 서버 상태 확인</li>
    </ul>
    <p>예시: <a href="/api/stock/AAPL">/api/stock/AAPL</a></p>
    """

@app.route('/api/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "message": "LSTM 주가 예측 API 서버가 정상 작동 중입니다! 🚀"
    })

@app.route('/api/stock/<ticker>')
def get_stock_data(ticker):
    try:
        logger.info(f"주가 데이터 요청: {ticker}")
        
        # yfinance로 주식 데이터 가져오기
        stock = yf.Ticker(ticker.upper())
        
        # 3개월 치 일별 데이터 가져오기
        hist = stock.history(period="3mo", interval="1d")
        
        if hist.empty:
            return jsonify({
                "error": f"'{ticker}' 종목을 찾을 수 없습니다.",
                "message": "올바른 종목 코드를 입력해주세요. (예: AAPL, GOOGL, TSLA)"
            }), 404
        
        # 데이터 정리 및 변환
        stock_data = []
        for date_index, row in hist.iterrows():
            stock_data.append({
                "date": date_index.strftime('%Y-%m-%d'),
                "price": round(float(row['Close']), 2),
                "open": round(float(row['Open']), 2),
                "high": round(float(row['High']), 2),
                "low": round(float(row['Low']), 2),
                "volume": int(row['Volume'])
            })
        
        # 종목 정보 가져오기
        info = stock.info
        company_name = info.get('longName', ticker.upper())
        
        logger.info(f"데이터 조회 완료: {ticker}, 데이터 개수: {len(stock_data)}")
        
        return jsonify({
            "ticker": ticker.upper(),
            "company_name": company_name,
            "data_count": len(stock_data),
            "data": stock_data,
            "last_updated": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"오류 발생 ({ticker}): {str(e)}")
        return jsonify({
            "error": "데이터 조회 중 오류가 발생했습니다.",
            "message": str(e),
            "ticker": ticker.upper()
        }), 500

@app.route('/api/stock/<ticker>/info')
def get_stock_info(ticker):
    """종목의 상세 정보를 가져오는 엔드포인트"""
    try:
        stock = yf.Ticker(ticker.upper())
        info = stock.info
        
        relevant_info = {
            "ticker": ticker.upper(),
            "company_name": info.get('longName', 'N/A'),
            "sector": info.get('sector', 'N/A'),
            "industry": info.get('industry', 'N/A'),
            "market_cap": info.get('marketCap', 'N/A'),
            "current_price": info.get('currentPrice', 'N/A'),
            "previous_close": info.get('previousClose', 'N/A'),
            "day_high": info.get('dayHigh', 'N/A'),
            "day_low": info.get('dayLow', 'N/A'),
            "52_week_high": info.get('fiftyTwoWeekHigh', 'N/A'),
            "52_week_low": info.get('fiftyTwoWeekLow', 'N/A'),
            "pe_ratio": info.get('trailingPE', 'N/A'),
            "dividend_yield": info.get('dividendYield', 'N/A')
        }
        
        return jsonify(relevant_info)
        
    except Exception as e:
        logger.error(f"종목 정보 조회 오류 ({ticker}): {str(e)}")
        return jsonify({
            "error": "종목 정보 조회 중 오류가 발생했습니다.",
            "message": str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "엔드포인트를 찾을 수 없습니다.",
        "message": "사용 가능한 엔드포인트를 확인해주세요."
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "서버 내부 오류가 발생했습니다.",
        "message": "잠시 후 다시 시도해주세요."
    }), 500

if __name__ == '__main__':
    print("🚀 LSTM 주가 예측 API 서버 시작!")
    print("📊 사용 가능한 엔드포인트:")
    print("   - http://localhost:5000/api/stock/<TICKER>")
    print("   - http://localhost:5000/api/stock/<TICKER>/info")
    print("   - http://localhost:5000/api/health")
    print("\n💡 예시:")
    print("   - http://localhost:5000/api/stock/AAPL")
    print("   - http://localhost:5000/api/stock/GOOGL/info")
    
    app.run(debug=True, host='0.0.0.0', port=5000)