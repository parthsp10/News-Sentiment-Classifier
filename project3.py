# Import Required Libraries
import random
import time
import csv
import concurrent.futures
from datetime import datetime
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import ollama

# Base Scraper Class
class BaseScraper:
    
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/91.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/91.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
    ]

    def get_random_headers(self):
        
        return {
            'User-Agent': random.choice(self.USER_AGENTS),
            'Accept': '*/*',
            'Referer': 'https://www.google.com/'
        }

    def scrape(self, url):
        
        raise NotImplementedError("Subclasses must implement the scrape method.")

# Headline Scraper Class
class HeadlineScraper(BaseScraper):

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument(f'user-agent={random.choice(self.USER_AGENTS)}')
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )

    def close(self):
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()
            self.driver = None

    def __del__(self):
        self.close()

    def scrape_with_requests(self, url):
        
        try:
            time.sleep(random.uniform(1, 2))  # Random delay to mimic human browsing
            response = requests.get(url, headers=self.get_random_headers(), timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            return None  # If scraping fails, return None

    def scrape_with_selenium(self, url):
        
        try:
            self.driver.get(url)
            time.sleep(random.uniform(2, 4))  # Wait for JavaScript to load
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            return soup
        except Exception as e:
            return None

    def extract_headlines(self, soup, domain):
        
        headlines = []
        if 'marketwatch.com' in domain:
            headlines = [h.get_text(strip=True) for h in soup.select('.article__headline')]
        elif 'yahoo.com' in domain:
            headlines = [h.get_text(strip=True) for h in soup.select('h3') if len(h.get_text(strip=True).split()) > 3]
        elif 'businessinsider.com' in domain:
            headlines += [h.get_text(strip=True) for h in soup.select('.tout-title-link, .teaser-title')]
        elif 'cnbc.com' in domain:
            headlines += [h.get_text(strip=True) for h in soup.select('.Card-title')]
        else:
            # Generic fallback for unknown domains
            headlines += [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3']) if len(h.get_text(strip=True).split()) > 3]
        return list(set(headlines))  # Remove duplicates

    def scrape(self, url):
        
        domain = urlparse(url).netloc
        soup = self.scrape_with_requests(url)
        if not soup:
            soup = self.scrape_with_selenium(url)
        headlines = self.extract_headlines(soup, domain) if soup else []
        return headlines[:5]  # Only return first 5 headlines

# Base LLM Class
class BaseLLM:
    
    def analyze(self, prompt):
        raise NotImplementedError("Subclasses must implement analyze method.")

# Sentiment Analyzer Class
class SentimentAnalyzer(BaseLLM):
    

    def __init__(self, model="llama3.2"):
        self.model = model

    def analyze(self, prompt):
        
        formatted_prompt = f"Classify the sentiment of this financial headline as positive, negative, or neutral:\n'{prompt}'"
        try:
            response = ollama.generate(model=self.model, prompt=formatted_prompt)
            return response['response'].strip().lower()
        except Exception as e:
            return f"error: {str(e)}"

# Helper Functions
def read_urls(path):
    try:
        with open(path, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
        print(f"Read {len(urls)} URLs from {path}")
        return urls
    except FileNotFoundError:
        print(f"Error: The file '{path}' was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Main Program
def main():
    
    url_file = "urls.txt"           # Input: List of financial news websites
    output_file = "results.csv"     # Output: Paired headlines and sentiments

    urls = read_urls(url_file)
    scraper = HeadlineScraper()
    llm = SentimentAnalyzer()

    all_headlines = []  # List of (headline, source_url) tuples

    # Scrape each URL
    for url in urls:
        print(f"Scraping: {url}")
        headlines = scraper.scrape(url)
        print(f"  Found {len(headlines)} headlines.")
        for h in headlines:
            all_headlines.append((h, url))

    scraper.close()

    print("\nRunning Sentiment Analysis with Ollama...\n")

    # Analyze sentiments in parallel using ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        sentiments = list(executor.map(llm.analyze, [h for h, _ in all_headlines]))

    # Write paired results to CSV
    timestamp = datetime.now().isoformat()
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['headline', 'sentiment', 'source_url', 'timestamp'])
        for (headline, source_url), sentiment in zip(all_headlines, sentiments):
            writer.writerow([headline, sentiment, source_url, timestamp])

    print(f"\n Done. {len(all_headlines)} headlines analyzed.")
    print(f"Results saved to: {output_file}")

# Run Main
if __name__ == "__main__":
    main()
