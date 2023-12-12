import requests
import pandas as pd

def get_dpe(size=float('inf')):

    batch_size = 10000
    offset = 0
    data_frames = []
    total_fetched = 0

    def get_dpe_batch(offset, batch_size):
        api_root = "https://koumoul.com/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines"

        variables = quote(",".join(list_variables))
        url_api = f"{api_root}?offset={offset}&size={batch_size}&select={variables}"

        req = requests.get(url_api)
        wb = req.json()

        df = pd.json_normalize(wb["results"])
        return df, len(wb["results"])


def get_dpe(var, size=float('inf')):
    """
    Function aims to generate a data Frame from the extraction of data from the Ademe API
    it takes as variable input the list of desired variables is the size of the sample. 
    Args : 
        var (list) -> list of variables names
        size (int) -> size of the sample
    """

    batch_size = 10000
    offset = 0
    data_frames = []
    total_fetched = 0
    list_variables = var

    while total_fetched < size:
        df, count = get_dpe_batch(offset, batch_size, list_variables)
        total_fetched += count
        
        if df.empty:
            break

        data_frames.append(df)
        offset += batch_size

        print(f"Fetched {total_fetched} observations")

    full_data = pd.concat(data_frames, ignore_index=True)

    return full_data