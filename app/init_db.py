from sqlalchemy import create_engine
from models import Base
from db import DATABASE_URL  

# Engine erstellen (Verbindung zur DB)
engine = create_engine(DATABASE_URL, echo=True)

# Die Tabellen in der Datenbank erstellen
Base.metadata.create_all(bind=engine)

print("✅ Tabellen wurden erstellt!")
