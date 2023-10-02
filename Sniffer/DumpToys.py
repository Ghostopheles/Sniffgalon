from Shared import *


class ToyDumper(BaseDumper):
    def __init__(self):
        super().__init__(name="Toys")

    def get_toys_index(
        self, dump_raw: bool = False, dump_processed: bool = False
    ) -> list[dict]:
        self.logger.info("Fetching toys index...")
        url = f"{API_URL}/data/wow/toy/index"
        response = self.client.get(url)
        self.request_count += 1
        data = response.json()

        if dump_raw:
            file_name = f"{self.dump_path}/Raw/ToysIndex.json"
            dump_json(file_name, data)

        processed = compress_generic_dict(data["toys"])

        if dump_processed:
            file_name = f"{self.dump_path}/Processed/ToysIndex.csv"
            dump_csv(file_name, processed)

        return processed


if __name__ == "__main__":
    dumper = ToyDumper()
    toys = dumper.get_toys_index(dump_raw=True, dump_processed=True)
