# finance_tracker/cli.py
import argparse
from datetime import date
from typing import List

from finance_tracker.models import Transaction
from finance_tracker.storage import load_transactions, save_transaction


def create_parser() -> argparse.ArgumentParser:
    """Erstellt und konfiguriert den Argument-Parser."""
    parser = argparse.ArgumentParser(description="💰 Personal Finance Tracker")
    subparsers = parser.add_subparsers(dest="command", help="Verfügbare Befehle")

    # Befehl: add
    parser_add = subparsers.add_parser("add", help="Neue Transaktion hinzufügen")
    parser_add.add_argument("--amount", type=float, required=True, help="Betrag (positiv für Einnahmen, negativ für Ausgaben)")
    parser_add.add_argument("--description", type=str, required=True, help="Beschreibung der Transaktion")
    parser_add.add_argument("--category", type=str, default=None, help="Kategorie (optional)")
    parser_add.add_argument("--date", type=str, default=str(date.today()), help="Datum im Format JJJJ-MM-TT (Standard: heute)")

    # Show Finanz-Statistiken
    parser_stats = subparsers.add_parser("stats", help="Zeige Finanz-Statistiken")
    # Befehl: list
    parser_list = subparsers.add_parser("list", help="Alle Transaktionen anzeigen")
    parser_list.add_argument("--category", type=str, help="Filtere nach Kategorie")
    parser_list.add_argument("--min-amount", type=float, help="Filtere nach minimalem Betrag")
    parser_list.add_argument("--max-amount", type=float, help="Filtere nach maximalem Betrag")

    return parser


def handle_add(args) -> None:
    """Verarbeitet den 'add'-Befehl."""
    try:
        transaction_date = date.fromisoformat(args.date)
    except ValueError:
        print(f"❌ Ungültiges Datumsformat: {args.date}. Bitte JJJJ-MM-TT verwenden.")
        return

    transaction = Transaction(
        amount=args.amount,
        description=args.description,
        date=transaction_date,
        category=args.category
    )
    save_transaction(transaction)
    print(f"✅ Transaktion hinzugefügt: {transaction}")


def handle_list(args) -> None:
    """Verarbeitet den 'list'-Befehl."""
    transactions: List[Transaction] = load_transactions()

    # Filter anwenden
    if args.category:
        transactions = [t for t in transactions if t.category == args.category]
    if args.min_amount is not None:
        transactions = [t for t in transactions if t.amount >= args.min_amount]
    if args.max_amount is not None:
        transactions = [t for t in transactions if t.amount <= args.max_amount]

    if not transactions:
        print("📋 Keine Transaktionen gefunden.")
        return

    print(f"📋 {len(transactions)} Transaktion(en):")
    for t in transactions:
        cat = t.category or "keine Kategorie"
        print(f"  {t.date} | {t.amount:+6.2f} € | {t.description} | [{cat}]")

def handle_stats(args) -> None:
    """Verarbeitet den 'stats'-Befehl und zeigt Statistiken an."""
    transactions = load_transactions()

    if not transactions:
        print("📋 Keine Transaktionen zum Analysieren.")
        return

    total = sum(t.amount for t in transactions)
    incomes = sum(t.amount for t in transactions if t.amount > 0)
    expenses = sum(t.amount for t in transactions if t.amount < 0)

    print("📊 Statistiken:")
    print(f"Gesamtbilanz: {total:+.2f} €")
    print(f"Einnahmen: {incomes:+.2f} €")
    print(f"Ausgaben: {expenses:+.2f} €")

    # Top-Ausgaben-Kategorie
    expense_by_category = {}
    for t in transactions:
        if t.amount < 0:
            cat = t.category or "keine Kategorie"
            expense_by_category[cat] = expense_by_category.get(cat, 0) + t.amount

    if expense_by_category:
        top_category = min(expense_by_category, key=expense_by_category.get)
        print(f"\nTop Kategorie (Ausgaben): {top_category} ({expense_by_category[top_category]:.2f} €)")

def main_cli() -> None:
    """Hauptfunktion für die CLI."""
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "add":
        handle_add(args)
    elif args.command == "list":
        handle_list(args)
    elif args.command == "stats":
        handle_stats(args)
    else:
        parser.print_help()