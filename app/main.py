import streamlit as st
from db import SessionLocal, add_zutat_to_vorrat, delete_vorratseintrag, add_rezept, delete_zutat_from_db
import datetime
from models import Vorrat, Zutat, Rezept
from util import check_haltbarkeit, defaul_einheit
from sqlalchemy.orm import joinedload

st.set_page_config(page_title="Koch mit mir!", layout="wide")

st.title("🍽️ Koch mit mir!")
st.markdown(
    "Verwalte deine Rezepte und deinen Vorrat. Lass uns schauen, was du kochen kannst!")

tab1, tab2, tab3 = st.tabs(["📦 Vorrat", "📖 Rezepte", "🧠 Vorschläge"])


# 🔹 UI für Vorratspeicherung
with tab1:
    st.subheader("📥 Vorrat verwalten")

    # Auswahl zwischen Hinzufügen und Löschen
    action = st.radio("Wähle eine Aktion",
                      ("Zutat hinzufügen", "Zutat löschen"))

    db = SessionLocal()

    if action == "Zutat hinzufügen":
        # Zutat hinzufügen
        with st.form("vorrat_form"):
            # Holen von bereits vorhandenen Zutaten aus der DB (diese werden als Vorschläge angezeigt)
            vorhandene_zutaten = db.query(Zutat.name).all()
            zutaten_liste = [z[0]
                             for z in vorhandene_zutaten]  # Extrahieren der Namen

            # Textinput mit Autocomplete
            name = st.selectbox("Zutat", zutaten_liste,
                                index=0, key="autocomplete_zutat")

            # Einheit und Menge
            vorhandene_einheiten = db.query(Zutat.einheit).all()
            einheiten_liste = [z[0]
                             for z in vorhandene_zutaten]
            einheit = st.selectbox("Einheit", defaul_einheit)
            menge = st.number_input("Menge", min_value=1, step=1)
            haltbar_bis = st.date_input(
                "Haltbar bis", value=datetime.date.today())

            submitted = st.form_submit_button("Hinzufügen")
            
    if submitted:
        # Prüfe, ob der gleiche Eintrag schon im Vorrat ist
        existiert_bereits = db.query(Vorrat).join(Zutat).filter(
            Zutat.name == name.strip().capitalize(),
            Vorrat.haltbar_bis == haltbar_bis
        ).first()

        if not existiert_bereits:
            # Zutat ist noch nicht im Vorrat, also neuen Eintrag hinzufügen
            try:
                add_zutat_to_vorrat(
                    db, name.strip().capitalize(), einheit, menge, haltbar_bis)
                st.success(f"✅ {name} wurde zum Vorrat hinzugefügt!")
            except Exception as e:
                st.error(f"❌ Fehler beim Hinzufügen: {e}")
        else:
            # Wenn die Zutat bereits existiert, die Menge aktualisieren
            try:
                # Erhöhe die Menge um den neuen Wert
                existiert_bereits.menge_vorhanden += menge
                db.commit()  # Änderungen speichern
                st.success(f"✅ Menge von {name} wurde im Vorrat aktualisiert!")
            except Exception as e:
                st.error(f"❌ Fehler beim Aktualisieren des Vorrats: {e}")

    elif action == "Zutat löschen":
        # Zutat löschen
        st.subheader("🗑️ Zutat löschen")

        # Zutat zum Löschen auswählen
        zutaten_liste = [z[0] for z in db.query(Zutat.name).all()]
        zutat_to_delete = st.selectbox(
            "Wähle eine Zutat zum Löschen", zutaten_liste)

        if zutat_to_delete:
            if st.button(f"❌ {zutat_to_delete} löschen"):
                if delete_zutat_from_db(db, zutat_to_delete):
                    st.success(f"✅ Zutat '{zutat_to_delete}' wurde gelöscht!")
                else:
                    st.error(
                        f"❌ Fehler: Zutat '{zutat_to_delete}' konnte nicht gelöscht werden.")

    db.close()

    st.divider()

    st.subheader("📦 Dein aktueller Vorrat")

    db = SessionLocal()
    try:
        eintraege = db.query(Vorrat).options(joinedload(Vorrat.zutat)).all()
        if eintraege:
            # Interaktive Liste mit Löschfunktion
            for eintrag in eintraege:
                col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 2, 1])
                col1.write(f"**{eintrag.zutat.name}**")
                col2.write(f"{eintrag.menge_vorhanden}")
                col3.write(eintrag.zutat.einheit)
                haltbarkeit_html = check_haltbarkeit(eintrag.haltbar_bis)
                col4.markdown(haltbarkeit_html, unsafe_allow_html=True)
                if col5.button("🗑️ Löschen", key=f"delete_{eintrag.id}"):
                    delete_vorratseintrag(db, eintrag.id)
                    st.success(f"✅ {eintrag.zutat.name} wurde gelöscht!")
                    st.rerun()
        else:
            st.info("Noch nichts im Vorrat.")
    finally:
        db.close()


