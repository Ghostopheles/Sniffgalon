# Sniffgalon

Some tools for easily dumping World of Warcraft API data to `json` and `csv`.

## Usage

**Requires `Python>=3.12.0`**

Install requirements with `pip install -r requirements.txt`, then run [Sniffer/Main.py](https://github.com/Ghostopheles/Sniffgalon/blob/master/Sniffer/Main.py).
* This will create top-level `Logs/` and `Data/` folders.
* To change the region or locale used, change the global variables in [Sniffer/Dumper/Shared.py](https://github.com/Ghostopheles/Sniffgalon/blob/master/Sniffer/Dumper/Shared.py).
* Inside [Sniffer/Main.py](https://github.com/Ghostopheles/Sniffgalon/blob/master/Sniffer/Main.py), you can enable/disable the raw `json` and processed `csv` outputs.

## Advanced Usage

All of the dumpers share the same base class (defined in [Sniffer/Dumper/Shared.py](https://github.com/Ghostopheles/Sniffgalon/blob/master/Sniffer/Dumper/Shared.py)) and contain functions for fetching specific IDs or a list of IDs.
* Currently only Achievements supports this behavior, will expand to the other areas in the future.