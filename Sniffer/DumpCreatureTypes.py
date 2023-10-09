from Shared import *


class CreatureTypeDumper(BaseDumper):
    def __init__(self):
        super().__init__(name="CreatureType")

    def get_creaturetype_index(
        self, dump_raw: bool = False, dump_processed: bool = False
    ) -> list[dict]:
        self.logger.info("Fetching creature type index...")
        url = f"{API_URL}/data/wow/creature-type/index"
        response = self.client.get(url)
        self.request_count += 1
        data = response.json()

        if dump_raw:
            file_name = f"{self.dump_path}/Raw/CreatureTypeIndex.json"
            dump_json(file_name, data)

        processed = compress_generic_dict(data["creature_types"])

        if dump_processed:
            file_name = f"{self.dump_path}/Processed/CreatureTypeIndex.csv"
            dump_csv(file_name, processed)

        return processed


if __name__ == "__main__":
    dumper = CreatureTypeDumper()
    toys = dumper.get_creaturetype_index(dump_raw=True, dump_processed=True)
