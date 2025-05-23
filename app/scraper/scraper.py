"""
Handles all web scraping functionality.

This module currently scrapes CPU listings from Newegg using requests and
BeautifulSoup. The extracted data is formatted into CPU objects.

Will be updated for additional parts, websites, and more advanced parsing.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random
from app.models.cpu import CPU
from app.models.gpu import GPU
from app.models.motherboard import MOBO
from app.utils.parsing import extract_cpu_info, extract_gpu_info, extract_mobo_info


def get_newegg_pages(url: str) -> int:
    """Returns the number of pages for a Newegg Pc part."""
    soup = BeautifulSoup(requests.get(url).text, "html.parser")

    pages_tag = soup.find(name="span", class_="list-tool-pagination-text").find(name="strong")
    last_page_number = int(pages_tag.text.split('/')[-1])

    return last_page_number


def scrape_newegg_cpus() -> list[CPU]:
    """Returns a list of CPU objects from scraping all available CPU data on Newegg."""
    cpus = []
    pages = get_newegg_pages("https://www.newegg.ca/p/pl?N=100007670%204814%208000&page=1&ComboBundle=true")

    for page in range(1, pages + 1):
        # fetch the webpage
        url = f"https://www.newegg.ca/p/pl?N=100007670%204814%208000&page={page}&ComboBundle=true"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser") 

        # extract all CPUs on page
        cpu_tags = soup.find_all(name="div", class_="item-cell")

        # extract relevant cpu information
        for cpu in cpu_tags:
            title = cpu.find(name="a", class_="item-title").text # contains all relevant info about product
            name, brand = extract_cpu_info(title)

            link = cpu.find(name="a", class_="item-title").get(key="href")

            try: # make sure price exists
                price_dollars = cpu.find(name="li", class_="price-current").find(name="strong").text
                price_cents = cpu.find(name="li", class_="price-current").find(name="sup").text
                price = price_dollars + price_cents # current price with discounts
            except:
                price = "N/A"

            date = datetime.now().isoformat()[:10] # YYYY-MM-DD format

            new_cpu = CPU(name, "newegg", link, price, date, brand)
            cpus.append(new_cpu)

        time.sleep(random.uniform(1.5, 3.0)) # limit scraping rate

    print(f"found {len(cpus)} CPUs.") # indicate how many CPUs were found when updating database

    return cpus


def scrape_newegg_gpus() -> list[GPU]:
    """Returns a list of CPU objects from scraping all available CPU data on Newegg."""
    gpus = []
    pages = get_newegg_pages("https://www.newegg.ca/p/pl?N=100007708%208000&page=1&ComboBundle=true")

    for page in range(1, pages + 1):
        # fetch the webpage
        url = f"https://www.newegg.ca/p/pl?N=100007708%208000&page={page}&ComboBundle=true"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # extract all GPUs on page
        gpu_tags = soup.find_all(name="div", class_="item-cell")

        # extract relevant cpu information
        for gpu in gpu_tags:
            title = gpu.find(name="a", class_="item-title").text # contains all relevant info about product
            name, brand = extract_gpu_info(title)

            link = gpu.find(name="a", class_="item-title").get(key="href")

            try: # make sure price exists
                price_dollars = gpu.find(name="li", class_="price-current").find(name="strong").text
                price_cents = gpu.find(name="li", class_="price-current").find(name="sup").text
                price = price_dollars + price_cents # current price with discounts
            except:
                price = "N/A"

            date = datetime.now().isoformat()[:10] # YYYY-MM-DD format

            new_gpu = GPU(name, "newegg", link, price, date, brand)
            gpus.append(new_gpu)

        time.sleep(random.uniform(1.5, 3.0)) # limit scraping rate
            
    print(f"found {len(gpus)} GPUs.") # indicate how many GPUs were found when updating database

    return gpus


def scrape_newegg_mobos() -> list[MOBO]:
    """Returns a list of MOBO objects from scraping all available desktop motherboard data on Newegg."""
    mobos = []
    amd_pages = get_newegg_pages("https://www.newegg.ca/p/pl?N=100007624%20601413462%20601413455%208000&page=1&ComboBundle=true")
    intel_pages = get_newegg_pages("https://www.newegg.ca/p/pl?N=100007626%208000%20601413471%20601458446&page=1&ComboBundle=true")

    # get all AMD motherboards
    for page in range(1, amd_pages + 1):
        # fetch the webpage
        url = f"https://www.newegg.ca/p/pl?N=100007624%20601413462%20601413455%208000&page={page}&ComboBundle=true"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # extract all motherboards on page
        mobo_tags = soup.find_all(name="div", class_="item-cell")

        # extract relevant cpu information
        for mobo in mobo_tags:
            title = mobo.find(name="a", class_="item-title").text # contains all relevant info about product

            name, brand = extract_mobo_info(title)

            link = mobo.find(name="a", class_="item-title").get(key="href")

            try: # make sure price exists
                price_dollars = mobo.find(name="li", class_="price-current").find(name="strong").text
                price_cents = mobo.find(name="li", class_="price-current").find(name="sup").text
                price = price_dollars + price_cents # current price with discounts
            except:
                price = "N/A"

            date = datetime.now().isoformat()[:10] # YYYY-MM-DD format

            new_mobo = MOBO(name, "newegg", link, price, date, brand)
            mobos.append(new_mobo)

        time.sleep(random.uniform(1.5, 3.0)) # limit scraping rate

    # get all Intel motherboards
    for page in range(1, intel_pages + 1):
        # fetch the webpage
        url = f"https://www.newegg.ca/p/pl?N=100007626%208000%20601413471%20601458446&page={page}&ComboBundle=true"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
         # extract all motherboards on page
        mobo_tags = soup.find_all(name="div", class_="item-cell")

        # extract relevant cpu information
        for mobo in mobo_tags:
            title = mobo.find(name="a", class_="item-title").text # contains all relevant info about product

            name, brand = extract_mobo_info(title)

            link = mobo.find(name="a", class_="item-title").get(key="href")

            try: # make sure price exists
                price_dollars = mobo.find(name="li", class_="price-current").find(name="strong").text
                price_cents = mobo.find(name="li", class_="price-current").find(name="sup").text
                price = price_dollars + price_cents # current price with discounts
            except:
                price = "N/A"

            date = datetime.now().isoformat()[:10] # YYYY-MM-DD format

            new_mobo = MOBO(name, "newegg", link, price, date, brand)
            mobos.append(new_mobo)

        time.sleep(random.uniform(1.5, 3.0)) # limit scraping rate

    print(f"found {len(mobos)} motherboards.") # indicate how many motherboards were found when updating database

    return mobos
