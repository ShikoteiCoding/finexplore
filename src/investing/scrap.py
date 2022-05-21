from bs4 import BeautifulSoup
import requests

# Scrapper here
#
# Only functionnal as most of the scrapp will be specific
# Will be too code-heavy to find generalities in scrapping websites

HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

def scrap_ishares_holdings(url: str) -> list[str]:
    """
    Given an iShare URL, this returns the list of tickers and associated weight.
    """

    req = requests.get(url, HEADERS)
    soup = BeautifulSoup(req.content, 'html.parser')

    print(soup.prettify())

    return []