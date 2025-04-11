from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Zutat, Vorrat, Rezept, RezeptZutat
from util import initialize_default_zutaten
from datetime import date
from db import DATABASE_URL


# Engine erstellen (Verbindung zur DB)
engine = create_engine(DATABASE_URL, echo=True)

# Die Tabellen in der Datenbank erstellen
Base.metadata.create_all(bind=engine)

print("✅ Tabellen wurden erstellt!")

# Session erstellen
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

############################################################################
# Testdaten anlegen
if True:
# if False:
    # Zutaten anlegen
    mehl = Zutat(name="Mehl", einheit="g")
    ei = Zutat(name="Ei", einheit="Stück")
    milch = Zutat(name="Milch", einheit="ml")
    zucker = Zutat(name="Zucker", einheit="g")

    db.add_all([mehl, ei, milch, zucker])
    db.commit()

    # Vorrat anlegen
    db.add_all([
        Vorrat(zutat_id=mehl.id, menge_vorhanden=1000,
               haltbar_bis=date(2025, 12, 31)),
        Vorrat(zutat_id=ei.id, menge_vorhanden=6,
               haltbar_bis=date(2025, 5, 1)),
        Vorrat(zutat_id=milch.id, menge_vorhanden=500,
               haltbar_bis=date(2025, 4, 20)),
        Vorrat(zutat_id=zucker.id, menge_vorhanden=300,
               haltbar_bis=date(2026, 1, 1)),
    ])
    db.commit()

    # Rezept anlegen
    rezept = Rezept(name="Pfannkuchen",
                    beschreibung="Klassisches Rezept für 2 Portionen.")

    db.add(rezept)
    db.commit()

    # Zutaten mit Mengen für das Rezept
    db.add_all([
        RezeptZutat(rezept_id=rezept.id, zutat_id=mehl.id, menge=200),
        RezeptZutat(rezept_id=rezept.id, zutat_id=ei.id, menge=2),
        RezeptZutat(rezept_id=rezept.id, zutat_id=milch.id, menge=250),
        RezeptZutat(rezept_id=rezept.id, zutat_id=zucker.id, menge=50),
    ])
    db.commit()

    print("✅ Testdaten erfolgreich hinzugefügt.")
############################################################################

# Initialisiere Standard-Zutaten
initialize_default_zutaten(db)

# Schließen der Session
db.close()