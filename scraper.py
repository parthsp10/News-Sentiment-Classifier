# Import required libraries
import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from webdriver_manager.chrome import ChromeDriverManager
import time 
import random 
from urllib.parse import urlparse

# List of user agents to rotate through to mimic different browsers
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
]

def get_random_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),  # Random browser signature
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',  # Preferred languages
        'Referer': 'https://www.google.com/'  # Fake referer
    }

def scrape_with_requests(url):
    try:
        # Random delay to prevent server overload detection
        time.sleep(random.uniform(1, 3))
        
        # Make HTTP GET request with random headers
        response = requests.get(url, headers=get_random_headers(), timeout=10)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Parse HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup, None
        
    except Exception as e:
        return None, f"Requests error: {str(e)}"

def scrape_with_selenium(url):
    try:
        # Configure Chrome options for headless browsing
        options = webdriver.ChromeOptions()
        options.add_argument('--headless') 
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument(f'user-agent={random.choice(USER_AGENTS)}')  # Random user agent
        
        # Initialize Chrome driver with automatic driver management
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        
        # Load the webpage
        driver.get(url)
        
        # Random delay to mimic human behavior
        time.sleep(random.uniform(3, 5))
        
        # Parse the rendered page source
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Clean up - close the browser
        driver.quit()
        return soup, None
        
    except Exception as e:
        return None, f"Selenium error: {str(e)}"

def extract_headlines(soup, domain):
    headlines = []
    
    # MarketWatch specific extraction
    if 'marketwatch.com' in domain:
        # Select headlines using CSS class
        for headline in soup.select('.article__headline'):
            headlines.append(headline.get_text(strip=True))
    
    # Yahoo Finance specific extraction
    elif 'yahoo.com' in domain:
        # Select all h3 elements and filter for meaningful content
        for headline in soup.select('h3'):
            text = headline.get_text(strip=True)
            if text and len(text.split()) > 3:  # Filter out short texts
                headlines.append(text)
    
    # Business Insider specific extraction
    elif 'businessinsider.com' in domain:
        # Try multiple selectors to catch different headline formats
        for headline in soup.select('.tout-title-link'):
            headlines.append(headline.get_text(strip=True))
        for headline in soup.select('.teaser-title'):
            headlines.append(headline.get_text(strip=True))
    
    # CNBC specific extraction
    elif 'cnbc.com' in domain:
        # Select headlines using CSS class
        for headline in soup.select('.Card-title'):
            headlines.append(headline.get_text(strip=True))
    
    # Generic fallback for unknown websites
    else:
        # Extract all heading tags (h1-h4) with meaningful content
        for headline in soup.find_all(['h1', 'h2', 'h3', 'h4']):
            text = headline.get_text(strip=True)
            if text and len(text.split()) > 3:  # Minimum word count filter
                headlines.append(text)
    
    return headlines

def clean_headlines(headlines):
    cleaned = []
    for headline in headlines:
        # Normalize whitespace (replace multiple spaces/newlines with single space)
        headline = ' '.join(headline.split())
        
        # Remove surrounding quotes and special characters
        headline = headline.strip('\"\'"')
        
        # Only keep non-empty headlines
        if headline:
            cleaned.append(headline)
    
    # Remove duplicate headlines while preserving order
    return list(set(cleaned))

def main():
    # Read URLs from input file
    with open('urls.txt', 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    
    all_headlines = []  # Store all collected headlines
    
    for url in urls:
        print(f"\nProcessing: {url}")
        domain = urlparse(url).netloc  # Extract domain from URL
        
        # First attempt: Try with requests (faster)
        soup, error = scrape_with_requests(url)
        
        # Fallback: If requests fails, try with Selenium
        if soup is None:
            print(f"Trying Selenium for {url} due to: {error}")
            soup, error = scrape_with_selenium(url)
            if soup is None:
                print(f"Failed to scrape {url}: {error}")
                continue  # Skip to next URL if both methods fail
        
        # Extract and clean headlines from the parsed HTML
        headlines = extract_headlines(soup, domain)
        cleaned_headlines = clean_headlines(headlines)
        
        # Add source domain to each headline and store
        all_headlines.extend([f"{domain}: {h}" for h in cleaned_headlines])
        print(f"Found {len(cleaned_headlines)} headlines from {domain}")
    
    # Save all collected headlines to output file
    with open('headlines.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_headlines))
    
    # Final status report
    print(f"\nTotal {len(all_headlines)} headlines saved to headlines.txt")

# Standard Python idiom to indicate main execution
if __name__ == "__main__":
    main()