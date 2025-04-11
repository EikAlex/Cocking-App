from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from models import Vorrat, Zutat, Rezept, RezeptZutat
from sqlalchemy.orm import Session

# DB-Konfig aus Umgebungsvariablen
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "example")
DB_HOST = os.getenv("DB_HOST", "db:5432")
DB_NAME = os.getenv("POSTGRES_DB", "cooking_db")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Engine & Session-Factory
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def add_zutat_to_vorrat(db, name, einheit, menge, haltbar_bis):
    # Zutat suchen oder neu anlegen
    zutat = db.query(Zutat).filter(Zutat.name == name).first()
    if not zutat:
        zutat = Zutat(name=name, einheit=einheit)
        db.add(zutat)
        db.commit()
        db.refresh(zutat)

    # Vorratseintrag anlegen
    eintrag = Vorrat(
        zutat_id=zutat.id,
        menge_vorhanden=menge,
        haltbar_bis=haltbar_bis
    )
    db.add(eintrag)
    db.commit()


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
