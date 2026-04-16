"""
A cleaner module that prepare data for analysis
"""

import pandas as pd

class Cleaner:
    def __init__(self):
        pass

    def _standarize_columns(self, df):
        df = df.copy()
        new_cols = []
        for column in df.columns:
            clean_name = column.strip().lower()
            new_cols.append(clean_name)
        
        df.columns = new_cols
        return df
    
    def clean_sales(self, df_sales):
        df = self._standarize_columns(df_sales)

        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["units"] = pd.to_numeric(df["units"], errors="coerce")

        df["units"] = df["units"].fillna(0)
        df = df[df["units"] >= 0]
        df = df[df["date"].notna()]

        df = df.reset_index(drop=True)

        return df
    
    def clean_jdg(self, df_jdg):
        df = self._standarize_columns(df_jdg)
        df["month"] = pd.to_datetime(df["miesiac"], errors="coerce")
        
        df["jdg_active"] = df["jdg"].apply(
            lambda x: 0 if str(x).strip().lower() == "zawieszona" else 1
        )
        
        df = df[["month", "jdg_active"]]
        df = df.dropna(subset=["month"])

        print("JDG", df)
        return df
