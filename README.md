# Sniffgalon

Some tools for easily dumping World of Warcraft API data to `json` and `csv`.

## Usage

**Requires `Python>=3.12.0`**

Install requirements with `pip install -r requirements.txt`, then run [Sniffer/Main.py](https://github.com/Ghostopheles/Sniffgalon/blob/master/Sniffer/Main.py).
* This will create top-level `Logs/` and `Data/` folders.
* To change the region or locale used, change the global variables in [Sniffer/Dumper/Shared.py](https://github.com/Ghostopheles/Sniffgalon/blob/master/Sniffer/Dumper/Shared.py).
* Inside [Sniffer/Main.py](https://github.com/Ghostopheles/Sniffgalon/blob/master/Sniffer/Main.py), you can enable/disable the raw `json` and processed `csv` outputs.

## Advanced Usage

All of the dumpers share the same base class (defined in [Sniffer/Dumper/Shared.py](https://github.com/Ghostopheles/Sniffgalon/blob/master/Sniffer/Dumper/Shared.py)) and contain `fetch_specific` and `fetch_many` functions for fetching a specific ID or a list of IDs.
* Currently only the achievements dumper supports this behavior, will expand to the other areas in the future. See [Sniffer/Dumper/Achievements.py](https://github.com/Ghostopheles/Sniffgalon/blob/master/Sniffer/Dumper/Achievements.py) for an example of how it's set up.