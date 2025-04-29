"""Hopefully a cool webscraping tool.

Currently scrapes CPU listings from Newegg and stores the data in an SQLite database.
Intended for testing the scraping and database pipeline. Future iterations may 
expand to include additional part categories, websites, and application features.
"""

import os
import app.scraper as scraper
import app.database as database


def cpu_table_main() -> None:
    """Current temporary setup of the GPU tables and information."""
    # Scrape CPU data
    cpus = scraper.scrape_newegg_cpus()

    # Connect to the database
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "parts.db")
    connection = database.get_connection(db_path)

    # === DEVELOPMENT ONLY: Reset the tables for clean testing ===
    # connection.execute("DROP TABLE IF EXISTS cpus")
    # connection.execute("DROP TABLE IF EXISTS cpu_prices")

    # Create fresh tables
    database.create_cpus_table(connection)
    database.create_part_prices_table(connection, 'cpu')

    # Insert scraped CPUs
    database.insert_all_cpus(connection, cpus)


def gpu_table_main() -> None:
    """Current temporary setup of the GPU tables and information."""
    # Scrape GPU data
    gpus = scraper.scrape_newegg_gpus()

    # Connect to the database
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "parts.db")
    connection = database.get_connection(db_path)

    # === DEVELOPMENT ONLY: Reset the tables for clean testing ===
    connection.execute("DROP TABLE IF EXISTS gpus")
    connection.execute("DROP TABLE IF EXISTS gpu_prices")

    # Create fresh tables
    database.create_gpus_table(connection)
    database.create_part_prices_table(connection, 'gpu')

    # Insert scraped GPUs
    database.insert_all_gpus(connection, gpus)


if __name__ == "__main__":
    cpu_table_main()
