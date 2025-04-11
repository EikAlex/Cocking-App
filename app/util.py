import streamlit as st
from datetime import datetime
from db import SessionLocal, Vorrat
from models import Vorrat, Zutat, Rezept, RezeptZutat

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


def delete_zutat_from_db(db, zutat_name):
    """Löscht eine Zutat aus der Datenbank."""
    zutat = db.query(Zutat).filter(Zutat.name == zutat_name).first()
    if zutat:
        db.delete(zutat)
        db.commit()
        return True
    return False