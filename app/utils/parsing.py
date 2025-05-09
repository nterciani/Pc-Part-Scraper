"""This module contains functions for extracting specific Pc part information."""

import re


def extract_cpu_info(full_title: str) -> tuple[str, str]:
    """Extract and return the clean CPU name and brand from <full_title>."""
    match_name = r"^(AMD Ryzen \d \w*|Intel Core Ultra \d+ \w*|Intel Core i\d+-\d+\w*|AMD Ryzen Threadripper ?(PRO)? \d*\w*|Intel Pentium \w*)"
    match_brand = r"^(AMD|Intel)"

    name = re.match(match_name, full_title)
    brand = re.match(match_brand, full_title)

    return name.group(0), brand.group(0)


def extract_gpu_info(full_title: str) -> tuple[str, str]:
    """Extract and return the clean GPU name and brand from <full_title>."""
    match_brand = r"(?i)^(?:(Refurbished|Open Box) +)?(\w+)"

    brand = re.match(match_brand, full_title)

    return full_title, brand.group(1) # get name later


def extract_mobo_info(full_title: str) -> tuple[str, str]:
    """Extract and return the clean motherboard name and brand from <full_title>."""
    match_brand = r"(?i)^(?:(Refurbished|Open Box) +)?(\w+)"

    brand = re.match(match_brand, full_title)

    return full_title, brand.group(1) # get name later