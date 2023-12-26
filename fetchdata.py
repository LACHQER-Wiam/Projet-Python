import requests
import pandas as pd
from urllib.parse import quote

def get_dpe_batch(offset, batch_size, list_variables, after):
    variables = quote(",".join(list_variables))
    api_root = "https://koumoul.com/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines"
    url_api = f"{api_root}?offset={offset}&size={batch_size}&select={variables}&after={after}"

    print(url_api)

    req = requests.get(url_api)
    wb = req.json()

    df = pd.json_normalize(wb["results"])
    return df, len(wb["results"])


def get_dpe(var, size):

    batch_size = 10000
    offset = 0
    data_frames = []
    total_fetched = 0
    list_variables = var
    after = 3334

    while total_fetched < size:
        df, count = get_dpe_batch(offset, batch_size, list_variables,after)
        total_fetched += count

        if df.empty:
            break

        data_frames.append(df)
        offset += batch_size
        after = after*2

        print(f"Fetched {total_fetched} observations")
        print(offset)

    full_data = pd.concat(data_frames, ignore_index=True)

    return full_data

