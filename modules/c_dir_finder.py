#!/usr/bin/python3

import sys,os

class c_dir_finder:
  def __init__(self):
    self.udir = None
  def fread_dir_list(self, f):
    # Selects the first dir it finds.
    lisa = []
    for l in f:
      l = l.strip()
      if len(l) == 0:  break
      if l[0] == '#':  continue
      mm = [m.strip() for m in l.split(' ; ')]
      lisa.append( mm[1] )
    #
    n_lisa = len(lisa)
    self.udir = None
    for i in range(n_lisa):
      cdir = lisa[i]
      if os.path.isdir( lisa[i] ):
        self.udir = lisa[i]
        break
    if self.udir == None:
      print("Error.  Couldn't find dir.")
      print("  Searched these dirs:")
      for i in range(n_lisa):
        print("    ", lisa[i])
      sys.exit(1)
    #
    return self.udir
    #




