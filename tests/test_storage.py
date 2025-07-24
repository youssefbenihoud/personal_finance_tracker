# tests/test_storage.py
import os
import tempfile
from datetime import date
from pathlib import Path

from finance_tracker.models import Transaction
from finance_tracker.storage import ensure_csv_exists, save_transaction, load_transactions


def test_save_and_load_transaction():
    # Temporäre CSV-Datei für den Test
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        original_file = Path("data/transactions.csv")
        
        # Temporäre CSV verwenden
        global CSV_FILE
        from finance_tracker import storage
        storage.CSV_FILE = tmp_path / "transactions.csv"
        storage.DATA_DIR = tmp_path

        # Sicherstellen, dass CSV existiert
        storage.ensure_csv_exists()

        # Test-Transaktion
        tx = Transaction(
            amount=99.99,
            description="Testkauf",
            date=date(2025, 1, 1),
            category="Test"
        )

        # Speichern
        storage.save_transaction(tx)

        # Laden
        loaded = storage.load_transactions()

        # Prüfen
        assert len(loaded) == 1
        assert loaded[0].amount == 99.99
        assert loaded[0].description == "Testkauf"
        assert loaded[0].date == date(2025, 1, 1)
        assert loaded[0].category == "Test"

    print("✅ test_save_and_load_transaction bestanden!")


# Führe den Test manuell aus (für jetzt)
if __name__ == "__main__":
    test_save_and_load_transaction()