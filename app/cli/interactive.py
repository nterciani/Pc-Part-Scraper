"""
Provides an interactive command-line interface (CLI) for browsing and querying
PC part listings stored in the local SQLite database. Users can view or search
for CPUs, GPUs, and motherboards based on stored data.

This module is designed for user-facing terminal interaction.
"""

import os
import app.database.database as database
from app.config import DB_PATH


def run_ui() -> None:
    """User interaction with the database."""
    connection = database.get_connection(DB_PATH)

    if not database.ensure_tables(connection):
        return

    print("\n==== PC Part Tracker ====")
    while True:
        print("1. View CPUs")
        print("2. View GPUs")
        print("3. View Motherboards")
        print("4. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            while True:
                print("1. Display all CPUs")
                print("2. Search for a CPU by name")
                print("3. Back")
                choice = input("Enter choice: ")

                if choice == "1":
                    cpus = database.fetch_cpus(connection)
                    for cpu in cpus:
                        print(cpu)
                elif choice == "2":
                    name = input("Enter CPU name: ").strip()
                    cpus = database.fetch_cpus(connection, name)
                    for cpu in cpus:
                        print(cpu)
                elif choice == "3":
                    break
                else:
                    print("Invalid option.")
        elif choice == "2":
            while True:
                print("1. Display all GPUs")
                print("2. Search for a GPU by name")
                print("3. Back")
                choice = input("Enter choice: ")

                if choice == "1":
                    gpus = database.fetch_gpus(connection)
                    for gpu in gpus:
                        print(gpu)
                elif choice == "2":
                    name = input("Enter GPU name: ").strip()
                    gpus = database.fetch_gpus(connection, name)
                    for gpu in gpus:
                        print(gpu)
                elif choice == "3":
                    break
                else:
                    print("Invalid option.")
        elif choice == "3":
            while True:
                print("1. Display all motherboards")
                print("2. Search for a motherboard by name")
                print("3. Back")
                choice = input("Enter choice: ")

                if choice == "1":
                    mobos = database.fetch_mobos(connection)
                    for mobo in mobos:
                        print(mobo)
                elif choice == "2":
                    name = input("Enter motherboard name: ").strip()
                    mobos = database.fetch_mobos(connection, name)
                    for mobo in mobos:
                        print(mobo)
                elif choice == "3":
                    break
                else:
                    print("Invalid option.")
        elif choice == "4":
            break
        else:
            print("Invalid option.")
