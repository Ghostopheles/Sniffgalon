from Shared import *


class ReputationFactionDumper(BaseDumper):
    def __init__(self):
        super().__init__(name="ReputationFaction")

    def get_rep_factions_index(
        self, dump_raw: bool = False, dump_processed: bool = False
    ) -> list[dict]:
        self.logger.info("Fetching reputation factions index...")
        url = f"{API_URL}/data/wow/reputation-faction/index"
        response = self.client.get(url)
        self.request_count += 1
        data = response.json()

        if dump_raw:
            file_name = f"{self.dump_path}/Raw/ReputationFactionIndex.json"
            dump_json(file_name, data)

        processed = compress_generic_dict(data["factions"])

        if dump_processed:
            file_name = f"{self.dump_path}/Processed/ReputationFactionIndex.csv"
            dump_csv(file_name, processed)

        return processed


if __name__ == "__main__":
    dumper = ReputationFactionDumper()
    toys = dumper.get_rep_factions_index(dump_raw=True, dump_processed=True)
