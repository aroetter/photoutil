# photoutil
Misc utilities for processing photos for organizing later

# delete_duplicate_files.py
Pass in a bunch of files, will delete all duplicates (defined by md5sum equivalance) and leave only one for each unique file

# add_prefix_to_files.py
Give me a prefix and 1+ files, and I'll preprend the predfix to every filename.
e.g.
```
./add_prefix_to_file.py hi foo.py bar.jpg"
# yields files
hi_foo.py hi_bar.jpg
```