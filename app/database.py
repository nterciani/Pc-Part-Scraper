"""
Handles all database-related operations for the PC parts web scraping tool.

This module establishes a connection to a SQLite database and defines functions
to create and populate tables for storing product and pricing information.
"""

import sqlite3
from typing import Optional
from app.models.cpu import CPU


def get_connection(db_name: str) -> sqlite3.Connection:
    """Return a connection to database <db_name>.
    """
    try:
        return sqlite3.connect(db_name)
    except Exception as e:
        print(f"Error: {e}")


# === CPU table functions ===
def create_cpus_table(connection: sqlite3.Connection) -> None:
    """Create a 'cpus' table in <connection> if it doesn't already exit. 
    The table stores CPU IDs and names (aswell as specs in the future).
    """
    query = """
    CREATE TABLE IF NOT EXISTS cpus (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
    """
    try:
        with connection:
            connection.execute(query)
        print("CPUs table was created.") # debug
    except Exception as e:
        print(f"Error: {e}")


def get_cpu_id(connection: sqlite3.Connection, name: str) -> Optional[int]:
    """Return the id of the cpu with name <name>, or None if not found.
    """
    query = "SELECT id FROM cpus WHERE name=?"
    try:
        with connection:
            result = connection.execute(query, (name,)).fetchone()
            return result[0] if result else None
    except Exception as e:
        print(f"Error: {e}")
        return None


def create_cpu_prices_table(connection: sqlite3.Connection) -> None:
    """Create a 'cpu_prices' table in <connection> that stores pricing 
    information for CPUs.
    """
    query = """
    CREATE TABLE IF NOT EXISTS cpu_prices (
        id INTEGER PRIMARY KEY,
        cpu_id INTEGER,
        website TEXT,
        price TEXT,
        link TEXT,
        price_date TEXT,
        FOREIGN KEY (cpu_id) REFERENCES cpus(id)
    )
    """
    try:
        with connection:
            connection.execute(query)
        print("CPU prices table was created.") # debug
    except Exception as e:
        print(f"Error: {e}")


def insert_all_cpus(connection: sqlite3.Connection, cpus: list[CPU]) -> None:
    """Insert all CPUs in <cpus> into <connection>."""
    for cpu in cpus:
        _insert_cpu(connection, cpu)
        

# === Helper function for insert_all_cpus ===
def _insert_cpu(connection: sqlite3.Connection, cpu: CPU) -> None:
    """Insert <cpu> into <connection>.

    - Adds <cpu> into the 'cpus' table if not already present.
    - Adds the pricing information into the 'cpu_prices' table.
    """
    if not get_cpu_id(connection, cpu.name):
        query = "INSERT INTO cpus (name) VALUES (?)"
        try:
            with connection:
                connection.execute(query, (cpu.name,))
                print(f"CPU: {cpu.name} was added to the cpus table.") # debug
        except Exception as e:
            print(f"Error: {e}")

    query2 = """
    INSERT INTO cpu_prices (cpu_id, website, price, link, price_date)
    VALUES (?, ?, ?, ?, ?)
    """
    cpu_id = get_cpu_id(connection, cpu.name)
    try:
        with connection:
            connection.execute(query2, (cpu_id, cpu.website, cpu.price, cpu.link, cpu.date))
            print(f"CPU: {cpu.name} was added to the cpu_price table with price {cpu.price} \
                  from website {cpu.website}.") # debug
    except Exception as e:
            print(f"Error: {e}")
