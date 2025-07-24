# web_app.py
import streamlit as st
import pandas as pd
from datetime import date
from pathlib import Path

# Pfad zum Hauptmodul hinzufügen
import sys
sys.path.append(str(Path(__file__).parent))

from finance_tracker.models import Transaction
from finance_tracker.storage import ensure_csv_exists, load_transactions, save_transaction


def main():
    st.set_page_config(page_title="💰 Finance Tracker", layout="wide")
    st.title("Personal Finance Tracker")

    # Sicherstellen, dass CSV existiert
    ensure_csv_exists()

    # Laden der Transaktionen
    transactions = load_transactions()
    df = pd.DataFrame([{
        "Betrag": t.amount,
        "Beschreibung": t.description,
        "Kategorie": t.category or "Unkategorisiert",
        "Datum": t.date
    } for t in transactions])

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📋 Übersicht", "➕ Hinzufügen", "📊 Statistiken"])

    with tab1:
        st.subheader("Alle Transaktionen")
        if not df.empty:
            st.dataframe(df.sort_values("Datum", ascending=False), use_container_width=True)
        else:
            st.info("Noch keine Transaktionen erfasst.")

    with tab2:
        st.subheader("Neue Transaktion hinzufügen")
        with st.form("add_transaction"):
            col1, col2 = st.columns(2)
            with col1:
                amount = st.number_input("Betrag (€)", value=0.0, format="%.2f")
            with col2:
                desc = st.text_input("Beschreibung")
            cat = st.text_input("Kategorie (optional)", value="Allgemein")
            trans_date = st.date_input("Datum", value=date.today())
            submitted = st.form_submit_button("Hinzufügen")

            if submitted and desc and amount != 0:
                tx = Transaction(
                    amount=amount,
                    description=desc,
                    date=trans_date,
                    category=cat if cat else None
                )
                save_transaction(tx)
                st.success(f"✅ '{desc}' ({amount:+.2f} €) hinzugefügt!")
                st.balloons()
                # Seite neu laden, um Tabelle zu aktualisieren
                st.rerun()
            elif submitted:
                st.warning("Bitte Beschreibung und Betrag eingeben.")

    with tab3:
        st.subheader("Statistiken")
        if df.empty:
            st.info("Keine Daten für Statistiken verfügbar.")
        else:
            col1, col2, col3 = st.columns(3)
            col1.metric("Gesamtbilanz", f"{df['Betrag'].sum():+.2f} €")
            col2.metric("Einnahmen", f"{df[df['Betrag'] > 0]['Betrag'].sum():+.2f} €")
            col3.metric("Ausgaben", f"{df[df['Betrag'] < 0]['Betrag'].sum():+.2f} €")

            # Top Kategorien (Ausgaben)
            expenses = df[df["Betrag"] < 0]
            if not expenses.empty:
                top_cat = expenses.groupby("Kategorie")["Betrag"].sum().round(2).sort_values().head(5)
                st.bar_chart(top_cat)
            # Kuchendiagramm für Ausgaben nach Kategorie
            st.subheader("Ausgaben nach Kategorie")
            expense_by_cat = expenses.groupby("Kategorie")["Betrag"].sum().abs()  # positiv für Diagramm
            if not expense_by_cat.empty:
                st.write("Verteilung der Ausgaben:")
                st.pyplot(expense_by_cat.plot.pie(autopct="%.1f%%").get_figure())
            else:
                st.info("Keine Ausgaben zum Anzeigen.")


if __name__ == "__main__":
    main()