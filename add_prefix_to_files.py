#!/usr/bin/python

import os
import sys

def main(argv):
  if len(argv) < 3:
    print "Usage:"
    print "  %s PREFIX file1 file2 file3 ..." % argv[0]
    print "  Need to pass in a new prefix and at least one file."
    sys.exit(1)

  prefix = argv[1]

  print "Prefix is %s" % prefix
  for filename in argv[2:]:
    new = "%s_%s" % (prefix, filename)
    print "Renaming from %s to %s" % (filename, new)
    os.rename(filename, new)


if __name__ == "__main__":
  main(sys.argv)
  pass


