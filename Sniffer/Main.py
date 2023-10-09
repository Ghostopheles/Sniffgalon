from DumpAchievements import AchievementDumper
from DumpMounts import MountDumper
from DumpTitles import TitleDumper
from DumpToys import ToyDumper
from DumpPets import PetDumper
from DumpCreatureFamilies import CreatureFamilyDumper
from DumpCreatureTypes import CreatureTypeDumper
from DumpReputationFactions import ReputationFactionDumper

# this file is sort of a band-aid until I decide to bring this all together a bit more cohesively
# supposed to be a "one-click" solution to dump all the things your heart may desire

achievements = AchievementDumper()
mounts = MountDumper()
titles = TitleDumper()
toys = ToyDumper()
pets = PetDumper()
creatureFamily = CreatureFamilyDumper()
creatureTypes = CreatureTypeDumper()
factions = ReputationFactionDumper()

# dump raw response json
dump_raw = True

# dump csv with just id, name, and api url
dump_processed = True

# to disable dumping of any of the below things, just comment the line out
achievements.get_all_achievements_for_all_categories(dump_raw, dump_processed)
mounts.get_mounts_index(dump_raw, dump_processed)
titles.get_titles_index(dump_raw, dump_processed)
toys.get_toys_index(dump_raw, dump_processed)
pets.get_pets_index(dump_raw, dump_processed)
creatureFamily.get_creaturefamily_index(dump_raw, dump_processed)
creatureTypes.get_creaturetype_index(dump_raw, dump_processed)
factions.get_rep_factions_index(dump_raw, dump_processed)
