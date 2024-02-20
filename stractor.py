#!/usr/bin/python3


# This script does the following:
# - It creates the dirlist file.
# - It creates v### folders.

from modules.c_dir_finder import *

import sys, os, shutil, subprocess
from datetime import datetime

progdir = os.path.dirname(os.path.realpath(__file__))

form1 = "%Y-%m-%d %H:%M:%S"
stime = datetime.now().strftime(form1)


indir = ""
oudir = ""
dirlist = ""

difi = c_dir_finder()

n_arg = len(sys.argv)

config_loaded = False

vte = []

save_log = False
log_fname = "z_stractor.log"  # default can be changed in config

ii = 0
while(True):
  ii += 1
  if ii >= n_arg:  break
  #
  arg = sys.argv[ii]
  #
  if arg == "--config":
    ii += 1
    config_loaded = True
    if ii >= n_arg:
      print("Error in reading arguments.")
      exit(1)
    #
    name_ifile = sys.argv[ii]
    #
    ifile = open( name_ifile, 'r' )
    for l in ifile:
      l = l.strip()
      if len(l) == 0:  continue
      if l[0] == '#':  continue
      mm = [m.strip() for m in l.split(';')]
      key = mm[0]
      #
      if key == "!end_of_data":  break
      elif key == '!sava_file':  sava_file = mm[1]
      elif key == "!indir":   indir = difi.fread_dir_list(ifile)
      elif key == "!dirlist": dirlist = mm[1]
      elif key == "!oudir":   oudir = difi.fread_dir_list(ifile)
      elif key == "!blobractor":  blobractor = mm[1]
      elif key == "!log_fname":  log_fname = mm[1]
      elif key == "!vids_to_extract":
        l = l.strip()
        ll = l.split(' ')
        ###
        if len(ll) > 1:  vids_to_extract = ll[1]
        else:            vids_to_extract = 'partial'
        if vids_to_extract == 'all':  continue
        ###
        for l in ifile:
          l = l.strip()
          if len(l) == 0:  break
          if l[0] == '#':  continue
          ll = l.split(' ')
          for k in range(len(ll)):
            vte.append( int(ll[k]) ) # vte:  vids to extract
      else:
        print("Error e0.  Unrecognized key.")
        print("  key:  ", key)
        sys.exit(1)
  elif arg == "--log":
    save_log = True
  else:
    print("Error.  Unrecognized argument.")
    print("  arg: ", arg)
    sys.exit(1)
  #
  #

if not config_loaded:
  print("Error.")
  print("  No config was loaded.")
  sys.exit(1)


if vids_to_extract != 'partial' and vids_to_extract != 'all':
  print("Error:  vids_to_extract no set correctly.")
  print("  Expected one of these:")
  print("    !vids_to_extract")
  print("    !vids_to_extract all")
  sys.exit(1)



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



invid = []
ouvid = []
fullinvid = []
fullouvid = []

lisa = os.listdir(indir)
lisa.sort()
vid_num = 0
for name in lisa:
  fu_dir = indir+'/'+name
  if not name.startswith("Video"):  continue
  if not os.path.isdir( fu_dir ):   continue
  if not os.path.isfile( fu_dir+'/Video Images.all' ):
    print("Warning.  Missing 'Video Images.all'.")
    print("  vid_num: ", vid_num)
    print("  name:    ", name)
  #
  vid_num += 1
  #
  invid.append(name)
  fullinvid.append(fu_dir+'/Video Images.all')
  #
  vid = 'v{:03d}'.format( vid_num )
  ouvid.append( vid )
  fullouvid.append( oudir+'/'+vid )
  #

n_vid = len(ouvid)
print("n_vid: ", n_vid)

if not os.path.isfile( sava_file ):
  print("Error.  Couldn't find sava file.")
  print("  sava_file: ", sava_file)
  sys.exit(1)

safi_n_vid = 0
f = open(sava_file, encoding='cp1252')
f.readline() # remove header.
for l in f:  safi_n_vid += 1
f.close()

if n_vid == safi_n_vid:
  print("Good:  n_vid == safi_n_vid.")
else:
  print("Error:  n_vid != safi_n_vid.")
  print("  n_vid:      ", n_vid)
  print("  safi_n_vid: ", safi_n_vid)
  sys.exit(1)



# If we get here, we're exporting videos.
if os.path.exists( dirlist ):
  print("Warning.  About to overwrite dirlist.")
  uin = input("  Is this OK (Y/n)? ")
  if uin != '' and uin != 'Y' and uin != 'y':
    print("Early exit.")
    sys.exit(0)
print("  OK")

ou = ''
for i in range(n_vid):
  vid_num = i+1
  ou += "v{:03d}".format( vid_num )
  ou += " ; "+fullinvid[i]
  ou += '\n'
fz = open(dirlist, 'w'); fz.write(ou);  fz.close();


n_vte = len(vte)
print("n_vte (vids to extract): ", n_vte)
for i in range(n_vte):
  vid_num = vte[i]
  if vid_num > n_vid or vid_num < 1:
    print("Error.  Couldn't find one of the vtes.")
    print("  vte: ", vid_num)
    sys.exit(1)


lisa = os.listdir(oudir)
if len(lisa) > 0:
  print("Error.  oudir is not empty.")
  print("  oudir: ", oudir)
  sys.exit(1)



for i in range(n_vte):
  vid_num = vte[i]
  vid = "v{:03d}".format(vid_num)
  os.mkdir(oudir+'/'+vid)


for i in range(n_vte):
  print('.', end='', flush=True)
  vid_num = vte[i]
  iv = vid_num - 1
  #
  cmd = [ blobractor ]
  cmd += [ "--blobfname", fullinvid[iv] ]
  cmd += [ "--oudir",     fullouvid[iv] ]
  rv = subprocess.call( cmd )
  if rv != 0:
    print()
    print("Error.")
    print("  blobractor rv = ", rv)
    exit(1)
print()

if save_log:
  ou = ''
  ou += '\n'
  ou += '#'+'_'*66 + '\n'
  ou += 'time  ; '+stime + '\n'
  ou += 'indir ; '+indir+'\n'
  ou += 'oudir ; '+oudir+'\n'
  ou += 'vte   ;'
  for i in range(n_vte):
    ou += ' '+str(vte[i])
  ou += '\n'
  progd = progdir.split('/')[-1]
  fgit = progdir+'/z_git_commit.data'
  ou += 'stractor dir ; '+progd+'\n'
  ou += 'git commit:\n'
  ou += '-'*22+'\n'
  if os.path.isfile(fgit):
    f=open(fgit)
    # Fist five lines max.
    i=0
    for l in f:
      l=l.strip()
      # Only non-empty lines.
      if len(l) > 0:  ou += l+'\n'
      i += 1
      if i == 5:  break
    f.close()
  else:
    ou += 'Git commit file not found.\n'
  #
  ou += '-'*22+'\n'
  ou += '\n'
  fz=open(log_fname,'a'); fz.write(ou); fz.close();

print("Done.")