# 🔹 UI für Rezepte in main.py
with tab2:
    db = SessionLocal()
    st.subheader("📥 Neues Rezept hinzufügen")

    # Init session state
    if "rezept_phase" not in st.session_state:
        st.session_state.rezept_phase = "start"
    if "rezept_zutaten_liste" not in st.session_state:
        st.session_state.rezept_zutaten_liste = []

    # Schritt 1: Basisdaten
    if st.session_state.rezept_phase == "start":
        with st.form("rezept_start_form"):
            rezeptname = st.text_input("Rezeptname")
            beschreibung = st.text_area("Beschreibung")
            portionen = st.number_input(
                "Anzahl Portionen", min_value=1, value=1, step=1)
            weiter = st.form_submit_button("➡️ Zutaten wählen")

            if weiter and rezeptname and portionen:
                st.session_state.rezeptname = rezeptname
                st.session_state.beschreibung = beschreibung
                st.session_state.portionen = portionen
                st.session_state.rezept_phase = "zutaten"
                st.rerun()

    # Schritt 2: Zutaten nach und nach hinzufügen
    elif st.session_state.rezept_phase == "zutaten":
        st.markdown(
            f"**Rezept:** {st.session_state.rezeptname} für {st.session_state.portionen} Portion(en)")

        zutaten = db.query(Zutat).all()
        zutaten_ids = [z.id for z in zutaten]
        zutaten_namen = [f"{z.name} ({z.einheit})" for z in zutaten]

        with st.form("zutat_hinzufuegen_form"):
            zutat_id = st.selectbox("Zutat auswählen", zutaten_ids,
                                    format_func=lambda x: zutaten_namen[zutaten_ids.index(x)])
            menge = st.number_input(
                "Menge für **1 Portion**", min_value=0.0, step=0.1)
            hinzufuegen = st.form_submit_button("➕ Zutat hinzufügen")

            if hinzufuegen and menge > 0:
                st.session_state.rezept_zutaten_liste.append({
                    "zutat_id": zutat_id,
                    "menge_pro_portion": menge
                })
                st.rerun()

        # Liste anzeigen
        st.subheader("🧾 Zutatenliste")
        if st.session_state.rezept_zutaten_liste:
            for i, eintrag in enumerate(st.session_state.rezept_zutaten_liste):
                z = db.query(Zutat).get(eintrag["zutat_id"])
                gesamtmenge = eintrag["menge_pro_portion"] * \
                    st.session_state.portionen
                col1, col2, col3, col4 = st.columns([4, 2, 3, 1])
                col1.write(z.name)
                col2.write(
                    f"{eintrag['menge_pro_portion']} {z.einheit} pro Portion")
                col3.write(f"{gesamtmenge} {z.einheit} gesamt")
                if col4.button("❌", key=f"del_zutat_{i}"):
                    st.session_state.rezept_zutaten_liste.pop(i)
                    st.rerun()
        else:
            st.info("Noch keine Zutat hinzugefügt.")

        # Rezept speichern
    if st.session_state.rezept_zutaten_liste:
        if st.button("✅ Rezept speichern"):
            # Überprüfen, ob der Rezeptname bereits existiert
            existing_rezept = db.query(Rezept).filter(
                Rezept.name == st.session_state.rezeptname).first()
            if existing_rezept:
                st.error("❌ Ein Rezept mit diesem Namen existiert bereits!")
            else:
                # Rezept speichern, wenn der Name eindeutig ist
                zutaten_liste = [
                    (e["zutat_id"], e["menge_pro_portion"]
                     * st.session_state.portionen)
                    for e in st.session_state.rezept_zutaten_liste
                ]
                add_rezept(
                    db,
                    st.session_state.rezeptname,
                    st.session_state.beschreibung,
                    zutaten_liste
                )
                st.success("🎉 Rezept gespeichert!")

                # Reset
                st.session_state.rezept_phase = "start"
                st.session_state.rezept_zutaten_liste = []
                st.rerun()
    st.divider()

    # Schritt 3: Rezepte anzeigen
    st.subheader("📖 Deine Rezepte")

    rezepte = db.query(Rezept).all()
    # Indizierung hinzufügen, um eindeutigen Key zu erzeugen
    for i, rezept in enumerate(rezepte):
        with st.expander(rezept.name):
            st.markdown(rezept.beschreibung or "_Keine Beschreibung_")
            st.markdown("**Zutaten:**")

            # Der Button-Key wurde jetzt eindeutig gemacht, indem `i` zur ID hinzugefügt wurde
            delete_button = st.button(
                f"🗑️ Löschen {rezept.name}", key=f"delete_{rezept.id}_{i}")
            if delete_button:
                try:
                    db.delete(rezept)  # Rezept aus der DB entfernen
                    db.commit()  # Änderungen speichern
                    st.success(
                        f"✅ Rezept '{rezept.name}' wurde erfolgreich gelöscht!")
                    st.rerun()  # Seite neu laden, um das gelöschte Rezept zu entfernen
                except Exception as e:
                    st.error(f"❌ Fehler beim Löschen des Rezepts: {e}")

            # Zugriff über die `rezept_zutaten` Beziehung
            for rz in rezept.rezept_zutaten:
                z = rz.zutat  # Direkter Zugriff auf Zutat über die Beziehung
                st.write(f"- {rz.menge} {z.einheit} {z.name}")


