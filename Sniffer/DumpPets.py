from Shared import *


class PetDumper(BaseDumper):
    def __init__(self):
        super().__init__(name="Pets")

    def get_pets_index(
        self, dump_raw: bool = False, dump_processed: bool = False
    ) -> list[dict]:
        self.logger.info("Fetching pets index...")
        url = f"{API_URL}/data/wow/pet/index"
        response = self.client.get(url)
        self.request_count += 1
        data = response.json()

        if dump_raw:
            file_name = f"{self.dump_path}/Raw/PetsIndex.json"
            dump_json(file_name, data)

        processed = compress_generic_dict(data["pets"])

        if dump_processed:
            file_name = f"{self.dump_path}/Processed/PetsIndex.csv"
            dump_csv(file_name, processed)

        return processed


if __name__ == "__main__":
    dumper = PetDumper()
    toys = dumper.get_pets_index(dump_raw=True, dump_processed=True)
