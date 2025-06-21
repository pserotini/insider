from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import MinMaxScaler, OrdinalEncoder

import pandas as pd


class TitanicPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        scaler: MinMaxScaler,
        ticket_encoder: OrdinalEncoder,
        age_bins: list[int],
    ) -> None:
        self.scaler = scaler
        self.ticket_encoder = ticket_encoder
        self.age_bins = age_bins

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        df = X.copy()

        df["age_group"] = pd.cut(df["age"], bins=self.age_bins, right=False).cat.codes
        df = df.drop(columns=["age"])

        df["ticket"] = self.ticket_encoder.transform(df[["ticket"]]).astype(int)

        df["ticket_count"] = df.groupby("ticket")["ticket"].transform("count")
        df["is_alone"] = (df["ticket_count"] == 1)

        df["sex"] = df["sex"].str.lower()
        df["sex_male"] = (df["sex"] == "male")

        df["embarked_Q"] = (df["embarked"] == "Q")
        df["embarked_S"] = (df["embarked"] == "S")

        cols_to_scale = ["sibsp", "parch", "fare", "ticket_count"]
        df[cols_to_scale] = self.scaler.transform(df[cols_to_scale])

        return df[
            [
                "pclass", "sibsp", "parch", "ticket", "fare",
                "age_group", "ticket_count", "is_alone",
                "sex_male", "embarked_Q", "embarked_S"
            ]
        ]