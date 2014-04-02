#! /usr/bin/env python

#   panelmerge, a simple program to create PCB panels using gerbmerge
#   Copyright Taylor Alexander 2013

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# imports
from sys import exit
import subprocess
from shutil import make_archive
import glob, os, shutil, sys
import zipfile

# variables
batchname=""
proj_list = []
ext_arr=['.GBO','.GBS','.GBL','.GTL','.GTO','.GTP','.GTS','.GOL','.TXT','G2L','G3L','.XLN']

# Assign the working directory. Batches and associated files will be stored here.
#working_directory = os.path.expanduser('~') #user's home directory. Should probably be changed when on windows (works on Win but weird).
#working_directory+= "/Dropbox/PCB/panelmerge/batches" # if you have things arranged like me use this or similar, otherwise use line below
working_directory= "/mnt/storage1/Dropbox/PCB/panelmerge/batches" # alternative directory suggestion. comment out the above line and uncomment this if desired.


# TODO:
# modify project contents
# refresh saved files
# view main directory project contents and select one
# 
#

#functions
def refresh_console(): # clears the terminal and adds the CLI header
    print chr(27) + "[H" # terminal command to reset terminal cursor position. see http://www.termsys.demon.co.uk/vtansi.htm
    print chr(27) + "[2J" # terminal command to erase screen. these two commands clean up the screen for us.
    print "**** Welcome to gerbmerge CLI. ****"
    print ""
    print "Current project directory is:"
    print working_directory
    if batchname != "":
        print ""
        print "Batch name is: %s" % batchname
        for index,project in enumerate(proj_list):
            print "Proj %d: %s" % (index, project)
        print ""
        print "Drag zipped gerbers here, or enter 'h' for help."

def append_project(filename, text_to_append):
    try:
        # This tries to open an existing file but creates a new file if necessary.
        file = open(filename, "a")
        try:
            file.write(text_to_append)
        finally:
            file.close()
            return True
    except IOError:
        return False

def reload_zip(source, dest):
    if zipfile.is_zipfile(source):
      #      print extract_path
        z = zipfile.ZipFile(source, "r")
        z.extractall(dest) # extract zip to specified folder
    else:
        print "Source '%s' is not zip file." % source.strip()

def load_project(project): # file I/O via http://snipplr.com/view/6630/
    try:
        # Read mode opens a file for reading only.
        filename = "%s/%s/%s.txt" % (working_directory, project, project)
        f = open(filename, "r")
        try:
            # read all the lines into a list.
            lines = f.readlines()
            global proj_list
            global batchname
            proj_list = []
            for line in lines:
                print "Found projects: %s" % line.split(';')[0]
                proj_list.append(line.split(';')[0])
            
         
            if raw_input("Project loaded. Reload zip files? Enter y to reload or just hit enter to skip. ") == 'y':
                for line in lines:
                    if len(line.split(';')) > 2:
                        file = line.split(';')[2]
                        project = line.split(';')[0]
                        extract_path = "%s/%s/%s/" % (working_directory, batchname, project)
                        reload_zip(file.strip(),extract_path.strip())
                      
            
        except:
            print "For filename '%s', there was an error." % filename
            print "Unexpected error:", sys.exc_info()[0]
            raw_input()
        finally:
            f.close()
    except IOError:
        
        print "Error reading project contents. Press enter to reset projects."
        raw_input()
        global proj_list
        proj_list = []
        batchname=""
        
