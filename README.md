# 🥘 Digitale Kochbuch-App mit Vorratsverwaltung

Willkommen zur digitalen Kochbuch-App mit integrierter Vorratsverwaltung!  
Diese Anwendung wurde mit **Python** und **Streamlit** erstellt und bietet eine einfache und moderne Benutzeroberfläche für das Verwalten von Rezepten und Vorräten.  
Die Daten werden in einer **PostgreSQL-Datenbank** gespeichert und mithilfe von **SQLAlchemy** und **Docker** verwaltet.

---

## 🚀 Features

- 🧺 Vorratsverwaltung: Behalte den Überblick über Zutaten, Bestände & Verfallsdatum
- 📖 Rezeptverwaltung: Hinzufügen, Bearbeiten und Anzeigen von Rezepten
- 🔄 Integration: Verknüpfung von Rezepten mit Vorratsdaten
- 🐳 Containerisiert mit Docker für einfache Bereitstellung
<!-- - 🔍 Such- und Filterfunktion für einfache Bedienung -->

---

## 🛠️ Tech-Stack

| Komponente       | Beschreibung                         |
|------------------|--------------------------------------|
| 🐍 Python         | Programmiersprache der Wahl          |
| 🌐 Streamlit      | Web-Interface für die Anwendung      |
| 🐘 PostgreSQL     | Datenbank für Rezepte & Vorräte      |
| 🧪 SQLAlchemy     | ORM für Datenbankzugriffe            |
| 🐳 Docker         | Containerisierung & Setup-Management |

---

## 🧱 Projektstruktur (grober Überblick)

```bash
Cocking-App/
├── app/
│   ├── scripts
│   │   └── wit-for-it.sh
│   ├── db.py
│   ├── Dockerfile
│   ├── ini_db.py
│   ├── main.py
│   ├── models.py
│   ├── requirements.txt
│   ├── templates.txt
│   └── util.py
├── docker-compose.yml
├── LICENSE
└── README.md
```
---
## 1. Klone das Repository
git clone https://github.com/EikAlex/Cocking-App.git

cd Cocking-App

## 2. Starte die Anwendung
docker-compose up --build 

Falls die Datenbank langsamer startet als die Web-App und wait-for-it.sh nicht korrekt greift, kannst du mit Strg + C abbrechen und anschließend neu starten.
Dieses Vorgehen ist nur nötig, wenn wait-for-it.sh Verbindungsprobleme zur Datenbank verursacht.

## 3. Link zur Webapp
http://localhost:8501/

## 4. Neustart und leeren der Datenbank
docker-compose down

docker volume rm cooking-app_pgdata

---
### Erstellt von Alexander Schmal für die Abgabe des Mobile Applikationen Moduls 
