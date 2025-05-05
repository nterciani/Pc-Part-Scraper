"""
Entry point for the PC Part Scraper application.

Provides a command-line interface for running either the interactive
terminal UI or the database updater. Currently supports scraping
CPU, GPU, and motherboard listings from Newegg and storing them
in a local SQLite database.

Future versions may expand to additional part types, websites, 
and application features such as filtering, comparison, and price tracking.
"""

import argparse
from app.cli import interactive, updater


def main():
    parser = argparse.ArgumentParser(description="PC Part Scraper CLI")
    parser.add_argument("--interactive", action="store_true", help="Run interactive terminal app")
    parser.add_argument("--update", action="store_true", help="Update the local database")

    args = parser.parse_args()

    if args.interactive:
        interactive.run_ui()
    elif args.update:
        updater.update_database()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
