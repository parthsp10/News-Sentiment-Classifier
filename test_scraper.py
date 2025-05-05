from project3 import HeadlineScraper
from bs4 import BeautifulSoup

def test_extract_headlines_marketwatch():
    """
    Test HeadlineScraper.extract_headlines() correctly extracts headlines
    from a mocked MarketWatch HTML snippet.
    """
    html = """
    <html>
        <body>
            <div class="article__headline">Stocks rally as inflation cools</div>
            <div class="article__headline">Dow Jones hits record high</div>
        </body>
    </html>
    """
    scraper = HeadlineScraper()
    soup = BeautifulSoup(html, 'html.parser')
    headlines = scraper.extract_headlines(soup, domain='marketwatch.com')

    assert isinstance(headlines, list)
    assert len(headlines) == 2
    assert "Stocks rally as inflation cools" in headlines
    assert "Dow Jones hits record high" in headlines
