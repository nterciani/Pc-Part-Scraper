"""Defines the CPU class used to represent individual CPU listings."""


class CPU():
    """A CPU's specs
    
    This class holds relevant CPU specficiation (expand?).

    === Attributes ===
    name: the name of this CPU
    website: the website where this CPU is found
    link: the website link for this CPU
    price: the price of this CPU
    date: the date for which the price was found

    === Representation Invariants ===
    - website == "newegg" or website == "bestbuy" or 
      website == "amazon".
    """
    name: str
    website: str
    link: str
    price: str
    date: str

    def __init__(self, name: str, website: str, link: str, price: str, date: str) -> None:
        """Initialize a new CPU object.
        """
        self.name = name
        self.website = website
        self.link = link
        self.price = price
        self.date = date

    def __str__(self) -> str:
        """Return a formatted version of this CPU's attributes"""
        return f"name: {self.name}\nprice: {self.price}\nlink: {self.link}\ndate: {self.date}\n"
