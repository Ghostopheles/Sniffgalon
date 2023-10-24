from .Shared import BaseDumper
from .Achievements import AchievementDumper


class Dumpers:
    def __init__(self, dump_raw: bool, dump_processed: bool):
        self.__dumpers = []
        self.__index = 0

        self.add_dumper(
            BaseDumper.new(
                name="Mounts",
                path="mount",
                dump_raw=dump_raw,
                dump_processed=dump_processed,
            )
        )
        self.add_dumper(
            BaseDumper.new(
                name="Titles",
                path="title",
                dump_raw=dump_raw,
                dump_processed=dump_processed,
            )
        )
        self.add_dumper(
            BaseDumper.new(
                name="Toys",
                path="toy",
                dump_raw=dump_raw,
                dump_processed=dump_processed,
            )
        )
        self.add_dumper(
            BaseDumper.new(
                name="Pets",
                path="pet",
                dump_raw=dump_raw,
                dump_processed=dump_processed,
            )
        )
        self.add_dumper(
            BaseDumper.new(
                name="CreatureFamilies",
                path="creature-family",
                dump_raw=dump_raw,
                dump_processed=dump_processed,
                override_key_name="creature_families",
            )
        )
        self.add_dumper(
            BaseDumper.new(
                name="CreatureTypes",
                path="creature-type",
                dump_raw=dump_raw,
                dump_processed=dump_processed,
                override_key_name="creature_types",
            )
        )
        self.add_dumper(
            BaseDumper.new(
                name="ReputationFactions",
                path="reputation-faction",
                dump_raw=dump_raw,
                dump_processed=dump_processed,
                override_key_name="factions",
            )
        )
        self.add_dumper(
            BaseDumper.new(
                name="JournalEncounters",
                path="journal-encounter",
                dump_raw=dump_raw,
                dump_processed=dump_processed,
                override_key_name="encounters",
            )
        )
        self.add_dumper(
            BaseDumper.new(
                name="JournalInstances",
                path="journal-instance",
                dump_raw=dump_raw,
                dump_processed=dump_processed,
                override_key_name="instances",
            )
        )
        self.add_dumper(
            AchievementDumper.new(
                name="Achievements",
                path="achievement",
                dump_raw=True,
                dump_processed=True,
                override_index_endpoint="/achievement-category/index",
            )
        )

    def add_dumper(self, dumper):
        self.__setattr__(dumper.name, dumper)
        self.__dumpers.append(dumper)

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self):
        if self.__index < len(self.__dumpers):
            result = self.__dumpers[self.__index]
            self.__index += 1
            return result
        else:
            raise StopIteration


def get_dumpers(dump_raw: bool, dump_processed: bool) -> Dumpers:
    return Dumpers(dump_raw=dump_raw, dump_processed=dump_processed)
