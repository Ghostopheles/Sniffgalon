import os

from dataclasses import dataclass, asdict

from .Shared import LOCALE, BaseDumper, dump_json, dump_csv, compress_generic_dict


@dataclass
class Category:
    id: int
    name: str


@dataclass
class Criteria:
    id: int
    description: str
    amount: int
    operator_type: str | None = None
    operator_name: str | None = None


@dataclass
class Achievement:
    id: int
    category: Category
    name: str
    description: str
    points: int
    is_account_wide: bool
    critera: Criteria
    display_order: int

    @staticmethod
    def from_json(data: dict):
        category = Category(
            id=data["category"]["id"],
            name=data["category"]["name"][LOCALE],
        )
        criteria = Criteria(
            id=data["criteria"]["id"],
            description=data["criteria"]["description"][LOCALE],
            amount=data["criteria"]["amount"],
            operator_type=data["criteria"]["operator"]["type"]
            if "operator" in data["criteria"]
            else None,
            operator_name=data["criteria"]["operator"]["name"][LOCALE]
            if "operator" in data["criteria"]
            else None,
        )

        return Achievement(
            id=data["id"],
            category=category,
            name=data["name"][LOCALE],
            description=data["description"][LOCALE],
            points=data["points"],
            is_account_wide=data["is_account_wide"],
            critera=criteria,
            display_order=data["display_order"],
        )

    def to_dict(self):
        return asdict(self)


class AchievementDumper(BaseDumper):
    object_class = Achievement

    def get_all_achievements_for_category(
        self,
        processed_category: dict,
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

        if self.dump_raw:
            path = os.path.normpath(
                f"{self.dump_path}/Raw/Achievements_{category_name}.json"
            ).replace(" ", "")
            dump_json(path, data)

        if "achievements" in data.keys():
            processed_data = compress_generic_dict(data[self.dict_key])
            if self.dump_processed:
                path = os.path.normpath(
                    f"{self.dump_path}/Processed/Achievements_{category_name}.csv"
                )
                dump_csv(path, processed_data)

            achievements = [achievement for achievement in processed_data]

            return achievements

    def get_all_achievements(self):
        categories = self.fetch_index(override_dict_key="categories")

        if not categories:
            return

        all_achievements = []
        for category in categories:
            achievements = self.get_all_achievements_for_category(category)

            if not achievements:
                continue

            all_achievements += achievements

        self.logger.info(
            f"Achievement fetching completed in {self.request_count} requests."
        )

        if self.dump_processed:
            file_name = f"{self.dump_path}/Processed/Achievements_All.csv"
            dump_csv(file_name, all_achievements)

        return all_achievements

    def fetch_all(self):
        return self.get_all_achievements()


if __name__ == "__main__":
    d = AchievementDumper.new(
        name="Achievements",
        path="achievement",
        dump_raw=True,
        dump_processed=True,
        override_index_endpoint="/achievement-category/index",
    )

    d.get_all_achievements()
