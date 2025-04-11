import streamlit as st
from datetime import datetime
from db import SessionLocal, Vorrat


def check_haltbarkeit(ablaufdatum):
    """
    Gibt einen farblich markierten HTML-String mit passendem Symbol je nach Haltbarkeit zurück.
    """
    heute = heute = datetime.today().date()
    tage_bis_ablauf = (ablaufdatum - heute).days

    if tage_bis_ablauf < 0:
        farbe = "red"
        symbol = "⚠️"
    elif tage_bis_ablauf <= 3:
        farbe = "orange"
        symbol = "⏳"
    else:
        farbe = "green"
        symbol = ""
    ablaufdatum = ablaufdatum.strftime("%d.%m.%Y")
    return f'<span style="color:{farbe}; font-size:18px;">{symbol} 📅 {ablaufdatum}</span>'

