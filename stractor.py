#!/usr/bin/python3


# This script does the following:
# - It creates the dirlist file.
# - It creates v### folders.


from subprocess import call

import sys
import os
# from os import system
# from pathlib import Path




indir = ""
oudir = ""
dirlist = ""


n_argv = len(sys.argv)

mode = "None"

for i in range(1, n_argv):
  if sys.argv[i] == "--config":
    i += 1
    if i == n_argv:
      print("Error in reading arguments.")
      exit(1)
    #
    name_ifile = sys.argv[i]
    #
    ifile = open( name_ifile, 'r' )
    for l in ifile:
      if l == '\n':  continue
      if l == '!end_of_data\n': break
      if    l == "!indir\n":
        indir = ifile.readline().strip()
      elif  l == "!dirlist\n":
        dirlist = ifile.readline().strip()
      elif  l == "!oudir\n":
        oudir = ifile.readline().strip()
      elif  l == "!blobractor\n":
        blobractor = ifile.readline().strip()
  elif sys.argv[i] == "--mode_make_list":
    mode = "make_list"
  elif sys.argv[i] == "--mode_export":
    mode = "export"


if mode == "None":
  print( "Error:  mode was not set." )
  print( "  Need either --mode_make_list or --mode_export." )
  exit(1)


if len(indir) == 0:
  print( "Error:  indir not found in config file." )
  exit(1)
if len(oudir) == 0:
  print( "Error:  oudir not found in config file." )
  exit(1)
if len(dirlist) == 0:
  print( "Error:  dirlist not found in config file." )
  exit(1)

print( "!indir:    [" + indir + "]" )
print( "!oudir:    [" + oudir + "]" )
print( "!dirlist:  [" + dirlist + "]" )






if mode == "make_list":
  # Check to see if dirlist already exists.
  if os.path.isfile( dirlist ):
    print( "Error:  dirlist file already exists." )
    exit(1)
  #
  # Store all the Video folder names in file 'dirlist'.
  cmd = "ls -d " + indir + "/Video* > \"" + dirlist + "\""
  os.system( cmd )
  #
  #
  exit(0)



# If we get here, we're exporting videos.
if not os.path.isfile( dirlist ):
  print( "Error:  dirlist file doesn't exists." )
  exit(1)



# Import vid list into this script.
invid = []
ouvid = []
fullinvid = []
fullouvid = []

f2 = open( dirlist )
i = 0
for l in f2:
  l = l.strip()
  if len(l) == 0:  continue
  if l[0] == '#':  continue
  #
  invid.append(l)
  #
  vvv = 'v' + str(i+1).zfill(3)
  ouvid.append( vvv )
  #
  #
  fullinvid.append( invid[i]+'/'+"Video Images.all")
  fullouvid.append( oudir+'/'+vvv )
  #
  i += 1
f2.close()


n_vid = len(invid)
print( "Found %1d" % n_vid, "videos." )




############################################
# Make vid folders.


# Check to make sure invids exist.
# If one is missing, it's really strange.
for i in range( n_vid ):
  if not os.path.exists( fullinvid[i] ):
    print( "Error:  invid missing" )
    print( "  Missing:  ", fullinvid[i])
    exit(1)


# Check to see if any of the vid folders exist.
# If so, exit with an error so that we don't overwrite
# previously exported images by mistake.
for i in range( n_vid ):
  if os.path.exists( fullouvid[i] ):
    print( "Error:  vid", fullouvid[i], "output dir already exists." )
    exit(1)



# Now create all the folders.
for i in range( n_vid ):
  v = i + 1
  vvv = 'v' + str(v).zfill(3)
  os.mkdir( oudir + "/" + vvv )



############################################
# For each vid, call prs-blobractor.
cmd = []
for i in range( n_vid ):
  # cmd += [ "prs-blobractor" ]
  cmd += [ blobractor ]
  cmd += [ "--blobfname", fullinvid[i] ]
  cmd += [ "--oudir", fullouvid[i] ]
  rv = call( cmd )
  if rv != 0:
    print("Error.")
    print("  blobractor rv = ", rv)
    exit(1)