def addproject(name, path, copies):
    return """
##############################################################################
[%s]
# List all the layers that participate in this job. Required layers are Drills
# and BoardOutline and have no '*' at the beginning.  Optional layers have
# names chosen by you and begin with '*'. You should choose consistent layer
# names across all jobs.

*TopLayer=%s.GTL
*InternalLayer1=%s.G2L
*InternalLayer2=%s.G3L
*BottomLayer=%s.GBL
*TopSilkscreen=%s.GTO
*BottomSilkscreen=%s.GBO
*TopSoldermask=%s.GTS
*BottomSoldermask=%s.GBS
Drills=%s.XLN
BoardOutline=%s.GKO

# If this job does not have drill tool sizes embedded in the Excellon file, it
# needs to have a separate tool list file that maps tool names (e.g., 'T01') to
# tool diameter. This may be the global tool list specified in the [Options]
# section with the ToolList parameter. If this job doesn't have embedded tool
# sizes, and uses a different tool list than the global one, you can specify it
# here.
#ToolList=proj1.drl

# If this job has a different ExcellonDecimals setting than the global setting
# in the [Options] section above, it can be overridden here.
#ExcellonDecimals = 3

# You can set a 'Repeat' parameter for this job when using automatic placement
# (i.e., no *.def file) to indicate how many times this job should appear in
# the final panel. When using manual placement, this option is ignored.
Repeat = %d
""" % (name,path,path,path,path,path,path,path,path,path,path,copies)
    

def setoutput(path):
    return """    
##############################################################################
[MergeOutputFiles]

*TopLayer=%s.GTL
*InternalLayer1=%s.G2L
*InternalLayer2=%s.G3L
*BottomLayer=%s.GBL
*TopSilkscreen=%s.GTO
*BottomSilkscreen=%s.GBO
*TopSoldermask=%s.GTS
*BottomSoldermask=%s.GBS
Drills=%s.XLN
BoardOutline=%s.GKO
ToolList = %s.toollist.drl
Placement = %s.placement.txt
""" % (path,path,path,path,path,path,path,path,path,path,path,path)
    
        
d = os.path.dirname(working_directory) #if folder does not exist, create it
if not os.path.exists(d):
    os.makedirs(d)


#ext_arr_key=['.GBO','.GBS','.GBL','.GTL','.GTO','.GTP','.GTS','.GOL','.TXT'] #TODO: Implement key

refresh_console()

