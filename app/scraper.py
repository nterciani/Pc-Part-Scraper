"""
Handles all web scraping functionality.

This module currently scrapes CPU listings from Newegg using requests and
BeautifulSoup. The extracted data is formatted into CPU objects.

Will be updated for additional parts, websites, and more advanced parsing.
"""

import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
from app.models.cpu import CPU


def extract_cpu_name(full_title: str) -> str:
    """Extract and return the clean CPU name from <full_title>.
    """
    match = re.match(r"^(AMD Ryzen \d \d+\w*|Intel Core Ultra \d+ \d+\w*|Intel Core i\d+-\d+\w*)", full_title)

    return match.group(0) if match else full_title


def scrape_newegg_cpus() -> list[CPU]:
    """Returns a list of CPU objects from scraping all available CPU data on Newegg.
    """
    # === ONLY PAGE 1 SO FAR, WILL EXPAND ===
    # fetch the webpage
    url = "https://www.newegg.ca/Desktop-CPU-Processor/SubCategory/ID-343/Page-1"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # extract all CPUs on page 1
    cpu_tags = soup.find_all(name="div", class_="item-cell")

    print(f"found {len(cpu_tags)} CPUs") # debug

    # extract relevant cpu information
    cpus = []
    for cpu in cpu_tags:
        title = cpu.find(name="a", class_="item-title").text # contains all relevant info about product
        name = extract_cpu_name(title) # strictly name of cpu

        link = cpu.find(name="a", class_="item-title").get(key="href")

        price_dollars = cpu.find(name="li", class_="price-current").find(name="strong").text
        price_cents = cpu.find(name="li", class_="price-current").find(name="sup").text
        price = price_dollars + price_cents # current price with discounts

        date = datetime.now().isoformat()[:10] # YYYY-MM-DD format

        new_cpu = CPU(name, "newegg", link, price, date)
        cpus.append(new_cpu)

    return cpus


if __name__ == "__main__":
    #Run the scraper and print CPUs for testing
    cpus = scrape_newegg_cpus()
    for cpu in cpus:
        print(cpu)