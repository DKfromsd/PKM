from flask import Flask, jsonify
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Mock Data representing AI Ticker Trends
mock_trends = [
    {"ticker": "NVDA", "mentions": 120, "sentiment": 0.85, "source": "Perplexity", "sector": "Semiconductors"},
    {"ticker": "AAPL", "mentions": 95, "sentiment": 0.70, "source": "Claude.ai", "sector": "Technology"},
    {"ticker": "TSLA", "mentions": 80, "sentiment": 0.45, "source": "Manus AI", "sector": "Automotive"},
    {"ticker": "AMD", "mentions": 110, "sentiment": 0.80, "source": "Perplexity", "sector": "Semiconductors"},
]

@app.route('/')
def home():
    return "AI-Trend Stock Tracker API is running."

@app.route('/api/v1/trends', methods=['GET'])
def get_trends():
    return jsonify({
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "data": mock_trends
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
