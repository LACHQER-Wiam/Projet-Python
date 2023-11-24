import requests
import pandas as pd

def get_dpe():
    size = 10000
    api_root = "https://koumoul.com/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines"
    url_api = f"{api_root}?size={size}&select=Etiquette_DPE%2CType_b%C3%A2timent%2CP%C3%A9riode_construction%2CHauteur_sous-plafond%2CSurface_habitable_logement%2CCode_postal_(brut)%2CType_%C3%A9nergie_n%C2%B01%2CType_%C3%A9nergie_n%C2%B02%2CType_%C3%A9nergie_n%C2%B03%2CIsolation_toiture_(0%2F1)%2CQualit%C3%A9_isolation_murs%2CQualit%C3%A9_isolation_plancher_bas%2CType_%C3%A9nergie_principale_chauffage%2CType_%C3%A9nergie_principale_ECS%2CType_ventilation"

    req = requests.get(url_api)
    wb = req.json()

    df = pd.json_normalize(wb["results"])
    return df

