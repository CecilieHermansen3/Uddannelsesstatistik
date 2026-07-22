"""
Henter Trivsel- og Fraværsdata fra uddannelsesstatistik.dk API'et
og gemmer dem som to CSV-filer, klar til at blive joinet på skole-ID.

Forudsætning: API_key.txt ligger i samme mappe som dette script.
"""

import json
import requests
import pandas as pd
from pathlib import Path

API_URL = "https://api.uddannelsesstatistik.dk/Api/v1/statistik"
KEY_PATH = Path(__file__).parent / "API_key.txt"

with open(KEY_PATH, "r") as f:
    API_KEY = f.read().strip()

HEADERS = {
    "content-type": "application/json",
    "authorization": f"Bearer {API_KEY}",
}

# ---- Indsæt forespørgsler her ----

QUERY_TRIVSEL = {
   "område": "GS",
   "emne": "TRIV",
   "underemne": "TRIVIND",
   "nøgletal": [
      "Andel Indikatorsvar"
   ],
   "detaljering": [
      "[Institution].[Beliggenhedskommune]",
      "[Klassetrin].[Klassetringruppe]",
      "[Skoleår].[Skoleår]",
      "[Trivselsindikator].[Trivselsindikator]",
      "[Trivselsindikator Svarintervaller].[Trivselsindikator Svarintervaller]"
   ],
   "filtre": {
      "[Skoleår].[Skoleår]": [
         "2024/2025"
      ],
      "[Trivselsindikator].[Trivselsindikator]": [
         "Generel trivsel"
      ]
   },
   "indlejret": False,
   "tomme_rækker": False,
   "formattering": "json",
   "side": 1
}

QUERY_TRIVSEL_TIME = {
   "område": "GS",
   "emne": "TRIV",
   "underemne": "TRIVIND",
   "nøgletal": [
      "Andel Indikatorsvar"
   ],
   "detaljering": [
      "[Institution].[Beliggenhedskommune]",
      "[Klassetrin].[Klassetringruppe]",
      "[Skoleår].[Skoleår]",
      "[Trivselsindikator].[Trivselsindikator]",
      "[Trivselsindikator Svarintervaller].[Trivselsindikator Svarintervaller]"
   ],
   "filtre": {
      "[Trivselsindikator].[Trivselsindikator]": [
         "Generel trivsel"
      ]
   },
   "indlejret": False,
   "tomme_rækker": False,
   "formattering": "json",
   "side": 1
}

QUERY_FRAVAER = {
    "område": "GS",
    "emne": "ELEVFRAV",
    "underemne": "FRAVAAR",
    "nøgletal": ["Gennemsnitligt fravær per skoleår"],
    "detaljering": [
        "[Institution].[Beliggenhedskommune]",
        "[Klassetrin].[Skoletrin]",
        "[Tid].[Skoleår]",
    ],
    "filtre": {
        "[Klassetrin].[Skoletrin]": [
            "10. klasse mv.",
            "Indskoling",
            "Mellemtrin",
            "Udskoling",
        ],
        "[Tid].[Skoleår]": ["2024/2025"]
    },
    "indlejret": False,
    "tomme_rækker": False,
    "formattering": "json",
    "side": 1,
}

QUERY_FRAVAER_TIME = {
    "område": "GS",
    "emne": "ELEVFRAV",
    "underemne": "FRAVAAR",
    "nøgletal": ["Gennemsnitligt fravær per skoleår"],
    "detaljering": [
        "[Institution].[Beliggenhedskommune]",
        "[Klassetrin].[Skoletrin]",
        "[Tid].[Skoleår]",
    ],
    "filtre": {
        "[Klassetrin].[Skoletrin]": [
            "10. klasse mv.",
            "Indskoling",
            "Mellemtrin",
            "Udskoling",
        ]
    },
    "indlejret": False,
    "tomme_rækker": False,
    "formattering": "json",
    "side": 1,
}



QUERY_FORAELDRE = {
   "område": "GS",
   "emne": "TRIV",
   "underemne": "TRIVSP",
   "nøgletal": [
      "Antal elever"
   ],
   "detaljering": [
      "[Forældres Højest Fuldførte Uddannelse].[Uddannelsesgruppe]",
      "[Institution].[Beliggenhedskommune]",
      "[Klassetrin].[Klassetringruppe]",
      "[Skoleår].[Skoleår]"
   ],
   "filtre": {
      "[Skoleår].[Skoleår]": [
         "2024/2025"
      ]
   },
   "indlejret": False,
   "tomme_rækker": False,
   "formattering": "json",
   "side": 1
}

QUERY_FORAELDRE_TIME = {
   "område": "GS",
   "emne": "TRIV",
   "underemne": "TRIVSP",
   "nøgletal": [
      "Antal elever"
   ],
   "detaljering": [
      "[Forældres Højest Fuldførte Uddannelse].[Uddannelsesgruppe]",
      "[Institution].[Beliggenhedskommune]",
      "[Klassetrin].[Klassetringruppe]",
      "[Skoleår].[Skoleår]"
   ],
   "indlejret": False,
   "tomme_rækker": False,
   "formattering": "json",
   "side": 1
}

def fetch(query: dict, label: str) -> pd.DataFrame:
    response = requests.post(API_URL, json=query, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)
    print(f"{label}: hentede {len(df)} rækker")
    return df


if __name__ == "__main__":
    df_trivsel = fetch(QUERY_TRIVSEL, "Trivsel")
    df_fravaer = fetch(QUERY_FRAVAER, "Fravær")

    df_trivsel.to_csv("trivsel_raw.csv", index=False)
    df_fravaer.to_csv("fravaer_raw.csv", index=False)

    print("\nKolonner i trivsel:", list(df_trivsel.columns))
    print("Kolonner i fravær:", list(df_fravaer.columns))

def to_float(series):
    """Parses Danish-formatted floats with ',' as decimal separator and '%' sign."""
    return (series.astype(str)
                  .str.replace('%', '', regex=False)
                  .str.replace(',', '.', regex=False)
                  .str.strip()
                  .astype(float))

def to_int_dk(series):
    """Parses Danish-formatted integers with '.' as thousands separator."""
    return (series.astype(str)
                  .str.replace('.', '', regex=False)
                  .astype(int))
