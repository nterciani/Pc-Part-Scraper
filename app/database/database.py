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
from app.models.motherboard import MOBO


# === Universal database functions ===
def get_connection(db_name: str) -> sqlite3.Connection:
    """Return a connection to database <db_name>."""
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
    except Exception as e:
            print(f"Error: {e}")


def ensure_tables(connection: sqlite3.Connection) -> bool:
    """Ensure all necessary tables exist before interactions."""
    tables_list = ["cpus", "cpu_prices", "gpus", "gpu_prices", "mobos", "mobo_prices"]

    query = "SELECT name FROM sqlite_master WHERE type='table'AND name=?"

    for table in tables_list:
        try:
            with connection:
                exists = connection.execute(query, (table,)).fetchone()
                if not exists:
                    print(f"No data found for {table}. Please run with --update first to populate data.")
                    return False
        except Exception as e:
            print(f"Error: {e}")

    return True


# === CPU table functions ===
def create_cpus_table(connection: sqlite3.Connection) -> None:
    """Create a 'cpus' table in <connection> if it doesn't already exist. 
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
    if not get_part_id(connection, cpu):
        query = "INSERT INTO cpus (brand, name) VALUES (?, ?)"
        try:
            with connection:
                connection.execute(query, (cpu.brand, cpu.name))
        except Exception as e:
            print(f"Error: {e}")

    insert_part_price(connection, cpu)


def fetch_cpus(connection: sqlite3.Connection, name_condition: str=None) -> list[CPU]:
    """Return a list of CPU objects reconstructed from the cpus and cpu_prices tables. The returned CPU 
    objects can be filtered through <name_condition> (and more in the future).
    """
    query = """
    SELECT cpus.name, cpus.brand, cpu_prices.website, cpu_prices.link, cpu_prices.price, cpu_prices.price_date
    FROM cpus
    JOIN cpu_prices ON cpus.id = cpu_prices.cpu_id
    """
    params = ()

    if name_condition:
        query += " WHERE cpus.name LIKE ?"
        params = (f"%{name_condition}%",)

    try:
        with connection:
            rows = connection.execute(query, params).fetchall()
        return [CPU(name=row[0], brand=row[1], website=row[2], link=row[3], price=row[4], date=row[5]) for row in rows]
    except Exception as e:
        print(f"Error: {e}")
        return []


# === GPU table functions ===
def create_gpus_table(connection: sqlite3.Connection) -> None:
    """Create a 'gpus' table in <connection> if it doesn't already exist. 
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
    if not get_part_id(connection, gpu):
        query = "INSERT INTO gpus (brand, name) VALUES (?, ?)"
        try:
            with connection:
                connection.execute(query, (gpu.brand, gpu.name))
        except Exception as e:
            print(f"Error: {e}")

    insert_part_price(connection, gpu)


def fetch_gpus(connection: sqlite3.Connection, name_condition: str=None) -> list[CPU]:
    """Return a list of GPU objects reconstructed from the gpus and gpu_prices tables. The returned GPU 
    objects can be filtered through <name_condition> (and more in the future).
    """
    query = """
    SELECT gpus.name, gpus.brand, gpu_prices.website, gpu_prices.link, gpu_prices.price, gpu_prices.price_date
    FROM gpus
    JOIN gpu_prices ON gpus.id = gpu_prices.gpu_id
    """
    params = ()

    if name_condition:
        query += " WHERE gpus.name LIKE ?"
        params = (f"%{name_condition}%",)

    try:
        with connection:
            rows = connection.execute(query, params).fetchall()
        return [GPU(name=row[0], brand=row[1], website=row[2], link=row[3], price=row[4], date=row[5]) for row in rows]
    except Exception as e:
        print(f"Error: {e}")
        return []


# === motherboard table functions ===
def create_mobos_table(connection: sqlite3.Connection) -> None:
    """Create a 'mobos' table in <connection> if it doesn't already exist. 
    The table stores motherboard IDs, names, and brands (as well as specs in the future).
    """
    query = """
    CREATE TABLE IF NOT EXISTS mobos (
        id INTEGER PRIMARY KEY,
        brand TEXT,
        name TEXT
    )
    """
    try:
        with connection:
            connection.execute(query)
    except Exception as e:
        print(f"Error: {e}")


def insert_all_mobos(connection: sqlite3.Connection, mobos: list[MOBO]) -> None:
    """Insert all motherboards in <mobos> into <connection>."""
    for mobo in mobos:
        insert_mobo(connection, mobo)


def insert_mobo(connection: sqlite3.Connection, mobo: MOBO) -> None:
    """Insert <mobo> into <connection>.

    - Adds <mobo> into the 'mobos' table if not already present.
    - Adds the pricing information into the 'mobo_prices' table.
    """
    if not get_part_id(connection, mobo):
        query = "INSERT INTO mobos (brand, name) VALUES (?, ?)"
        try:
            with connection:
                connection.execute(query, (mobo.brand, mobo.name))
        except Exception as e:
            print(f"Error: {e}")

    insert_part_price(connection, mobo)


def fetch_mobos(connection: sqlite3.Connection, name_condition: str=None) -> list[CPU]:
    """Return a list of MOBO objects reconstructed from the mobos and mobo_prices tables. The returned MOBO 
    objects can be filtered through <name_condition> (and more in the future).
    """
    query = """
    SELECT mobos.name, mobos.brand, mobo_prices.website, mobo_prices.link, mobo_prices.price, mobo_prices.price_date
    FROM mobos
    JOIN mobo_prices ON mobos.id = mobo_prices.mobo_id
    """
    params = ()

    if name_condition:
        query += " WHERE mobos.name LIKE ?"
        params = (f"%{name_condition}%",)

    try:
        with connection:
            rows = connection.execute(query, params).fetchall()
        return [MOBO(name=row[0], brand=row[1], website=row[2], link=row[3], price=row[4], date=row[5]) for row in rows]
    except Exception as e:
        print(f"Error: {e}")
        return []
