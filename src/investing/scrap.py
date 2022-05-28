from bs4 import BeautifulSoup
import requests
import pandas as pd

from utils import load_json

# Scrapper here
#
# Only functionnal as most of the scrapp will be specific
# Will be too code-heavy to find generalities in scrapping websites

def scrap_ishares_holdings_download_link(url: str) -> list[str]:
    """
    Given an iShare URL, this returns the url to download data from.
    """

    export_classname = "holdings fund-component-data-export"

    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    # Hypothesis: only one div with this class name
    export_class_div = soup.find_all(class_=export_classname)

    downloadable_urls = []

    for export_div in export_class_div:
        downloadable_urls.append(export_div.a.get("href"))

    return downloadable_urls

def download_ishares_holdings_data(url: str, file_name: str, store_path: str = "") -> bool:
    """
    Given a data url, download the file and store it in the folder path.
    Need to transform it to DataFrame
    """
    req = requests.get("https://www.ishares.com/" + url, allow_redirects=True)

    print(url)
    #us/products/239738/ishares-global-clean-energy-etf/1467271812596.ajax?tab=all&fileType=json
    
    open(store_path + "/" + file_name, 'wb').write(req.content)

    return True

def convert_ishares_json_to_csv(json_file_path: str, csv_file_path: str) -> None:
    """
    From a json file provided, convert it and store to csv
    """
    dict_data = load_json(json_file_path, encoding="utf-8-sig")

    data = pd.DataFrame.from_dict(dict_data["aaData"]) 
    data.to_csv(csv_file_path)

    #print(type(dict_data))