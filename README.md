# Auto News Translate

Auto News Translate is a Python-based automation system designed specifically for **journalists** to streamline **news monitoring and preliminary research**. Instead of manually tracking multiple sources and languages, the system automatically collects the latest news, extracts full articles, summarizes and translates them using AI, and delivers the processed content directly to **private Discord channels**.

The goal is to reduce repetitive monitoring work so journalists can focus on **fact-checking, analysis, and story development**.

---

## Key Features

* **Automated RSS Monitoring**
  Parses RSS feeds to detect newly published articles.

* **Full Article Extraction**
  Uses a web crawling tool to fetch complete article content instead of partial RSS snippets.

* **Token-Efficient Content Processing**
  Extracts only relevant information (title, source, publish date, main content) and converts it into **Markdown format**, minimizing token usage for LLM processing.

* **AI-Powered Translation & Summarization**
  Uses the **Gemini API** to summarize articles and translate them into the target language.

* **Discord Delivery**
  Automatically sends translated summaries and key content to **topic-specific Discord channels** via webhooks.

---

## System Workflow

1. Fetch RSS feeds from configured news sources
2. Detect and filter new articles
3. Crawl article pages to extract full content
4. Clean and convert content to Markdown
5. Send content to Gemini API for summarization and translation
6. Deliver formatted results to Discord webhooks

---

## Technologies Used

* **Python** (Object-Oriented Programming)
* **Pytest** for unit testing
* **Crawl4AI** for article crawling and extraction
* **Gemini API** for AI translation and summarization
* **Discord Webhooks** for content delivery
* **Playwright** (required dependency for crawling)

---

## Requirements

* Python 3.10+
* Playwright (must be installed separately)
* Valid Gemini API credentials
* Discord webhook URLs

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/auto-news-translate.git
cd auto-news-translate
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\\Scripts\\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright browsers

```bash
playwright install
```

> ⚠️ Playwright is required for full article extraction and must be installed separately.

---

## Configuration

1. Configure RSS feed sources
2. Set Gemini API credentials
3. Define Discord webhook URLs for each topic or language

Configuration is typically done via environment variables or a configuration file (depending on project setup).

---

## Running the Project

```bash
python main.py
```

The system will continuously monitor RSS feeds, process new articles, and send updates to Discord.

---

## Testing

Unit tests are written using **Pytest**.

```bash
pytest
```

---

## Use Cases

* Monitoring international news sources
* Early-stage research for breaking stories
* Translating foreign-language articles for newsroom review
* Private newsroom intelligence channels on Discord

---

## Notes

* This project is intended for **research and editorial assistance**, not automated publishing.
* Always verify translated and summarized content before publication.

---

## License

Specify your license here (e.g., MIT, Apache 2.0).

---

## Disclaimer

AI-generated summaries and translations may contain inaccuracies. Journalists should always verify facts and consult
