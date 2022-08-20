from datapackage import Package
import pandas as pd

def get_sp_500_constituents() -> pd.DataFrame:
    """ Get the S&P 500 constituents. """
    url = 'https://datahub.io/core/s-and-p-500-companies/datapackage.json'

    package = Package(url)