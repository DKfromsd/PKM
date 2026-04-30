from flask import Flask, jsonify, render_template
from datetime import datetime
import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
DB_PATH = 'stock_trends.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/v1/trends', methods=['GET'])
def get_trends():
    try:
        if not os.path.exists(DB_PATH):
            return jsonify({
                "status": "warning",
                "message": "Database is empty. Please run crawler.py first.",
                "data": []
            })

        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch the latest 10 trending items
        cursor.execute('SELECT ticker, mentions, sentiment, source, sector, timestamp FROM trends ORDER BY timestamp DESC LIMIT 10')
        rows = cursor.fetchall()
        conn.close()

        trends = []
        for row in rows:
            trends.append({
                "ticker": row['ticker'],
                "mentions": row['mentions'],
                "sentiment": row['sentiment'],
                "source": row['source'],
                "sector": row['sector'],
                "timestamp": row['timestamp']
            })

        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "count": len(trends),
            "data": trends
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "data": []
        }), 500

if __name__ == '__main__':
    # Ensure DB exists before starting
    if not os.path.exists(DB_PATH):
        print("Database not found. Running initialization...")
        import database
        database.init_db()

    # Using port 5001 because port 5000 is often used by macOS AirPlay Receiver
    app.run(debug=True, port=5001)
