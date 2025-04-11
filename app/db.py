from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from models import Vorrat, Zutat, Rezept, RezeptZutat
from sqlalchemy.orm import Session
import streamlit as st

# DB-Konfig aus Umgebungsvariablen
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "example")
DB_HOST = os.getenv("DB_HOST", "db:5432")
DB_NAME = os.getenv("POSTGRES_DB", "cooking_db")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Engine & Session-Factory
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# def add_zutat_to_vorrat(db, name, einheit, menge, haltbar_bis):
#     # Zutat suchen oder neu anlegen
#     zutat = db.query(Zutat).filter(Zutat.name == name).first()
#     if not zutat:
#         zutat = Zutat(name=name, einheit=einheit)
#         db.add(zutat)
#         db.commit()
#         db.refresh(zutat)

#     # Vorratseintrag anlegen
#     eintrag = Vorrat(
#         zutat_id=zutat.id,
#         menge_vorhanden=menge,
#         haltbar_bis=haltbar_bis
#     )
#     db.add(eintrag)
#     db.commit()
def add_zutat_to_vorrat(db, name, einheit, menge, haltbar_bis):
    # Zutat suchen oder neu anlegen
    zutat = db.query(Zutat).filter(Zutat.name == name).first()
    
    if not zutat:
        # Zutat existiert nicht, also anlegen
        zutat = Zutat(name=name, einheit=einheit)
        db.add(zutat)
        db.commit()  # Sicherstellen, dass Zutat gespeichert wird
        db.refresh(zutat)

    # Prüfen, ob bereits ein Vorratseintrag für diese Zutat und dieses Haltbarkeitsdatum existiert
    vorratseintrag = db.query(Vorrat).filter(
        Vorrat.zutat_id == zutat.id, Vorrat.haltbar_bis == haltbar_bis
    ).first()

    if vorratseintrag:
        # Wenn Eintrag vorhanden ist, die Menge addieren
        vorratseintrag.menge_vorhanden += menge
        db.commit()  # Änderungen speichern
        st.success(f"✅ Menge für {name} wurde um {menge} erhöht. Neuer Vorrat: {vorratseintrag.menge_vorhanden} {einheit}.")
    else:
        # Wenn kein Eintrag vorhanden ist, neuen Vorratseintrag erstellen
        eintrag = Vorrat(
            zutat_id=zutat.id,
            menge_vorhanden=menge,
            haltbar_bis=haltbar_bis
        )
        db.add(eintrag)
        db.commit()  # Sicherstellen, dass der Vorratseintrag gespeichert wird
        st.success(f"✅ {name} wurde zum Vorrat hinzugefügt!")


def delete_vorratseintrag(db, vorrat_id: int):
    eintrag = db.query(Vorrat).filter(Vorrat.id == vorrat_id).first()
    if eintrag:
        db.delete(eintrag)
        db.commit()


def add_rezept(db, name, beschreibung, zutaten_liste):
    rezept = Rezept(name=name, beschreibung=beschreibung)
    db.add(rezept)
    db.commit()
    db.refresh(rezept)

    for zutat_id, menge in zutaten_liste:
        rz = RezeptZutat(rezept_id=rezept.id, zutat_id=zutat_id, menge=menge)
        db.add(rz)

    db.commit()
