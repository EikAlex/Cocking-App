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


def initialize_default_zutaten(db):
    # Liste mit Standard-Zutaten
    default_zutaten = [
        "Tomaten", "Kartoffeln", "Zwiebeln", "Knoblauch", "Salz", "Pfeffer",
        "Olivenöl", "Mehl", "Eier", "Milch", "Butter", "Hefe", "Paprika",
        "Kräuter", "Zucker", "Reis", "Pasta", "Linsen", "Hähnchenbrust", "Rindfleisch",
        "Schinken", "Mozzarella", "Parmesan", "Sahne", "Kochschinken", "Paprikapulver",
        "Chili", "Kaffee", "Kakaopulver", "Honig", "Essig", "Senf", "Balsamico",
        "Kokosmilch", "Gemüsebrühe", "Fisch", "Thunfisch", "Spinat", "Lauch", "Karotten"
    ]
    default_einheiten = [
        "g", "ml", "Stück", "TL", "EL", "Prise", "kg", "l", "Pck.", "Dose", "Glas"
    ]
    # Überprüfen, ob jede Zutat bereits existiert und hinzufügen, falls nicht
    for zutat_name in default_zutaten:
        # Überprüfen, ob die Zutat schon in der DB existiert
        zutat = db.query(Zutat).filter(Zutat.name == zutat_name).first()
        if not zutat:
            # Wenn die Zutat nicht existiert, fügen wir sie hinzu
            new_zutat = Zutat(name=zutat_name)
            db.add(new_zutat)
            db.commit()
            db.refresh(new_zutat)

    for einheit in default_einheiten:
        # Überprüfen, ob die Einheit schon in der DB existiert
        einheit_obj = db.query(Zutat).filter(Zutat.einheit == einheit).first()
        if not einheit_obj:
            # Wenn die Einheit nicht existiert, fügen wir sie hinzu
            new_einheit = Zutat(einheit=einheit)
            db.add(new_einheit)
            db.commit()
            db.refresh(new_einheit)
