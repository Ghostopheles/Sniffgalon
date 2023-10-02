from Shared import *


class TitleDumper(BaseDumper):
    def __init__(self):
        super().__init__(name="Titles")

    def get_titles_index(
        self, dump_raw: bool = False, dump_processed: bool = False
    ) -> list[dict]:
        self.logger.info("Fetching titles index...")
        url = f"{API_URL}/data/wow/title/index"
        response = self.client.get(url)
        self.request_count += 1
        data = response.json()

        if dump_raw:
            file_name = f"{self.dump_path}/Raw/TitlesIndex.json"
            dump_json(file_name, data)

        processed = compress_generic_dict(data["titles"])

        if dump_processed:
            file_name = f"{self.dump_path}/Processed/TitlesIndex.csv"
            dump_csv(file_name, processed)

        return processed


if __name__ == "__main__":
    dumper = TitleDumper()

    titles = dumper.get_titles_index(dump_raw=True, dump_processed=True)