while True:
    
    name=""
    while name == "":
        name=raw_input(">").strip() # strip() removes trailing whitespace that ends up there
	
	if "'" in name:
		name = name.replace("'", "") # lazy string cleanup remove single quotes from string. I don't recall this being needed on windows, but it was needed on Linux.
        
    if "\ " in name:
        name = name.replace("\ ", " ") # cleans up filename that was dropped into terminal if it has spaces
    
    if name=='h': # show help TODO: change how this works to not suck.
        print " quit = q\r\n done adding = d\r\n clear console = c\r\n list/switch batches in master dir = b\r\n erase all projects = eraseall\r\n help = h"
        
    elif name=='d':
        break # break while loop, we are done adding files
        
    elif name=='c':
        refresh_console() # clear console/refresh
    
    elif name=='rp':
        if batchname == "":
            print "No batch name assigned. Type one now or press enter to use 'temp'. All files in that dir will be wiped."
            batchname = raw_input(">")
            if batchname == "":
                batchname = "temp"
        for line in proj_list:
            print len(line.split(';'))
            if len(line.split(';')) > 2:
                file = line.split(';')[2]
                print file
                project = line.split(';')[0]
                print project
                extract_path = "%s/%s/%s/" % (working_directory, batchname, project)
                reload_zip(file.strip(),extract_path.strip())
        refresh_console() # reload zip
        
    elif name=='pp': # print projects in batch
        print "Projects in batch:"
        for index, project in enumerate(proj_list):
            print "Proj %d: %s" % (index, project)
    
    elif name=='b':
        print "Project Batches in main directory:"
        for index, dirname in enumerate(os.listdir(working_directory)):
            if dirname[0] != '.': # hide hidden folders
                print dirname
        print "Type a batch name to assign as the current batch, or press enter to return."
        oldbatch = batchname
        batchname = raw_input(">")
        if oldbatch != "":
            print "Change from batch '%s' to batch '%s'? (y/n)" % (oldbatch, batchname)
            if raw_input(">")!='y':
                batchname = oldbatch
        if batchname != "":
            load_project(batchname)
            refresh_console()
            
       
    elif name=='eraseall':
        # erase all files
        print ""
        print "*** WARNING: This command will delete all files in the following directory! ***"
        print "--"
        print working_directory
        print "--"
        print "Type 'yes' to proceed, otherwise this will be canceled."
        if raw_input(">")=="yes": 
            for root, dirs, files in os.walk(working_directory, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    if(name != "layout.cfg"):
                        os.rmdir(os.path.join(root, name))
        else:
            print "Files not erased."
    
    elif name=='q':
        exit(0)
     
    elif os.path.exists(name): # if we dropped a zip file here, handle it
        
        print "Filename is: %s" % name
        
        matched_files=0;
        
        if zipfile.is_zipfile(name):
            z = zipfile.ZipFile(name, "r")
            for ext in ext_arr:
                for filename in z.namelist():
                    try:
                        # filename = os.path.basename(filename)
                        bytes = z.read(filename)
                        head, tail = os.path.split(filename)
                        filename = tail                    
                        if filename[0]!='.': # by this point we've peeked the contents of the zip file and excluded anything strange
                                            # so now we see if the files match what we need (all necessary gerber files present),
                                            # and then we ask if we should save and proceed.
                                            # and if so we copy them to our temp dir, save the paths (so we can refresh without another drop),
                                            # and then facilitate the batch. Also ask for a batch name, and make batch-specific temp files
                        
                        
                            if os.path.splitext(filename)[1] == ext:
                                print filename + "  -  %d kb, has extension %s" % ((len(bytes)/1000), ext)
                                matched_files+=1
                    except:
                        print "cannot split string %s or match extension %s" % (filename, ext)
                        continue #continue is fine, the try just freaks out with some of the weird filenames listed as being part of a zip file
        answer = raw_input("Found %d matching files. Add to batch? (y/n) " % matched_files)
        if answer == 'y':
            if batchname == "":
                print "No batch name assigned. Type one now or press enter to use 'temp'. All files in that dir will be wiped."
                batchname = raw_input(">")
                if batchname == "":
                    batchname = "temp"
            project_name = os.path.splitext(filename)[0];
            extract_path = "/%s/%s/%s" % (working_directory, batchname, project_name)
            print extract_path
            z.extractall(extract_path) # extract zip to specified folder
            proj_list.append(project_name) #append project entry to project details list
            textfile_path = "/%s/%s/%s.txt" % (working_directory, batchname, batchname)
            project_string = "%s;0;%s\r\n" % (project_name, name)
            if append_project(textfile_path ,project_string):
                print "Files saved into batch %s" % batchname
            else:
                print "File I/O error, cannot proceed. Hit enter to quit."
                raw_input()
                exit(0)
            
            raw_input("Hit enter to continue")
            refresh_console()
        elif answer =='n':
            print "Files not saved"
        else:
            print "Invalid entry, please drop file again."
        
    else:
        print "Invalid file or command"
        
#raw_input("Hit enter to add text to project file")
source = "%s/layout.cfg" % os.path.dirname(working_directory)
#print source
dest = "%s/%s/layout.cfg" % (working_directory, batchname)
#print dest
shutil.copyfile(source, dest) # copies skeleton config file to batch directory

append_project(dest, setoutput("%s/output/merge" % os.path.dirname(dest) )) # assign output directory to batch folder

folder = "%s/output" % os.path.dirname(dest) # make sure folder exists
if not os.path.exists(folder):
    os.makedirs(folder)

for project in proj_list:
    copies = raw_input("How many copies of %s should be made?" % project)
    proj_dest = "%s/%s/%s/%s" % (working_directory, batchname, project, project)
    append_project(dest, addproject(project, proj_dest, int(copies)))

call = "gerbmerge --random-search %s" % dest
print "CMD to run:%s" % call
#subprocess.call(call)
os.system(call)
sys.exit(0)
        
