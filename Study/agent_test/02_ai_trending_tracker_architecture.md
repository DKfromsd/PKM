# 🏗️ AI-Trend Stock Tracker Architecture

## 1. Overview
This project aims to build a real-time stock trend analysis platform that aggregates data from various AI tools (Perplexity, Claude, Manus AI, etc.) using web scraping or API integration. The extracted ticker information is analyzed for sentiment and frequency, then visualized on a full-stack web dashboard.

## 2. Technical Stack
- **Frontend**: React (Next.js) + Tailwind CSS + Shadcn UI
- **Backend**: Python (Flask) for the prototype, eventually deploying to Cloudflare Workers/Pages.
- **Database**: PostgreSQL (Metadata & Tickers) + Redis (Caching)
- **Deployment**: Cloudflare Pages / Workers
- **Authentication**: JWT-based secure login

## 3. Data Acquisition Strategy
- **Agents**: Specialized scrapers for each AI platform.
- **Input**: Natural language queries to AI tools about trending stocks.
- **Output**: JSON data containing Tickers, Sentiment, and Source.

## 4. System Components
- **Crawler Agent**: Periodically queries AI tools and extracts ticker data.
- **Data Processor**: Normalizes and scores trends using a Semantic Model.
- **API Server**: Serves processed trend data to the frontend.
- **Dashboard**: Real-time visualization using Recharts/Chart.js.
