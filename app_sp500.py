
from flask import Flask, jsonify, request
from flask_cors import CORS
import datetime as dt
import csv
import io
import requests
import yfinance as yf
import pandas as pd

app = Flask(__name__)
CORS(app)

# ---------- Utilities ----------
def _fmt_date(d):
    if isinstance(d, (pd.Timestamp, dt.date, dt.datetime)):
        return pd.to_datetime(d).strftime('%Y-%m-%d')
    return str(d)

def _safe(val, fallback='N/A'):
    return fallback if val is None else val

# ---------- Health ----------
@app.route('/api/health')
def health():
    return jsonify({'status': 'ok'})

# ---------- S&P500 proxy (avoids CORS on the client) ----------
# Source CSV columns: Symbol,Security,GICS Sector, ... (we only need these 3)
@app.route('/api/sp500')
def sp500():
    url = 'https://datahub.io/core/s-and-p-500-companies/_r/-/data/constituents.csv'
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        r.encoding = 'utf-8'
        f = io.StringIO(r.text)
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            rows.append({
                'symbol': row.get('Symbol', '').strip(),
                'name': row.get('Security', '').strip(),
                'sector': row.get('GICS Sector', '').strip()
            })
        return jsonify(rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ---------- Stock endpoints ----------
@app.route('/api/stock/<ticker>')
def stock_series(ticker):
    ticker = ticker.upper().strip()
    period = request.args.get('period', '1y')
    interval = request.args.get('interval', '1d')
    try:
        hist = yf.Ticker(ticker).history(period=period, interval=interval, auto_adjust=True)
        if hist is None or hist.empty:
            return jsonify({'error': 'No data for ticker'}), 404
        hist = hist.dropna(subset=['Close']).reset_index()
        data = [{'date': _fmt_date(row['Date']), 'price': float(row['Close'])} for _, row in hist.iterrows()]
        # company name
        info = {}
        try:
            info = yf.Ticker(ticker).get_info()
        except Exception:
            info = {}
        company_name = info.get('shortName') or info.get('longName') or ticker
        return jsonify({'company_name': company_name, 'data': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stock/<ticker>/info')
def stock_info(ticker):
    ticker = ticker.upper().strip()
    try:
        t = yf.Ticker(ticker)
        current_price = None
        try:
            fi = getattr(t, 'fast_info', None)
            if fi and hasattr(fi, 'last_price'):
                current_price = fi.last_price
            elif fi and isinstance(fi, dict):
                current_price = fi.get('last_price')
        except Exception:
            pass
        if current_price is None:
            # fallback from last close
            hist = t.history(period='5d', interval='1d', auto_adjust=True)
            if not hist.empty:
                current_price = float(hist['Close'].iloc[-1])
        info = {}
        try:
            info = t.get_info()
        except Exception:
            info = {}
        company_name = info.get('shortName') or info.get('longName') or ticker
        sector = info.get('sector') or 'N/A'
        return jsonify({
            'company_name': company_name,
            'current_price': current_price if current_price is not None else 'N/A',
            'sector': sector
        })
    except Exception as e:
        return jsonify({'company_name': 'N/A', 'current_price': 'N/A', 'sector': 'N/A', 'error': str(e)}), 500

if __name__ == '__main__':
    # Default: localhost:5000
    app.run(host='0.0.0.0', port=5000, debug=True)
