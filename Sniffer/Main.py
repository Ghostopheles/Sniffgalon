from Dumper import get_dumpers

# dump raw response json
dump_raw = True

# dump csv with just id, name, and api url
dump_processed = True

all_dumpers = get_dumpers(dump_raw=dump_raw, dump_processed=dump_processed)

for dumper in all_dumpers:
    dumper.fetch_all()
