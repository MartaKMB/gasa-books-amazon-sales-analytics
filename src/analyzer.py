"""
Business logic for aggregations and KPIs
"""

from config.products import ASIN_TO_BOOK
from config.status import STATUS_MAP
from config.regions import MARKETPLACE_TO_REGION

class BaseAnalyzer:
    def __init__(self, df):
        self.df = df.copy()

        required = [
            "month", "title", "asin",
            "marketplace", "units", "own_channel_active"
        ]

        missing = [c for c in required if c not in self.df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        self.df = self.df[self.df["month"].notna()].copy()

        self._add_book_label()
        self._add_region()
        self._add_status()

    def _add_book_label(self):
        self.df["book"] = self.df["asin"].map(ASIN_TO_BOOK)

    def _add_region(self):
        region = (
            self.df["marketplace"]
            .str.split(".").str[-1]
            .str.upper()
        )
        self.df["region"] = region.replace(MARKETPLACE_TO_REGION)

    def _add_status(self):
        self.df["channel_status"] = self.df["own_channel_active"].map(STATUS_MAP)

class KPIAnalyzer(BaseAnalyzer):

    def kpis(self):
        return {
            "total_units": int(self.df["units"].sum()),
            "distinct_products": int(self.df["asin"].nunique()),
            "distinct_regions": int(self.df["region"].nunique()),
            "cannibalization_impact": self._status_impact()
        }

    def _status_impact(self):
        active = self.df[self.df["own_channel_active"] == 1]["units"].mean()
        suspended = self.df[self.df["own_channel_active"] == 0]["units"].mean()

        if active == 0:
            return 0.0

        return float((suspended - active) / active)

class AggregationAnalyzer(BaseAnalyzer):

    def by_product(self):
        return (
            self.df.groupby("book", as_index=False)
            .agg(total_units=("units", "sum"))
            .sort_values("total_units", ascending=False)
        )

    def by_region(self):
        return (
            self.df.groupby("region", as_index=False)
            .agg(total_units=("units", "sum"))
            .sort_values("total_units", ascending=False)
        )

    def by_month(self):
        df = self.df.copy()

        df["month"] = df["month"].dt.to_period("M").dt.to_timestamp()

        return (
            df.groupby("month", as_index=False)
            .agg(total_units=("units", "sum"))
            .sort_values("month")
        )

    def seasonality(self):
        df = self.df.copy()
        df["quarter"] = df["month"].dt.quarter

        return (
            df.groupby(["own_channel_active", "quarter"], as_index=False)
            .agg(avg_units=("units", "mean"))
            .sort_values(["quarter", "own_channel_active"])
        )
    
class CannibalizationAnalyzer(BaseAnalyzer):

    def sales_by_channel_status(self):
        return (
            self.df.groupby("channel_status", as_index=False)
            .agg(total_units=("units", "sum"))
            .sort_values("total_units", ascending=False)
        )

    def impact_summary(self):
        active = self.df[self.df["own_channel_active"] == 1]["units"]
        suspended = self.df[self.df["own_channel_active"] == 0]["units"]

        return {
            "active_avg": float(active.mean()),
            "suspended_avg": float(suspended.mean()),
            "difference": float(suspended.mean() - active.mean())
        }
