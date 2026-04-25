from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List

@dataclass
class TickerTrend:
    ticker: str
    mentions: int
    sentiment_score: float
    source: str
    sector: str
    timestamp: str = datetime.now().isoformat()

def get_sample_data() -> List[TickerTrend]:
    return [
        TickerTrend("MRVL", 45, 0.9, "Perplexity", "Semiconductors"),
        TickerTrend("CGTX", 30, 0.75, "Claude.ai", "Biotech"),
        TickerTrend("MTZ", 55, 0.85, "Manus AI", "Infrastructure"),
    ]

if __name__ == "__main__":
    samples = get_sample_data()
    for s in samples:
        print(asdict(s))
