from DumpAchievements import AchievementDumper
from DumpMounts import MountDumper
from DumpTitles import TitleDumper
from DumpToys import ToyDumper

# this file is sort of a band-aid until I decide to bring this all together a bit more cohesively
# supposed to be a "one-click" solution to dump all the things your heart may desire

achievements = AchievementDumper()
mounts = MountDumper()
titles = TitleDumper()
toys = ToyDumper()

# dump raw response json
dump_raw = True

# dump csv with just id, name, and api url
dump_processed = True

# to disable dumping of any of the below things, just comment the line out
achievements.get_all_achievements_for_all_categories(dump_raw, dump_processed)
mounts.get_mounts_index(dump_raw, dump_processed)
titles.get_titles_index(dump_raw, dump_processed)
toys.get_toys_index(dump_raw, dump_processed)
