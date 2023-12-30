import requests
import pandas as pd
from urllib.parse import quote


batch_size = 10000
after = 1 
api_root = "https://koumoul.com/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines"


def get_dpe_batch(url):
    response = requests.get(url)
    return response


def get_dpe(var, size=float('inf')):

    variables = quote(",".join(var))
    
    url_api = f"{api_root}?after={after}&size={batch_size}&select={variables}"

    results = []
    total_fetched = 0

    while url_api and total_fetched < size:
        response = get_dpe_batch(url_api)

        if response.status_code == 200:
            data = response.json()
            results.extend(data['results'])
            url_api = data.get('next')
            total_fetched = len(results)

        else:
            print("Failed to fetch data")
            break

        print(f"Fetched {total_fetched} observations")

    return pd.json_normalize(results)


