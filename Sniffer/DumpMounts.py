from Shared import *


class MountDumper(BaseDumper):
    def __init__(self):
        super().__init__(name="Mounts")

    def get_mounts_index(
        self, dump_raw: bool = False, dump_processed: bool = False
    ) -> list[dict]:
        self.logger.info("Fetching mounts index...")
        url = f"{API_URL}/data/wow/mount/index"
        response = self.client.get(url)
        self.request_count += 1
        data = response.json()

        if dump_raw:
            file_name = f"{self.dump_path}/Raw/MountsIndex.json"
            dump_json(file_name, data)

        processed = compress_generic_dict(data["mounts"])

        if dump_processed:
            file_name = f"{self.dump_path}/Processed/MountsIndex.csv"
            dump_csv(file_name, processed)

        return processed


if __name__ == "__main__":
    dumper = MountDumper()

    mounts = dumper.get_mounts_index(dump_raw=True, dump_processed=True)
