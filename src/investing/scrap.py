from bs4 import BeautifulSoup
import requests

# Scrapper here
#
# Only functionnal as most of the scrapp will be specific
# Will be too code-heavy to find generalities in scrapping websites

def scrap_ishares_holdings_download_link(url: str) -> list[str]:
    """
    Given an iShare URL, this returns the url to download data from.
    """

    export_classname = "fund-download fund-component-data-export"

    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    # Hypothesis: only one div with this class name
    export_class_div = soup.find_all(class_=export_classname)

    downloadable_urls = []

    for export_div in export_class_div:
        downloadable_urls.append(export_div.a.get("href"))

    return downloadable_urls

def download_ishares_holdings_data(url: str, store_path: str) -> bool:
    """
    Given a data url, download the file and store it in the folder path.
    Need to transform it to DataFrame
    """
    req = requests.get( url)

    return True
