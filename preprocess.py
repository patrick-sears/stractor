#!/usr/bin/python3


# This script does the following:
# - It creates the dirlist file.
# - It creates v### folders.


from subprocess import call

import sys
import os
# from os import system
# from pathlib import Path





if len(sys.argv) < 2:
  print( "Error:  Config filename not supplied." )
  exit(1)



name_ifile = sys.argv[1]


indir = ""
oudir = ""
dirlist = ""

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



# Check to see if dirlist already exists.
if os.path.isfile( dirlist ):
 print( "Error:  indir file already exists." )
 exit(1)


# Store all the Video folder names in file 'dirlist'.
cmd = "ls -d " + indir + "/Video* > \"" + dirlist + "\""
os.system( cmd )








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
  cmd += [ "prs-blobractor" ]
  cmd += [ "--blobfname", fullinvid[i] ]
  cmd += [ "--oudir", fullouvid[i] ]
  rv = call( cmd )
  if rv != 0:
    print("Error.")
    print("  blobractor rv = ", rv)
    exit(1)





