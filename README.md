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



## Run with Docker

The container holds the app, Python dependencies, and Chromium (for the Selenium fallback). **Ollama is not in the container. It runs on your host machine, and the container connects to it over the network.**

### Prerequisites

- Docker Desktop (or Docker Engine with the Compose plugin)
- Ollama installed and running on the host
- The model pulled on the host:

```
ollama pull llama3.2
```

### Build

```
docker compose build
```

### Run

```
docker compose run --rm classifier
```

The container reads `urls.txt` from your project folder (mounted read-only) and writes `results.csv` to `./output/results.csv` on your machine. To point at a different Ollama server, set `OLLAMA_HOST` (default `http://host.docker.internal:11434`):

```
OLLAMA_HOST=http://192.168.1.50:11434 docker compose run --rm classifier
```

### Run the tests

```
docker compose --profile test run --rm test
```

### Troubleshooting

- **`host.docker.internal` on Linux:** Docker Desktop provides it automatically. On Linux, `docker-compose.yml` maps it with `extra_hosts: host.docker.internal:host-gateway`, which needs Docker 20.10+. With plain `docker run`, add `--add-host=host.docker.internal:host-gateway`.
- **Ollama only listens on 127.0.0.1:** if the results show `error: Failed to connect to Ollama`, the container may not be able to reach a host server bound to loopback only. Start Ollama with `OLLAMA_HOST=0.0.0.0` (on Windows, set it as an environment variable and restart Ollama), then retry. Be aware this exposes Ollama to your network.
- **Chrome crashes or `/dev/shm` errors:** the app already passes `--disable-dev-shm-usage` in the container. If Chromium still runs out of shared memory, add `shm_size: "1gb"` to the service in `docker-compose.yml`.
- **Permission denied writing `./output` (Linux):** the container runs as UID 1000. Make the folder writable for that user, for example `mkdir -p output && chmod 777 output`.
- **`Found 0 headlines` for a site:** sites change their markup or block automated requests; this is scraping behaviour and is unrelated to Docker.

## Limitations

- **MarketWatch currently returns 0 headlines.** In a test run it answered plain `requests` calls with HTTP 401 and a DataDome bot-protection page, and headless Chromium received the same challenge page instead of the site. The CSS selector for MarketWatch is therefore untested against the live site, and the classifier does not try to bypass the protection. The other three sites returned 5 headlines each in that run.
- **Selenium is only a fallback for failed HTTP requests.** It runs when `requests` raises an error or gets an error status. It is not tried when the request succeeds but the page has no matching headlines, and the console does not say when the fallback ran.
- **Sentiment labels are not validated against human labels.** The model is asked for one word at temperature 0, and the reply is reduced to the first of `positive`, `negative` or `neutral` that appears as a whole word. Anything else becomes `unknown`, and Ollama failures are recorded as `error: ...`. No accuracy has been measured.
- **Which 5 headlines you get can change between runs**, because duplicates are removed with a set before the first 5 are taken. Selectors for the other sites may also break when the sites change their markup.

## Technologies Used

- **Python 3.9**
- **Ollama** (Local LLM API)
- **Selenium** + **Webdriver-Manager** (for dynamic web pages)
- **Requests** + **BeautifulSoup** (for fast static scraping)
- **Object-Oriented Programming** (Classes, Inheritance)
