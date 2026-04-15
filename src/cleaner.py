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
    
    def _drop_duplicates(self, df, subset=None):
        before = len(df)
        df = df.drop_duplicates(subset=subset)
        after = len(df)
        print(f"Dropped duplicates: {before} - {after}")
        return df
    
    def clean_sales(self, df_sales):
        df = self._standarize_columns(df_sales)

        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.to_period("M")
        df["units"] = pd.to_numeric(df["units"], errors="coerce")

        df["units"] = df["units"].fillna(0)
        df = df[df["units"] >= 0]

        df = df[df["date"].notna()]

        # df.self._drop_duplicates(df, subset=["sales_id"])
        df.reset_index(drop=True)

        print(df)
        return df
