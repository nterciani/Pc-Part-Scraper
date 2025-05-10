# PC Part Price Tracker

A Python command-line application that scrapes Pc part listings from Newegg and stores their prices in a local SQLite database. Users can interactively search and view component listings by name.

> ⚠️ Project is a work in progress — currently supports Newegg scraping for CPUs, GPUs, and motherboards.

---

## Features

- Scrapes current CPU, GPU, and motherboard listings from Newegg.
- Stores scraped data with historical pricing in a normalized SQLite database.
- Command-line interface for querying components by type or name.
- Modular architecture with support for future websites and part categories.

---

## Project Structure
```graphql
app/
├── cli/               # CLI interaction and updater logic
│   ├── interactive.py
│   └── updater.py
├── database/          # SQLite setup, inserts, queries
│   └── database.py
├── models/            # OOP classes for PC parts
│   ├── cpu.py, gpu.py, motherboard.py, pc_part.py
├── scraper/           # Web scrapers
│   └── scraper.py
├── utils/             # Helper functions (e.g. name extraction)
│   └── parsing.py
├── config.py          # Configurations for the app
├── main.py            # CLI entry point
tests/                 # Unit tests for scraper and database modules
├── test_parsing.py  
parts.db               # Local SQLite DB (created after update)
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/nterciani/Pc-Part-Scraper.git
cd Pc-Part-Scraper
```

### 2. Ensure Python 3.12 or higher is installed.


### 3. Create a virtual environment

```bash
python -m venv .venv

# For macOS/Linux:
source .venv/Scripts/activate

# For Windows:
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

### Update the database with scraped listings:
```bash
python -m app.main --update
```

### Launch the interactive Command Line Interface:
```bash
python -m app.main --interactive
```