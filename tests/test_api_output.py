import pandas as pd
import requests
import pytest
import joblib

BASE_URL = "http://127.0.0.1:8000"

df = pd.read_csv("notebooks/data/train.csv")
df.columns = df.columns.str.lower()
predictions = pd.read_pickle("tests/valid_idx_predictions.pkl")

@pytest.mark.parametrize("i", pd.read_pickle('tests/valid_idx.pkl')[0:100])
# @pytest.mark.parametrize("i", range(10))
def test_prediction_matches(i):

    row = df.loc[i]
    expected = predictions.loc[i]

    input_json = {
        "pclass": int(row["pclass"]),
        "name": row["name"],
        "sex": row["sex"],
        "age": float(row["age"]),
        "sibsp": int(row["sibsp"]),
        "parch": int(row["parch"]),
        "ticket": row["ticket"],
        "fare": float(row["fare"]),
        "cabin": "",
        "embarked": row["embarked"],
        "passengerid": 0
    }

    
    response = requests.post(f"{BASE_URL}/predict", json=input_json)

    if response.json()["prediction"] != expected:
        print(f"i: {i}")
        print(input_json)
        
    assert response.status_code == 200
    assert response.json()["prediction"] == expected