# 🔹 UI für Vorschläge in main.py

with tab3:
    db = SessionLocal()
    st.subheader("🧠 Rezeptvorschläge basierend auf deinem Vorrat")

    vorrat = db.query(Vorrat).all()
    vorrats_map = {v.zutat_id: v.menge_vorhanden for v in vorrat}

    rezepte = db.query(Rezept).all()
    for rezept in rezepte:
        portionen_moeglich = float("inf")
        fehlende_zutaten = []

        for rz in rezept.rezept_zutaten:
            benoetigte_menge = rz.menge
            vorhandene_menge = vorrats_map.get(rz.zutat_id, 0)

            if vorhandene_menge <= 0:
                portionen_moeglich = 0
                fehlende_zutaten.append(
                    (rz.zutat.name, benoetigte_menge, rz.zutat.einheit))
            else:
                moegliche_portionen = vorhandene_menge / benoetigte_menge
                portionen_moeglich = min(
                    portionen_moeglich, moegliche_portionen)

                if vorhandene_menge < benoetigte_menge:
                    fehlende_zutaten.append(
                        (rz.zutat.name, benoetigte_menge - vorhandene_menge, rz.zutat.einheit))

        with st.expander(rezept.name):
            st.markdown(rezept.beschreibung or "_Keine Beschreibung_")

            if portionen_moeglich >= 1:
                st.success(
                    f"✅ Du kannst ca. {int(portionen_moeglich)} Portion(en) kochen")
            else:
                st.warning("⚠️ Du hast nicht genug Vorrat für eine Portion.")
                if fehlende_zutaten:
                    st.markdown("**Fehlende Zutaten:**")
                    for name, diff, einheit in fehlende_zutaten:
                        st.write(f"- {diff:.2f} {einheit} {name}")

            st.markdown("**Zutatenübersicht:**")
            for rz in rezept.rezept_zutaten:
                st.write(f"- {rz.menge} {rz.zutat.einheit} {rz.zutat.name}")
