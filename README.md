# Auto News Translate

Auto News Translate is a Python-based automation system designed specifically for **journalists** to streamline **news monitoring**. Instead of manually tracking multiple sources and languages, the system automatically collects the latest news, extracts full articles, summarizes and translates them using AI, and delivers the processed content directly to **private Discord channels**.

The goal is to reduce repetitive monitoring work so journalists can focus on **fact-checking, analysis, and story development**.


## Key Features

* **Automated RSS Monitoring**
  Parses RSS feeds to detect newly published articles.

* **Full Article Extraction**
  Uses a web crawling tool to fetch complete article content instead of partial RSS snippets.

* **Token-Efficient Content Processing**
  Extracts only relevant information (title, source, publish date, main content) and converts it into **Markdown format**, minimizing token usage for LLM processing.

* **AI-Powered Translation & Summarization**
  Uses the **Gemini API** to summarize articles and translate them into the target language.

* **Asynchronous fetching and processing**
  Uses asyncio to perform concurrent article fetching, scraping and API requests, improving throughput and reducing overall processing time.


## Project set up

### 1. Create virtual environment and install dependencies with uv

```bash
uv sync
```

### 2. Create .env inside project directory

```bash
# Discord Configuration
WORLD_NEWS_WEBHOOK_URL=<your webhook url>
CANADA_NEWS_WEBHOOK_URL=<your webhook url>

# Google Gemini AI Configuration
GEMINI_API_KEY=<your api key>
```

### 3. schedule the script to run at desired time interval (15 min by default)
Use systemd service and timer in Linux or other methods to schedule the script to run.

> ⚠️ Playwright is required for full article extraction and must be installed separately.


## Use Cases

* Monitoring international news sources
* Translating foreign-language articles 
* Private newsroom intelligence channels on Discord


## Disclaimer
This project is for educational purposes only.
AI-generated summaries and translations may contain inaccuracies. Users should always verify facts and consult original sources before reporting.
