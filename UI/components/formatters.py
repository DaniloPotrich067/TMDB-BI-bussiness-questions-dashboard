import pandas as pd

def fmt2(x) -> str:
    if x is None or pd.isna(x):
        return "-"
    return f"{float(x):,.2f}"

def fmt0(x) -> str:
    if x is None or pd.isna(x):
        return "-"
    return f"{float(x):,.0f}"

def money_short(x) -> str:
    if x is None or pd.isna(x):
        return "-"
    x = float(x)
    sign = "-" if x < 0 else ""
    x = abs(x)

    if x >= 1e9:
        return f"{sign}${x/1e9:.2f}B"
    if x >= 1e6:
        return f"{sign}${x/1e6:.2f}M"
    if x >= 1e3:
        return f"{sign}${x/1e3:.2f}K"
    return f"{sign}${x:.2f}"

def pct2(x) -> str:
    if x is None or pd.isna(x):
        return "-"
    return f"{float(x)*100:.2f}%"
