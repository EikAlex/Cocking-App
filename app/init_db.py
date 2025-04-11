from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Zutat
from db import DATABASE_URL  
 

# # Engine erstellen (Verbindung zur DB)
# engine = create_engine(DATABASE_URL, echo=True)

# # Die Tabellen in der Datenbank erstellen
# Base.metadata.create_all(bind=engine)

# print("✅ Tabellen wurden erstellt!")


# Engine erstellen (Verbindung zur DB)
engine = create_engine(DATABASE_URL, echo=True)

# Die Tabellen in der Datenbank erstellen
Base.metadata.create_all(bind=engine)

print("✅ Tabellen wurden erstellt!")

# Session erstellen
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

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
            print(f"Zutat '{zutat_name}' hinzugefügt.")
        else:
            print(f"Zutat '{zutat_name}' ist bereits vorhanden.")

# Initialisiere Standard-Zutaten
initialize_default_zutaten(db)

# Schließen der Session
db.close()

print("✅ Standard-Zutaten wurden hinzugefügt, wenn noch nicht vorhanden.")
