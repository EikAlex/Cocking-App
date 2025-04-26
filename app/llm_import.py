import openai
from models import Rezept, RezeptZutat, Zutat
from sqlalchemy.orm import Session

# OpenAI API-Key laden
openai.api_key = None  

# System-Prompt für saubere Extraktion
system_prompt = """
Du bist ein intelligenter Rezept-Extraktionsassistent. 
Deine Aufgabe: Formatiere den folgenden Kochtext in ein sauberes Python-Objekt mit folgendem Aufbau:

{
  "name": "Rezeptname",
  "beschreibung": "Zubereitungsschritte",
  "portionen": 1,                # Optional: Falls im Text angegeben
  "kochzeit_minuten": 30,        # Optional: Falls im Text angegeben
  "zutaten": [
    {"name": "Mehl", "menge": 200},
    {"name": "Ei", "menge": 2},
    {"name": "Milch", "menge": 250}
  ]
}

Regeln:
- Mengen immer als ganze Zahl.
- Fehlende Mengen = 1.
- Portionen schätzen oder auf eine Portion die jeweiligen zutatenmengen berechnen.
- Ignoriere irrelevante Informationen (z.B. Werbungen, Links).
"""

def rezept_aus_text_extrahieren(text: str) -> dict:
    #Schickt Text an OpenAI und extrahiert strukturiertes Rezept
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        temperature=0
    )
    antwort = response['choices'][0]['message']['content']
    
    try:
        rezept_daten = eval(antwort)  # Achtung: eval() nur bei vertrauenswürdiger Quelle
        return rezept_daten
    except Exception as e:
        raise ValueError(f"Fehler beim Parsen der Antwort: {e}")

def rezept_speichern(db: Session, rezept_daten: dict):
    #Speichert ein extrahiertes Rezept und seine Zutaten in der DB
    rezept = Rezept(
        name=rezept_daten["name"],
        beschreibung=rezept_daten["beschreibung"]
    )
    db.add(rezept)
    db.commit()

    for z in rezept_daten["zutaten"]:
        zutat_obj = db.query(Zutat).filter(Zutat.name.ilike(z["name"])).first()
        if zutat_obj:
            rezept_zutat = RezeptZutat(
                rezept_id=rezept.id,
                zutat_id=zutat_obj.id,
                menge=z["menge"]
            )
            db.add(rezept_zutat)
    db.commit()
