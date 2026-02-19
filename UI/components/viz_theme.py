import altair as alt

PALETTE = {
    "ok": "#22c55e",
    "warn": "#f59e0b",
    "bad": "#ef4444",
    "info": "#60a5fa",
    "muted": "rgba(255,255,255,0.70)",
    "grid": "rgba(255,255,255,0.08)",
}

def enable_altair_theme():
    def _tmdb_dark():
        return {
            "config": {
                "background": None,
                "view": {"strokeOpacity": 0},
                "axis": {
                    "labelColor": PALETTE["muted"],
                    "titleColor": PALETTE["muted"],
                    "domainColor": PALETTE["grid"],
                    "tickColor": PALETTE["grid"],
                    "gridColor": PALETTE["grid"],
                    "gridOpacity": 1,
                    "labelFontSize": 12,
                    "titleFontSize": 12,
                },
                "legend": {
                    "labelColor": PALETTE["muted"],
                    "titleColor": PALETTE["muted"],
                    "labelFontSize": 12,
                    "titleFontSize": 12,
                },
                "title": {"color": "rgba(255,255,255,0.92)", "fontSize": 14},
            }
        }

    # Altair permite registrar e habilitar tema global por config [web:642]
    try:
        alt.themes.register("tmdb_dark", _tmdb_dark)
    except Exception:
        pass
    alt.themes.enable("tmdb_dark")
