"""
Handles all database-related operations for the PC parts web scraping tool.

This module establishes a connection to a SQLite database and defines functions
to create and populate tables for storing product and pricing information.
"""

import sqlite3
from typing import Optional
from app.models.pc_part import PcPart
from app.models.cpu import CPU
from app.models.gpu import GPU


# === Universal table functions ===
def get_connection(db_name: str) -> sqlite3.Connection:
    """Return a connection to database <db_name>.
    """
    try:
        return sqlite3.connect(db_name)
    except Exception as e:
        print(f"Error: {e}")


def get_part_id(connection: sqlite3.Connection, part: PcPart) -> Optional[int]:
    """Return the id of <part>, or None if not found."""
    query = f"SELECT id FROM {type(part).__name__.lower()}s WHERE name=?"
    try:
        with connection:
            result = connection.execute(query, (part.name,)).fetchone()
            return result[0] if result else None
    except Exception as e:
        print(f"Error: {e}")
        return None
    

def create_part_prices_table(connection: sqlite3.Connection, part_type: str) -> None:
    """Create a '<part_type>_prices' table in <connection> that stores pricing 
    information for the given <part_type>.
    """
    table_name = f"{part_type}_prices"
    foreign_key = f"{part_type}_id"

    query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY,
        {foreign_key} INTEGER,
        website TEXT,
        price TEXT,
        link TEXT,
        price_date TEXT,
        FOREIGN KEY ({foreign_key}) REFERENCES {part_type}s(id)
    )
    """
    try:
        with connection:
            connection.execute(query)
        print(f"{part_type}_prices table was created.") # debug
    except Exception as e:
        print(f"Error: {e}")


def insert_part_price(connection: sqlite3.Connection, part: PcPart) -> None:
    """Insert <part>'s pricing information into the '<part>_prices' table within
    <connection>."""
    part_type = type(part).__name__.lower()

    query = f"""
    INSERT INTO {part_type}_prices ({part_type}_id, website, price, link, price_date)
    VALUES (?, ?, ?, ?, ?)
    """
    part_id = get_part_id(connection, part)
    try:
        with connection:
            connection.execute(query, (part_id, part.website, part.price, part.link, part.date))
            print(f"{part_type}: {part.name} was added to the {part_type}_prices table with price {part.price}") # debug
    except Exception as e:
            print(f"Error: {e}")


# === CPU table functions ===
def create_cpus_table(connection: sqlite3.Connection) -> None:
    """Create a 'cpus' table in <connection> if it doesn't already exit. 
    The table stores CPU IDs, names, and brands (as well as specs in the future).
    """
    query = """
    CREATE TABLE IF NOT EXISTS cpus (
        id INTEGER PRIMARY KEY,
        brand TEXT,
        name TEXT
    )
    """
    try:
        with connection:
            connection.execute(query)
        print("CPUs table was created.") # debug
    except Exception as e:
        print(f"Error: {e}")


def insert_all_cpus(connection: sqlite3.Connection, cpus: list[CPU]) -> None:
    """Insert all CPUs in <cpus> into <connection>."""
    for cpu in cpus:
        insert_cpu(connection, cpu)
        

def insert_cpu(connection: sqlite3.Connection, cpu: CPU) -> None:
    """Insert <cpu> into <connection>.

    - Adds <cpu> into the 'cpus' table if not already present.
    - Adds the pricing information into the 'cpu_prices' table.
    """
    # unique portion
    if not get_part_id(connection, cpu):
        query = "INSERT INTO cpus (brand, name) VALUES (?, ?)"
        try:
            with connection:
                connection.execute(query, (cpu.brand, cpu.name))
                print(f"CPU: {cpu.name} was added to the cpus table.") # debug
        except Exception as e:
            print(f"Error: {e}")

    # non-unique portion
    insert_part_price(connection, cpu)


# === GPU table functions ===
def create_gpus_table(connection: sqlite3.Connection) -> None:
    """Create a 'gpus' table in <connection> if it doesn't already exit. 
    The table stores GPU IDs, names, and brands (as well as specs in the future).
    """
    query = """
    CREATE TABLE IF NOT EXISTS gpus (
        id INTEGER PRIMARY KEY,
        brand TEXT,
        name TEXT
    )
    """
    try:
        with connection:
            connection.execute(query)
        print("GPUs table was created.") # debug
    except Exception as e:
        print(f"Error: {e}")


def insert_all_gpus(connection: sqlite3.Connection, gpus: list[GPU]) -> None:
    """Insert all GPUs in <gpus> into <connection>."""
    for gpu in gpus:
        insert_gpu(connection, gpu)


def insert_gpu(connection: sqlite3.Connection, gpu: GPU) -> None:
    """Insert <gpu> into <connection>.

    - Adds <gpu> into the 'gpus' table if not already present.
    - Adds the pricing information into the 'gpu_prices' table.
    """
    # unique portion
    if not get_part_id(connection, gpu):
        query = "INSERT INTO gpus (brand, name) VALUES (?, ?)"
        try:
            with connection:
                connection.execute(query, (gpu.brand, gpu.name))
                print(f"GPU: {gpu.name} was added to the gpus table.") # debug
        except Exception as e:
            print(f"Error: {e}")

    # non-unique portion
    insert_part_price(connection, gpu)
