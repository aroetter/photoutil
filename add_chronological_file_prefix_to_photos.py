#!/Users/aroetter/anaconda2/bin/python

# Take a photos with a meaningless name, extract date from EXIF
# data and rename

import exifread
from optparse import OptionParser
import os
import re
import sys


options = None # will get filles out in main()

def do_rename(oldname, newname):
  global options
  if options.dryrun:
    print "Simulated rename of %s to %s." % (oldname, newname)
  else:
    print "Renaming %s to %s." % (oldname, newname)
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


exif_timestamp_pattern = re.compile('(\d{4}):(\d{2}):(\d{2}) (\d{2}):(\d{2}):(\d{2})')
DATETIME_KEY = 'Image DateTime'

def process_using_exif_data(fname):
  """ TODO: document me. """
  f = open(fname, 'rb')
  tags = exifread.process_file(f)

  if DATETIME_KEY in tags.keys():
    tstamp = tags[DATETIME_KEY]
    match = exif_timestamp_pattern.match(tstamp.printable)
    if match is None:
      print "SHOULD NEVER HAPPEN!"
      sys.exit(1)
    y = match.group(1)
    m = match.group(2)
    d = match.group(3)
    #h = match.group(4)
    #mi = match.group(5)
    #s = match.group(6)
    new_fname = get_new_filename(fname, y, m, d)
    do_rename(fname, new_fname)
    return True
  else:
    #print "Exif Method won't work. [%s] has no DATETIME. EXIF fields: are %s" % (fname, tags.keys())
    return False
  pass


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
    print "Need to pass in at least one file..."

   
  for fname in args:

    if should_skip_file(fname):
      print "Skipping [%s]. Already has YYYY-MM-DD_*.jpg." % fname
    elif process_using_exif_data(fname):
      pass
    elif process_using_android_file_naming_convention(fname):
      pass
    else:
      print "Can't handle file [%s]" % fname


if __name__ == "__main__":
  main(sys.argv)
  pass

