from datapackage import Package, Resource
import pandas as pd

def get_sp_500_constituents() -> pd.DataFrame :
    """ Get the S&P 500 constituents. """
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