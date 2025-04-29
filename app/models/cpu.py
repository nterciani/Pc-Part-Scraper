"""Defines the CPU class used to represent individual CPU listings."""

from app.models.pc_part import PcPart


class CPU(PcPart):
    """A CPU's specs.
    
    This class holds relevant CPU specification (expand?).
    """
    name: str
    website: str
    link: str
    price: str
    date: str
    brand: str

    def __init__(self, name: str, website: str, link: str, price: str, date: str, brand: str) -> None:
        """Initialize a new CPU object."""
        super().__init__(name, website, link, price, date, brand)
