"""
Handles the scraping of PC part listings from Newegg and populates the local
SQLite database with the retrieved data. This includes creating tables (if needed)
and inserting both part specifications and pricing data.

Intended to be run manually or on a schedule to keep the database current.
"""

import os
import app.scraper.scraper as scraper
import app.database.database as database
from app.config import DB_PATH


def update_database() -> None:
    """Scrapes all CPUs, GPUs, and motherboards from Newegg and inserts them into the 
    local database given by <DB_PATH>.
    """
    connection = database.get_connection(DB_PATH)

    # create/reload all tables
    database.create_cpus_table(connection)
    database.create_part_prices_table(connection, 'cpu')

    database.create_gpus_table(connection)
    database.create_part_prices_table(connection, 'gpu')

    database.create_mobos_table(connection)
    database.create_part_prices_table(connection, 'mobo')

    # scrape data
    cpus = scraper.scrape_newegg_cpus()
    gpus = scraper.scrape_newegg_gpus()
    mobos = scraper.scrape_newegg_mobos()

    database.insert_all_cpus(connection, cpus)
    database.insert_all_gpus(connection, gpus)
    database.insert_all_mobos(connection, mobos)
