from Shared import *


class AchievementDumper(BaseDumper):
    def __init__(self):
        super().__init__(name="Achievements")

    def get_achievement_categories_index(
        self, dump_raw: bool = False, dump_processed: bool = False
    ) -> list[dict]:
        self.logger.info("Fetching category index...")
        url = f"{API_URL}/data/wow/achievement-category/index"
        response = self.client.get(url)
        self.request_count += 1
        data = response.json()

        if dump_raw:
            file_name = f"{self.dump_path}/Raw/AchievementCategoriesIndex.json"
            dump_json(file_name, data)

        processed = compress_generic_dict(data["categories"])

        if dump_processed:
            file_name = f"{self.dump_path}/Processed/AchievementCategoriesIndex.csv"
            dump_csv(file_name, processed)

        return processed

    def get_all_achievements_for_category(
        self,
        processed_category: dict,
        dump_raw: bool = False,
        dump_processed: bool = False,
        parent_name: str = None,
    ) -> list[dict]:
        category_name = (
            processed_category["name"]
            if not parent_name
            else f"{parent_name}_{processed_category['name']}"
        )

        self.logger.info(f"Fetching achievements for category {category_name}")
        url = processed_category["href"]
        response = self.client.get(url)
        self.request_count += 1

        if response.status_code != 200:
            self.logger.error(
                f"Error occurred fetching achievements for {category_name} ({response.status_code})"
            )
            return

        data = response.json()

        if dump_raw:
            path = os.path.normpath(
                f"{self.dump_path}/Raw/Achievements_{category_name}.json"
            ).replace(" ", "")
            dump_json(path, data)

        if "achievements" in data.keys():
            processed_data = compress_generic_dict(data["achievements"])
            if dump_processed:
                path = os.path.normpath(
                    f"{self.dump_path}/Processed/Achievements_{category_name}.csv"
                )
                dump_csv(path, processed_data)

            return processed_data

    def get_all_achievements_for_all_categories(
        self,
        dump_raw: bool = False,
        dump_processed: bool = False,
        parent_name: str = None,
    ):
        categories = self.get_achievement_categories_index(
            dump_raw=dump_raw, dump_processed=dump_processed
        )

        all_achievements = {}
        for category in categories:
            achievements = self.get_all_achievements_for_category(
                category,
                dump_raw=dump_raw,
                dump_processed=dump_processed,
                parent_name=parent_name,
            )

            if not achievements:
                continue

            all_achievements[category["name"]] = achievements

        self.logger.info(
            f"Achievement fetching completed in {self.request_count} requests."
        )

        return all_achievements


if __name__ == "__main__":
    dumper = AchievementDumper()

    dumper.get_all_achievements_for_all_categories(dump_raw=True, dump_processed=True)
