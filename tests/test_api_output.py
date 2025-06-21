import pandas as pd
import requests

BASE_URL = "http://127.0.0.1:8000"

df = pd.read_csv("notebooks/data/train.csv")
df.columns = df.columns.str.lower()
predictions = pd.read_pickle("tests/valid_idx_predictions.pkl")
valid_idx = pd.read_pickle("tests/valid_idx.pkl")

def test_all_predictions_match():
    mismatches = []

    for i in valid_idx:
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
            "cabin": "",  # valor dummy já que não é utilizado
            "embarked": row["embarked"],
            "passengerid": 0  # valor dummy já que não é utilizado
        }

        response = requests.post(f"{BASE_URL}/predict", json=input_json)

        if response.status_code != 200 or response.json()["prediction"] != expected:
            mismatches.append({
                "index": i,
                "input": input_json,
                "expected": int(expected),
                "got": response.json().get("prediction"),
                "status": response.status_code
            })

    assert not mismatches, f"Mismatch found in {len(mismatches)} cases: {mismatches}"
