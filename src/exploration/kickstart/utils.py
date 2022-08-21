from datapackage import Package, Resource
import pandas as pd

DATA_PATH = "data/"

def _scrap_sp_500_constituants() -> pd.DataFrame:
    """ Scrap the S&P 500 constituents. """
    url = 'https://datahub.io/core/s-and-p-500-companies/datapackage.json'

    resource_name = "constituents_csv"
    columns = ["symbol", "company", "sector"]

    package = Package(url)
    resource = package.get_resource(resource_name)
    if resource:
        table = resource.read()
        return pd.DataFrame(table, columns=columns)
    print("[INFO]: Resource is empty. Consider fixing the get_sp_500_constituents() scrapping function.")
    return pd.DataFrame()

def load_sp_500_constituents(reload=False) -> pd.DataFrame:
    """ Load or crap the S&P500 constituents. """
    filename = "s&p500_constituents.csv"
    if not reload:
        return pd.read_csv(DATA_PATH + filename, header=0)
    constituents = _scrap_sp_500_constituants()
    constituents.to_csv(DATA_PATH + filename)
    return constituents