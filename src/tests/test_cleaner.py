import pandas as pd
from src.cleaner import Cleaner

def test_clean_jdg_mapping():
    df = pd.DataFrame({
        "Miesiac": ["2024-06", "2024-07"],
        "JDG": [None, "zawieszona"]
    })

    cleaner = Cleaner()
    result = cleaner.clean_jdg(df)

    assert result.loc[0, "own_channel_active"] == 1
    assert result.loc[1, "own_channel_active"] == 0
