# 💰 Personal Finance Tracker

Ein CLI-basierter Finanz-Tracker, um Einnahmen und Ausgaben einfach zu verwalten – **ohne externe Abhängigkeiten**.  
Daten werden in einer CSV-Datei gespeichert: einfach, portabel und robust.

✨ **Hauptfunktionen**:
- Transaktionen hinzufügen (Betrag, Beschreibung, Kategorie, Datum)
- Alle Einträge anzeigen oder nach Kategorie/Betrag filtern
- Statistiken anzeigen: Gesamtbilanz, Einnahmen, Ausgaben, Top-Kategorien
- Automatische CSV-Verwaltung mit Header-Sicherung
- Robust gegen fehlende oder fehlerhafte Dateien

---

## 🚀 Schnellstart: So nutzt du das Projekt

Da dieses Projekt ein eigenes Python-Paket (`finance_tracker`) verwendet, musst du den **Python-Modulpfad korrekt setzen**, um den Fehler `ModuleNotFoundError` zu vermeiden.

### 🔧 Ausführen (empfohlene Methode):

```bash
# 1. In das Projektverzeichnis wechseln
cd personal_finance_tracker

# 2. PYTHONPATH setzen und Befehle ausführen
PYTHONPATH=. python scripts/main.py add --amount 100 --description "Gehalt" --category "Lohn" --date 2025-04-01
PYTHONPATH=. python scripts/main.py add --amount -20 --description "Kino" --category "Freizeit" --date 2025-04-05
PYTHONPATH=. python scripts/main.py list
PYTHONPATH=. python scripts/main.py list --category "Freizeit"
PYTHONPATH=. python scripts/main.py stats
```

### ✅ Warum PYTHONPATH=.?

Dieser Befehl sagt Python: „Suche Module auch im aktuellen Ordner“.
So kann from finance_tracker.cli import main_cli gefunden werden.
➡️ Dies ist eine gängige und professionelle Praxis bei strukturierten Python-Projekten.

### add - neue Transkation hinzufügen
```bash
python scripts/main.py add --amount <Betrag> --description "<Text>" [--category "<Kategorie>"] [--date JJJJ-MM-TT]
```

#### Beispiel
```bash
PYTHONPATH=. python scripts/main.py add --amount 50 --description "Kaffee" --category "Essen" --date 2025-04-05
```

### list - Alle Transaktionen anzeigen

```bash
PYTHONPATH=. python scripts/main.py list
```

### Mit Filtern

```bash
PYTHONPATH=. python scripts/main.py list --category "Essen"
PYTHONPATH=. python scripts/main.py list --min-amount 10
PYTHONPATH=. python scripts/main.py list --max-amount -5
```

### stats - Finanzstatistics zeigen
```bash
PYTHONPATH=. python scripts/main.py stats
```

### Ausgabe 
```bash
📊 Statistiken:
Gesamtbilanz: +80.00 €
Einnahmen: +100.00 €
Ausgaben: -20.00 €

Top Kategorie (Ausgaben): Freizeit (-20.00 €)
````

## 📂 Projektstruktur
```bash
personal_finance_tracker/
├── finance_tracker/
│   ├── __init__.py
│   ├── models.py       # Transaction-Klasse (dataclass)
│   ├── storage.py      # CSV-Lesen/Schreiben mit automatischer Header-Korrektur
│   └── cli.py          # Befehlsverarbeitung mit argparse
├── scripts/
│   └── main.py         # Einstiegspunkt
├── data/
│   └── transactions.csv # Wird automatisch erstellt
├── tests/
│   └── test_storage.py # Einfacher Integrationstest
├── README.md
├── requirements.txt    # (leer – kein externes Paket nötig)
└── .gitignore
```