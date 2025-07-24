# finance_tracker/models.py
from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Transaction:
    """
    Repräsentiert eine finanzielle Transaktion (Einnahme oder Ausgabe).

    Attribute:
        amount (float): Betrag (positiv für Einnahmen, negativ für Ausgaben)
        description (str): Beschreibung der Transaktion (z. B. "Gehalt" oder "Miete")
        date (date): Datum der Transaktion
        category (Optional[str]): Kategorie (z. B. "Essen", "Lohn", "Miete")
    """
    amount: float
    description: str
    date: date
    category: Optional[str] = None

    def __post_init__(self):
        """Validiert den Betrag nach der Instanziierung."""
        if not isinstance(self.amount, (int, float)):
            raise ValueError("Amount must be a number.")
        if self.amount == 0:
            raise ValueError("Amount cannot be zero.")