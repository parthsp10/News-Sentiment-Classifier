# News Sentiment Classifier

This project **scrapes financial news headlines** from major business websites and then uses a **local LLM** (via **Ollama**) to **classify each headline as Positive, Negative, or Neutral** based on its sentiment.

It combines **Web Scraping**, **Local Language Models (LLMs)**, and **Object-Oriented Programming (OOP)** principles in Python.

## Project Features

- **Multi-source Scraping**: Automatically collects business headlines from multiple financial websites.
- **Headless Scraping**: Uses both `requests` and `selenium` with random User-Agents to mimic real users.
- **Headline Limiting**: Fetches a maximum of 5 headlines from each website.
- **Local Sentiment Analysis**: Analyzes the sentiment of each headline using an LLM (`llama3.2`) through Ollama.
- **Modular OOP Design**:
  - Base classes (`BaseScraper`, `BaseLLM`)
  - Child classes (`HeadlineScraper`, `SentimentAnalyzer`)
- **Clean Input/Output**:
  - `urls.txt` for input URLs
  - `prompts.txt` for scraped headlines
  - `sentiments.txt` for the model's sentiment predictions.

## Prerequisites

- Windows/macOS/Linux
- Miniconda Installed
- Ollama Installed and Running
- Python 3.9 Installed

## Setting Up the Environment

### 1. Create and Activate Conda Environment

conda create -n project3_env python=3.9 -y
conda activate project3_env


### 2. Install Python Dependencies

pip install requests beautifulsoup4 selenium webdriver-manager ollama

### 3. (Optional) Create environment.yml for reproducibility

conda env export > environment.yml

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

python project3_sentiment_classifier.py

### 3. Output Files

After successful execution:

- **`prompts.txt`** — Contains all the scraped financial headlines.
- **`sentiments.txt`** — Contains the predicted sentiments for each headline.

Example:

Today the market jumped 2000 points --> positive
Nvidia stocks are having a bullish run --> positive
Trader Joe is downsizing its business --> negative



## Technologies Used

- **Python 3.9**
- **Ollama** (Local LLM API)
- **Selenium** + **Webdriver-Manager** (for dynamic web pages)
- **Requests** + **BeautifulSoup** (for fast static scraping)
- **Object-Oriented Programming** (Classes, Inheritance)

