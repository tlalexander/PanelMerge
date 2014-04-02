#PanelMerge
A command line program for making PCB panels with gerbmerge.

####Why make a program for this? I thought that was the point of gerbmerge?
Well, that is sort of the point of gerbmerge. Taking a PCB file and duplicating it many times is a complex and code-intensive process. Gerbmerge provides all the interpreters, parsers, and structure needed to do all of this, but it lacks a clean user interface. The actual work to be done by gerbmerge is defined in a plain text configuration file that normally needs to be manually edited to include every layer of every board slated for panelization. This is a lot of manual entry, and would be tedious to do for every panel you want to make.

####How does panelmerge improve this?
Panelmerge is a command line program that essentially lets you drag and drop zip files for each board in a panel, creating the approptiate configuration file for you programatically. After defining a batch run with all of your boards, Panelmerge then runs gerbmerge with the automatic placement option. The automatic placement option randomly tries to make panels with the requested number of each board, saving the smallest configuration it finds.

####Disclaimer
It should be noted that panelmerge is not a cleanly finished program. It runs well in Linux and should run in Windows and Mac OS, but may require some changes for your system. First and foremost, the variable working_directory needs to be changed to a valid directory on your system. Panelmerge is in an early state, essentially a script to help the author make circuit board panels. It has been published in the hopes that others will find it useful.

####Preparation
You'll need to have python version 2.7 installed. You will also need gerbmerge and its dependencies. Gerbmerge can be found at http://174.136.57.214/gerbmerge/ or via google.

Make sure your PCB layers are in zip files with the following format:

\*.GTL Layer 1 (top)  
\*.G2L Layer 2  
\*.G3L Layer 3  
\*.GBL Layer 4 (bottom)  
\*.GTS Top Soldermask  
\*.GBS Bottom Soldermask  
\*.GTO Top Silkscreen  
\*.GBO Bottom Silkscreen  
\*.GKO Board Outline  
\*.XLN Drills  

You'll notice that there are 4 copper layers listed here. Panelmerge currently assumes a 4 layer board. It may work for a 2 layer board, but if there are any troubles, try removing the middle two layers from the configuration file (two locations):  
>\*InternalLayer1=%s.G2L  
>\*InternalLayer2=%s.G3L

####Instructions for use
Change the working directory at the top of panelmerge.py to a directory on your system where you would like the board files to be copied. Run panelmerge by executing the command 'python panelmerge.py" in the directory where you have placed panelmerge.

Panelmerge will present you with a command line interface. Generally, you will drag a zip file to the prompt and press enter. Panelmerge will open the zip and scan the files inside, presenting you with a list of files found. If the files found look correct panelmerge will ask you to name the current batch, which represents a PCB panel to be made. After entering a name you will be returned to the panelmerge prompt, where you can drop more zip files to add to the batch.

After adding all files to the batch, enter 'd' for done (followed by enter) and panelmerge will ask you how many copies of each board you would like to have in the final panel. After entering the quantities for each board, panelmerge will make the appropriate configuration file and run gerbmerge to start calculating the panel.

Gerbmerge will first ask you to enter 'y' after presenting you with a disclaimer, and will then start calculating panel possibilities. Panel calculation will continue indefinitely until you press Ctrl+c, at which time the calculation will stop and the best panel configuration found will be used to create your panel. Finished files will be found in the working directory under the output folder inside of a folder named for your batch.