from Shared import *


class CreatureFamilyDumper(BaseDumper):
    def __init__(self):
        super().__init__(name="CreatureFamily")

    def get_creaturefamily_index(
        self, dump_raw: bool = False, dump_processed: bool = False
    ) -> list[dict]:
        self.logger.info("Fetching creature family index...")
        url = f"{API_URL}/data/wow/creature-family/index"
        response = self.client.get(url)
        self.request_count += 1
        data = response.json()

        if dump_raw:
            file_name = f"{self.dump_path}/Raw/CreatureFamilyIndex.json"
            dump_json(file_name, data)

        processed = compress_generic_dict(data["creature_families"])

        if dump_processed:
            file_name = f"{self.dump_path}/Processed/CreatureFamilyIndex.csv"
            dump_csv(file_name, processed)

        return processed


if __name__ == "__main__":
    dumper = CreatureFamilyDumper()
    toys = dumper.get_creaturefamily_index(dump_raw=True, dump_processed=True)
