# 🥘 Digitale Kochbuch-App mit Vorratsverwaltung

Willkommen zur digitalen Kochbuch-App mit integrierter Vorratsverwaltung!  
Diese Anwendung wurde mit **Python** und **Streamlit** erstellt und bietet eine einfache und moderne Benutzeroberfläche für das Verwalten von Rezepten und Vorräten.  
Die Daten werden in einer **PostgreSQL-Datenbank** gespeichert und mithilfe von **SQLAlchemy** und **Docker** verwaltet.

---

## 🚀 Features

- 🧺 Vorratsverwaltung: Behalte den Überblick über Zutaten, Bestände & Verfallsdatum
- 📖 Rezeptverwaltung: Hinzufügen, Bearbeiten und Anzeigen von Rezepten
- 🔄 Integration: Verknüpfung von Rezepten mit Vorratsdaten
<!-- - 🔍 Such- und Filterfunktion für einfache Bedienung -->
- 🐳 Containerisiert mit Docker für einfache Bereitstellung

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
coocking-app/
├── app/
│   ├── db.py
│   ├── Dockerfile
│   ├── ini_db.py
│   ├── main.py
│   ├── models.py
│   ├── requirements.txt
│   └── templates.py
├── docker-compose.yml
├── LICENSE
└── README.md
```

# 1. Klone das Repository
git clone https://github.com/dein-user/koch-app.git

cd koch-app

# 2. Starte die Anwendung
docker-compose up --build

# 3. Neustart und leeren der Datenbank
docker-compose down

docker volume rm cooking-app_pgdata
### Erstellt von Alexander Schmal für die Abgabe des Mobile Applikationen Moduls 