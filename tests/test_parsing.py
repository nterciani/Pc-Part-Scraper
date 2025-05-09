"""Testing module for the parsing functions in parsing.py"""

from app.utils import parsing


def test_extract_cpu_info() -> None:
    """Test that CPU info is properly extracted when given the full title of a CPU listing."""
    amd1 = "AMD Ryzen 9 9950X - Ryzen 9 9000 Series Granite Ridge (Zen 5) 16-Core 4.3 GHz - Socket AM5 170W - Radeon Graphics Processor - 100-100001277WOF"
    amd2 = "AMD Ryzen 7 7800X3D - Ryzen 7 7000 Series Zen 4 8-Core 4.2 GHz - Socket AM5 120W - AMD Radeon Graphics Desktop Processor - 100-100000910WOF"

    intel1 = "Intel Core i5-13400F Desktop Processor 10 cores (6 P-cores + 4 E-cores) 20MB Cache, up to 4.6 GHz - Box"
    intel2 = "Intel Core Ultra 9 285K - Core Ultra 9 (Series 2) Arrow Lake 24-Core (8P+16E), LGA 1851, 125W Desktop Processor - BX80768285K"

    threadripper = "AMD Ryzen Threadripper PRO 7965WX 350W SP6 - Zen 4 - 24-Core/48-Threads - 100-100000885WOF"
    pentium = "Intel Pentium G7400 - Pentium Gold Alder Lake Dual-Core 3.7 GHz LGA 1700 Processor 46W Intel UHD Graphics 710 Desktop Processor - BX80715G7400"

    assert parsing.extract_cpu_info(amd1) == ("AMD Ryzen 9 9950X", "AMD")
    assert parsing.extract_cpu_info(amd2) == ("AMD Ryzen 7 7800X3D", "AMD")

    assert parsing.extract_cpu_info(intel1) == ("Intel Core i5-13400F", "Intel")
    assert parsing.extract_cpu_info(intel2) == ("Intel Core Ultra 9 285K", "Intel")

    assert parsing.extract_cpu_info(threadripper) == ("AMD Ryzen Threadripper PRO 7965WX", "AMD")
    assert parsing.extract_cpu_info(pentium) == ("Intel Pentium G7400", "Intel")


if __name__ == "__main__":
    import pytest

    pytest.main(["test_parsing.py"])