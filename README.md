RAV

A project that creates random sound files from source files.  From the source sound, a target sound is created with shards of the source.  The user specifies the length of each shard, in seconds, and the total length of the target sound.  The shards are chosen randomly from the source file.  The length of each shard may also vary randomly in a specified range.

Usage:

No shard length variation:
./app.py <SRC_FILE> <DST_FILE> <shard_length> <total_length>

With shard length variation:
./app.py <SRC_FILE> <DST_FILE> <shard_length_lower_bound>-<shard_length_upper_bound> <total_length>