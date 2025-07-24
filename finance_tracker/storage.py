# finance_tracker/storage.py
import csv
from datetime import date, datetime
from pathlib import Path
from typing import List

from models import Transaction


# Pfad zur CSV-Datei
DATA_DIR = Path("data")
CSV_FILE = DATA_DIR / "transactions.csv"

# Header für die CSV
CSV_HEADER = ["amount", "description", "date", "category"]


def ensure_csv_exists() -> None:
    """Stellt sicher, dass die CSV-Datei mit Header existiert."""
    DATA_DIR.mkdir(exist_ok=True)
    if not CSV_FILE.exists():
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADER)


def save_transaction(transaction: Transaction) -> None:
    """Speichert eine einzelne Transaktion in der CSV-Datei."""
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            transaction.amount,
            transaction.description,
            transaction.date.isoformat(),
            transaction.category or ""
        ])


def load_transactions() -> List[Transaction]:
    """Lädt alle Transaktionen aus der CSV-Datei."""
    transactions = []
    if not CSV_FILE.exists():
        return transactions

    with open(CSV_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                transactions.append(
                    Transaction(
                        amount=float(row["amount"]),
                        description=row["description"],
                        date=datetime.strptime(row["date"], "%Y-%m-%d").date(),
                        category=row["category"] or None
                    )
                )
            except (ValueError, KeyError) as e:
                print(f"⚠️  Ungültige Zeile in CSV übersprungen: {row} | Fehler: {e}")
    return transactions

## Testen

# Test in Python-Shell oder temporär in storage.py unter if __name__ == "__main__":
if __name__ == "__main__":
    from datetime import date
    from models import Transaction

    # 1. Stelle sicher, dass CSV existiert
    ensure_csv_exists()

    # 2. Speichere eine Test-Transaktion
    tx = Transaction(50.0, "Kaffee", date.today(), "Essen")
    save_transaction(tx)
    print("✅ Transaktion gespeichert!")

    # 3. Lade alle Transaktionen
    loaded = load_transactions()
    print(" Geladene Transaktionen:", loaded)