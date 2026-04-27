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
    scraper = HeadlineScraper.__new__(HeadlineScraper)
    soup = BeautifulSoup(html, 'html.parser')
    headlines = scraper.extract_headlines(soup, domain='marketwatch.com')

    assert isinstance(headlines, list)
    assert len(headlines) == 2
    assert "Stocks rally as inflation cools" in headlines
    assert "Dow Jones hits record high" in headlines

def test_extract_headlines_generic_fallback():
    """
    Test HeadlineScraper.extract_headlines() correctly extracts h1/h2/h3
    headlines for an unknown domain (generic fallback).
    """
    html = """
    <html>
        <body>
            <h1>Breaking news in finance sector today</h1>
            <h2>Markets see major upward movement today</h2>
            <h3>OK</h3>
        </body>
    </html>
    """
    scraper = HeadlineScraper.__new__(HeadlineScraper)
    soup = BeautifulSoup(html, 'html.parser')
    headlines = scraper.extract_headlines(soup, domain='unknowndomain.com')

    assert isinstance(headlines, list)
    assert len(headlines) == 2  # h3 "OK" has <=3 words, filtered out
    assert "Breaking news in finance sector today" in headlines
    assert "Markets see major upward movement today" in headlines

def test_extract_headlines_no_matching_elements():
    """
    Test HeadlineScraper.extract_headlines() returns an empty list
    when soup contains no matching elements.
    """
    html = "<html><body><p>No headlines here</p></body></html>"
    scraper = HeadlineScraper.__new__(HeadlineScraper)
    soup = BeautifulSoup(html, 'html.parser')
    headlines = scraper.extract_headlines(soup, domain='marketwatch.com')

    assert headlines == []
