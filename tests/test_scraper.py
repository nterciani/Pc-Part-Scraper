"""Testing module for functions in scraper.py"""

from app import scraper


def test_extract_cpu_name() -> None:
    """Test that cpu names are properly extracted by the extract_cpu_name function.
    """
    amd1 = "AMD Ryzen 9 9950X - Ryzen 9 9000 Series Granite Ridge (Zen 5) 16-Core 4.3 GHz - Socket AM5 170W - Radeon Graphics Processor - 100-100001277WOF"
    amd2 = "AMD Ryzen 7 7800X3D - Ryzen 7 7000 Series Zen 4 8-Core 4.2 GHz - Socket AM5 120W - AMD Radeon Graphics Desktop Processor - 100-100000910WOF"
    amd3 = "AMD Ryzen 5 5500 - Ryzen 5 5000 Series Cezanne (Zen 3) 6-Core 3.6 GHz Socket AM4 65W None Integrated Graphics Desktop Processor - 100-100000457BOX"

    intel1 = "Intel Core i7-14700K - Core i7 14th Gen 20-Core (8P+12E) LGA 1700 125W Intel UHD Graphics 770 Processor - Boxed - BX8071514700K"
    intel2 = "Intel Core i5-13400F Desktop Processor 10 cores (6 P-cores + 4 E-cores) 20MB Cache, up to 4.6 GHz - Box"
    intel3 = "Intel Core Ultra 9 285K - Core Ultra 9 (Series 2) Arrow Lake 24-Core (8P+16E), LGA 1851, 125W Desktop Processor - BX80768285K"

    assert scraper.extract_cpu_name(amd1) == "AMD Ryzen 9 9950X"
    assert scraper.extract_cpu_name(amd2) == "AMD Ryzen 7 7800X3D"
    assert scraper.extract_cpu_name(amd3) == "AMD Ryzen 5 5500"

    assert scraper.extract_cpu_name(intel1) == "Intel Core i7-14700K"
    assert scraper.extract_cpu_name(intel2) == "Intel Core i5-13400F"
    assert scraper.extract_cpu_name(intel3) == "Intel Core Ultra 9 285K"


if __name__ == "__main__":
    import pytest

    pytest.main(["test_scraper.py"])