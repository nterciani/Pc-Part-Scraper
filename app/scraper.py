"""
Handles all web scraping functionality.

This module currently scrapes CPU listings from Newegg using requests and
BeautifulSoup. The extracted data is formatted into CPU objects.

Will be updated for additional parts, websites, and more advanced parsing.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from app.models.cpu import CPU
from app.models.gpu import GPU
from app.utils.parsing import extract_cpu_info, extract_gpu_info


def get_pages(url: str) -> int:
    """Returns the number of pages for a Newegg Pc part.
    """
    soup = BeautifulSoup(requests.get(url).text, "html.parser")

    pages_tag = soup.find(name="span", class_="list-tool-pagination-text").find(name="strong")
    last_page_number = int(pages_tag.text.split('/')[-1])

    return last_page_number


def scrape_newegg_cpus() -> list[CPU]:
    """Returns a list of CPU objects from scraping all available CPU data on Newegg.
    """
    cpus = []
    pages = get_pages("https://www.newegg.ca/p/pl?N=100007670%204814%208000&page=1&ComboBundle=true")

    for page in range(1, pages + 1):
        # fetch the webpage
        url = f"https://www.newegg.ca/p/pl?N=100007670%204814%208000&page={page}&ComboBundle=true"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser") 

        # extract all CPUs on page
        cpu_tags = soup.find_all(name="div", class_="item-cell")

        print(f"found {len(cpu_tags)} CPUs on page {page}.") # debug

        # extract relevant cpu information
        for cpu in cpu_tags:
            title = cpu.find(name="a", class_="item-title").text # contains all relevant info about product
            name, brand = extract_cpu_info(title)

            link = cpu.find(name="a", class_="item-title").get(key="href")

            price_dollars = cpu.find(name="li", class_="price-current").find(name="strong").text
            if price_dollars == "COMING SOON":
                price = "COMING SOON"
            else:
                price_cents = cpu.find(name="li", class_="price-current").find(name="sup").text
                price = price_dollars + price_cents # current price with discounts

            date = datetime.now().isoformat()[:10] # YYYY-MM-DD format

            new_cpu = CPU(name, "newegg", link, price, date, brand)
            cpus.append(new_cpu)

    return cpus


def scrape_newegg_gpus() -> list[GPU]:
    gpus = []
    pages = get_pages("https://www.newegg.ca/p/pl?N=100007708%208000&page=1&ComboBundle=true")

    for page in range(1, pages + 1):
        # fetch the webpage
        url = f"https://www.newegg.ca/p/pl?N=100007708%208000&page={page}&ComboBundle=true"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # extract all GPUs on page
        gpu_tags = soup.find_all(name="div", class_="item-cell")

        print(f"found {len(gpu_tags)} GPUs on page {page}.") # debug

        # extract relevant cpu information
        for gpu in gpu_tags:
            title = gpu.find(name="a", class_="item-title").text # contains all relevant info about product
            name, brand = extract_gpu_info(title)

            link = gpu.find(name="a", class_="item-title").get(key="href")

            price_dollars = gpu.find(name="li", class_="price-current").find(name="strong").text
            if price_dollars == "COMING SOON":
                price = "COMING SOON"
            else:
                price_cents = gpu.find(name="li", class_="price-current").find(name="sup").text
                price = price_dollars + price_cents # current price with discounts

            date = datetime.now().isoformat()[:10] # YYYY-MM-DD format

            new_gpu = GPU(name, "newegg", link, price, date, brand)
            gpus.append(new_gpu)
            
    return gpus


if __name__ == "__main__":
    # # Run the scraper and print CPUs for testing
    # cpus = scrape_newegg_cpus()
    # for cpu in cpus:
    #     print(cpu)

    # Run the scraper and print GPUs for testing
    gpus = scrape_newegg_gpus()
    for gpu in gpus:
        print(gpu)
