#!/usr/bin/python3

# Extract date from EXIF data and rename
# 
# Need imagemagick. On Mac OS X
# brew install imagemagick
# export PATH=${PATH}:~/homebrew/bin/
# 1. Install the rust programming language
# 2. Install libheif
# 3. Install libheif-rs
# 4. Install cykooz.heif
#    sudo pip3 install setuptools-rust
#    sudo pip3 install cykooz.heif
#
import exifread
from optparse import OptionParser
import os
import re
import subprocess
import sys

options = None # will get filles out in main()

def do_rename(oldname, newname):
  global options
  if options.dryrun:
    print("Simulated rename of", oldname, "to", newname)
  else:
    print("Renaming ", oldname, " to ", newname, ".")
    os.rename(oldname, newname)

def get_new_filename(orig_fname, y, m, d):
  album_name = "_%s" % options.album if options.album is not None else ""
  return "%s-%s-%s%s_%s" % (y, m, d, album_name, orig_fname)

already_renamed_file_pattern = re.compile('20\d\d-\d{2}-\d{2}_.*\.jpg')
def should_skip_file(fname):
  """
  If a file already matches 20YY-MM-DD_text.jpg then we don't need to 
  rename it.
  """
  match = already_renamed_file_pattern.match(fname)
  return match is not None


DATETIME_REGEX = '(\d{4}):(\d{2}):(\d{2}) (\d{2}):(\d{2}):(\d{2})'
exif_timestamp_pattern = re.compile(DATETIME_REGEX)
DATETIME_KEY = 'Image DateTime'
# *.heif files seem to have this one
DATETIME_ORIG_KEY = 'EXIF DateTimeOriginal'

# TODO: delete this method
def process_using_exif_data(fname):
  """ TODO: document me. """
  f = open(fname, 'rb')
  tags = exifread.process_file(f)

  if DATETIME_KEY in tags.keys():
    datestr = tags[DATETIME_KEY]
    print("CASE 1 fname=", fname)
  elif DATETIME_ORIG_KEY in tags.keys():
    datestr = tags[DATETIME_ORIG_KEY]
    print("CASE 2 fname=", fname)
  else:
    print ("Exif Method won't work for [", fname, "]. keys=", tags.keys())
    return False

  match = exif_timestamp_pattern.match(datestr.printable)
  if match is None:
    print("SHOULD NEVER HAPPEN!")
    sys.exit(1)
  y = match.group(1)
  m = match.group(2)
  d = match.group(3)
  new_fname = get_new_filename(fname, y, m, d)
  do_rename(fname, new_fname)
  return True


android_pattern = re.compile('IMG-(\d{4})(\d{2})(\d{2})-WA(\d{4}).jpg')
def process_using_android_file_naming_convention(fname):
  """ TODO: document me. """
    
  match = android_pattern.match(fname)

  if match is not None:
    (y, m, d, seqno) = (
      match.group(1), match.group(2), match.group(3), match.group(4))
    do_rename(fname, get_new_filename(fname, y, m, d))
    return True
  else:
    return False

def process_using_imagemagick_exif(fname):
  out = subprocess.Popen(['identify', '-format', '%[EXIF:DateTimeOriginal*]', fname], 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
  stdout, stderr = out.communicate()
  tomatch = stdout.decode('ascii').strip()
  imagemagick_output_regex = re.compile('exif:DateTimeOriginal=' + DATETIME_REGEX)
  match = imagemagick_output_regex.match(tomatch)
  if match is None:
    print ("WHAT?!?!?!")
    sys.exit(1)

  y = match.group(1)
  m = match.group(2)
  d = match.group(3)

  do_rename(fname, get_new_filename(fname, y, m, d))
  return True

def main(argv):
  parser = OptionParser()
  parser.add_option("-a", "--album", dest="album",
                    help="The album name. Will be incorporated into any rewritten filenames, if present",
                    metavar="ALBUM")
  parser.add_option("-d", "--dryrun",
                  action="store_true", dest="dryrun", default=False,
                  help="don't print status messages to stdout")

  global options

  (options, args) = parser.parse_args()

  if len(argv) < 2:
    print("Need to pass in at least one file...")

  for fname in args:
    if should_skip_file(fname):
      print("Skipping [", fname, "]. Already has YYYY-MM-DD_*. format.")
    # TODO: delete this cruft
    #elif process_using_exif_data(fname):
    #  pass
    #elif process_using_android_file_naming_convention(fname):
    #  pass
    elif process_using_imagemagick_exif(fname):
      pass
    else:
      print("Can't handle file [", fname, "]")


if __name__ == "__main__":
  main(sys.argv)
  pass

