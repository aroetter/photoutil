#!/Users/aroetter/anaconda2/bin/python

# Delete (all but one) copy of a duplicate photo


import hashlib
from optparse import OptionParser
import os
import re
import sys


options = None # will get filles out in main()



# copied from https://www.joelverhagen.com/blog/2011/02/md5-hash-of-file-in-python/
def md5Checksum(filePath):
    with open(filePath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192 * 8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()


def do_delete(fname):
  """ Delete a file, or practice it in --dryrun mode. """
  global options
  if options.dryrun:
    print "  Dryrun delete of %s." % fname
  else:
    print "  Deleting %s." % (fname)
    os.remove(fname)


def main(argv):
  parser = OptionParser()
  parser.add_option("-d", "--dryrun",
                  action="store_true", dest="dryrun", default=False,
                  help="don't print status messages to stdout")

  global options
  (options, args) = parser.parse_args()

  if len(argv) < 2:
    print "Need to pass in at least one file..."

  # a map from md5sum of a file (string), to all files names (list of strings) that have that hash
  hash_to_files = {}
   
  for fname in args:
    md5 = md5Checksum(fname)
    if md5 not in hash_to_files:
      hash_to_files[md5] = []
    hash_to_files[md5].append(fname)

  for (md5, files) in hash_to_files.iteritems():
    print "Hash %s has files %s" % (md5, files)
    if len(files) > 1:
      files.sort(reverse=True)
      to_delete = files[1:]
      for fname in to_delete:
        do_delete(fname)


if __name__ == "__main__":
  main(sys.argv)
  pass

