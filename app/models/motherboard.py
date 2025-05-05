"""Defines the MOBO class used to represent individual motherboard listings."""

from app.models.pc_part import PcPart


class MOBO(PcPart):
    """A motherboard's specs.
    
    This class holds relevant motherboard specficiation (expand?).
    """
    name: str
    website: str
    link: str
    price: str
    date: str
    brand: str

    def __init__(self, name: str, website: str, link: str, price: str, date: str, brand: str) -> None:
        """Initialize a new motherboard object."""
        super().__init__(name, website, link, price, date, brand)