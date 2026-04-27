# News Sentiment Classifier

This project **scrapes financial news headlines** from major business websites and then uses a **local LLM** (via **Ollama**) to **classify each headline as Positive, Negative, or Neutral** based on its sentiment.

It combines **Web Scraping**, **Local Language Models (LLMs)**, and **Object-Oriented Programming (OOP)** principles in Python.

## Project Features

- **Multi-source Scraping**: Automatically collects business headlines from multiple financial websites.
- **Headless Scraping**: Uses both `requests` and `selenium` with random User-Agents to mimic real users.
- **Headline Limiting**: Fetches a maximum of 5 headlines from each website.
- **Local Sentiment Analysis**: Analyzes the sentiment of each headline using an LLM (`llama3.2`) through Ollama.
- **Parallel Processing**: Uses `ThreadPoolExecutor` for concurrent sentiment analysis.
- **Modular OOP Design**:
  - Base classes (`BaseScraper`, `BaseLLM`)
  - Child classes (`HeadlineScraper`, `SentimentAnalyzer`)
- **Clean Input/Output**:
  - `urls.txt` for input URLs
  - `results.csv` for paired headlines, sentiments, source URLs, and timestamps.

## Prerequisites

- Windows/macOS/Linux
- Miniconda Installed
- Ollama Installed and Running
- Python 3.9 Installed

## Setting Up the Environment

### 1. Create and Activate Conda Environment from environment.yaml

```
conda env create -f environment.yaml
conda activate project3_env
```

## How to Use

### 1. Prepare `urls.txt`

Create a text file called `urls.txt` in the project folder, containing the URLs of financial websites you want to scrape.

Example:

```
https://www.marketwatch.com/
https://finance.yahoo.com/
https://www.businessinsider.com/
https://www.cnbc.com/business/
```

---

### 2. Run the Script

Make sure the Ollama service is running in the background!

Then, execute:

python project3.py

### 3. Output Files

After successful execution:

- **`results.csv`** — Contains all scraped headlines paired with their predicted sentiments, source URLs, and timestamps.

Example:

| headline | sentiment | source_url | timestamp |
|---|---|---|---|
| Today the market jumped 2000 points | positive | https://www.marketwatch.com/ | 2026-04-27T... |
| Nvidia stocks are having a bullish run | positive | https://finance.yahoo.com/ | 2026-04-27T... |
| Trader Joe is downsizing its business | negative | https://www.cnbc.com/business/ | 2026-04-27T... |



## Technologies Used

- **Python 3.9**
- **Ollama** (Local LLM API)
- **Selenium** + **Webdriver-Manager** (for dynamic web pages)
- **Requests** + **BeautifulSoup** (for fast static scraping)
- **Object-Oriented Programming** (Classes, Inheritance)
