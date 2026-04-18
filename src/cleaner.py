import pandas as pd

class Cleaner:

    def _standarize_columns(self, df):
        df = df.copy()
        df.columns = [c.strip().lower() for c in df.columns]
        return df

    def clean_sales(self, df_sales):
        df = self._standarize_columns(df_sales)

        df["month"] = pd.to_datetime(df["date"], errors="coerce")
        df["units"] = pd.to_numeric(df["units"], errors="coerce").fillna(0)

        df = df[df["month"].notna()]
        return df.reset_index(drop=True)

    def clean_jdg(self, df_jdg):
        df = self._standarize_columns(df_jdg)

        df["month"] = pd.to_datetime(df["miesiac"], errors="coerce")

        df["own_channel_active"] = (
            df["jdg"]
            .fillna("active")
            .str.lower()
            .str.strip()
            .map({"active": 1, "zawieszona": 0})
        )

        df["own_channel_active"] = df["own_channel_active"].ffill().fillna(1)
        df["is_active"] = df["own_channel_active"] == 1

        return df[["month", "own_channel_active", "is_active"]]

    def enrich_sales_with_own_activity(self, df_sales, df_jdg):
        monthly = (
            df_sales.groupby("month", as_index=False)
            .agg(units=("units", "sum"))
        )

        merged = monthly.merge(df_jdg, on="month", how="left")
        merged["own_channel_active"] = merged["own_channel_active"].ffill().fillna(1)

        return merged

    def enrich_sales_with_own_activity_raw(self, df_sales, df_jdg):

        merged = df_sales.merge(df_jdg, on="month", how="left")

        merged["own_channel_active"] = merged["own_channel_active"].ffill().fillna(1)

        return merged
