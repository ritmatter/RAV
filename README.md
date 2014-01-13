RAV
===

Creates new sound samples based on random shards of a source sound.  The shards are random sections of the original song,
and their length is specified by the user.  The shard length can also vary randomly in a specified range.

Usage:

With shard length variation:
./app.py SRC_FILE DST_FILE shard_lower_bound-shard_upper_bound total_length

Without shard length variation:
./app.py SRC_FILE DST_FILE shard_length total_length
