import os
import sqlite3
import json
from datetime import datetime
from dotenv import load_dotenv
import anthropic

load_dotenv()

# Configuration
DB_PATH = 'stock_trends.db'
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

def fetch_trending_tickers():
    """
    Uses Claude API to analyze current trending stock tickers.
    In a real scenario, this would involve more complex prompt engineering or web search.
    """
    if not ANTHROPIC_API_KEY:
        print("Error: ANTHROPIC_API_KEY not found in .env")
        return []

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    prompt = """Analyze current market trends and provide 5 trending stock tickers that are frequently mentioned in the context of AI and Technology.
    Return the result ONLY as a JSON array of objects with the following keys:
    "ticker", "mentions" (estimated number), "sentiment" (0.0 to 1.0), "source" (use 'Claude Analysis'), "sector".
    Example: [{"ticker": "NVDA", "mentions": 150, "sentiment": 0.9, "source": "Claude Analysis", "sector": "Semiconductors"}]"""

    try:
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract content
        content = response.content[0].text
        data = json.loads(content)
        return data
    except Exception as e:
        print(f"Error calling Claude API: {e}")
        return []

def save_to_db(trends):
    if not trends:
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for item in trends:
        cursor.execute('''
            INSERT INTO trends (ticker, mentions, sentiment, source, sector)
            VALUES (?, ?, ?, ?, ?)
        ''', (item['ticker'], item['mentions'], item['sentiment'], item['source'], item['sector']))

    conn.commit()
    conn.close()
    print(f"Successfully saved {len(trends)} trending items to database.")

if __name__ == '__main__':
    print("Starting AI Crawler Agent...")
    trending_data = fetch_trending_tickers()
    if trending_data:
        save_to_db(trending_data)
    else:
        print("No data collected. Check API key or connection.")
