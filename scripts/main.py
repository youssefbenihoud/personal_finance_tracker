# scripts/main.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from finance_tracker.cli import main_cli


if __name__ == "__main__":
    main_cli()