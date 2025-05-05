# Import Required Libraries
import random
import time
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
    

    def scrape_with_requests(self, url):
        
        try:
            time.sleep(random.uniform(1, 2))  # Random delay to mimic human browsing
            response = requests.get(url, headers=self.get_random_headers(), timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except:
            return None  # If scraping fails, return None

    def scrape_with_selenium(self, url):
        
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
            options.add_argument(f'user-agent={random.choice(self.USER_AGENTS)}')  # Random user agent
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.get(url)
            time.sleep(random.uniform(2, 4))  # Wait for JavaScript to load
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            driver.quit()
            return soup
        except:
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
    
    with open(path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def write_lines(path, lines):
    
    with open(path, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')

# Main Program
def main():
    
    url_file = "urls.txt"         # Input: List of financial news websites
    prompt_file = "prompts.txt"   # Output: Scraped headlines
    output_file = "sentiments.txt"  # Output: Sentiment results

    urls = read_urls(url_file)
    scraper = HeadlineScraper()
    llm = SentimentAnalyzer()

    all_headlines = []

    # Scrape each URL
    for url in urls:
        print(f"Scraping: {url}")
        headlines = scraper.scrape(url)
        print(f"  Found {len(headlines)} headlines.")
        all_headlines.extend(headlines)

    # Save all scraped headlines
    write_lines(prompt_file, all_headlines)

    print("\nRunning Sentiment Analysis with Ollama...\n")

    # Analyze sentiments for each headline
    sentiments = [llm.analyze(h) for h in all_headlines]

    # Save sentiment results
    write_lines(output_file, sentiments)

    print(f"\n Done. {len(all_headlines)} headlines analyzed.")
    print(f"Prompts saved to: {prompt_file}")
    print(f"Sentiments saved to: {output_file}")

# Run Main
if __name__ == "__main__":
    main()
