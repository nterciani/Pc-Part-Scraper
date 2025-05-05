"""Defines the PcPart abstract class used to represent generic pc part listings."""


class PcPart():
    """A part/component of a PC.

    This is an abstract class. Only subclasses should be instantiated.

    === Attributes ===
    name: the name of this pc part
    website: the website where this pc part is found
    link: the website link for this pc part
    price: the price of this pc part
    date: the date for which the price was found
    brand: the brand that makes this pc part

    === Representation Invariants ===
    - website == "newegg" or website == "bestbuy" or 
      website == "amazon".
    """
    name: str
    website: str
    link: str
    price: str
    date: str
    brand: str

    def __init__(self, name: str, website: str, link: str, price: str, date: str, brand: str) -> None:
        """Initialize a new PcPart object."""
        self.name = name
        self.website = website
        self.link = link
        self.price = price
        self.date = date
        self.brand = brand

    def __str__(self) -> str:
        """Return a formatted version of this PcPart's attributes."""
        return f"({self.name}, {self.website}, {self.price}, {self.date})"