"""Defines the GPU class used to represent individual GPU listings."""

from app.models.pc_part import PcPart


class GPU(PcPart):
    """A GPU's specs.
    
    This class holds relevant GPU specficiation (expand?).
    """
    name: str
    website: str
    link: str
    price: str
    date: str
    brand: str

    def __init__(self, name: str, website: str, link: str, price: str, date: str, brand: str) -> None:
        """Initialize a new GPU object."""
        super().__init__(name, website, link, price, date, brand)