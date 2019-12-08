import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
import os
 
addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')

foundLines=[]
selected=[]

kodiLog=addon.getSetting('kodiLog')
outputFile=addon.getSetting('outputFile')

file = open(kodiLog, "r")

with file as searchfile:
    for line in searchfile:
        if 'added to' in line:
            foundLines.extend([line.split("'")[1]])
            print(line.split("'")[1])

if len(foundLines) < 1:
    xbmcgui.Dialog().ok(addonname, "Found no uninitialized Media. Please issue a 'UpdateLibrary' and execute again")
else:
    print(foundLines)

    # Let the user select the files to rename
    ret = xbmcgui.Dialog().multiselect("Not initialized Media", foundLines)

    # if the user hits cancel, all found filenames will be written into the specified path
    if ret is None:
        with open(outputFile, mode='wt') as myfile:
            myfile.write('\n'.join(str(line) for line in foundLines))
            xbmcgui.Dialog().ok(addonname, "Wrote all found files/paths to '" + outputFile + "'")
    else:
        # Rename line per line
        for line in ret:
            # Cut the path/filename into pieces, so we can work with them later, when renaming the file
            fullPath = foundLines[line]
            fullBasename = os.path.basename(foundLines[line])
            basename = os.path.splitext(fullBasename)[0]
            filePath = os.path.splitext(foundLines[line])[0]
            extension = os.path.splitext(foundLines[line])[1]

            # /home/peter/videos/serien/tolleSerie1/E01/akdlsj.avi
            print("FullPath: " + fullPath)
            # akdlsj.avi
            print("FullBasename: " + fullBasename)
            # akdlsj
            print("Basename: " + basename)
            # /home/peter/videos/serien/tolleSerie1/E01
            print("FilePath: " + filePath)
            # .avi
            print("Extension: " + extension)

            keyb = xbmc.Keyboard(basename, 'Enter New Filename (without extension!)')
            keyb.doModal()

            if keyb.isConfirmed():
                # Grab the text from the input
                newFilename = keyb.getText()
                # Concatenate the new filename to match the correct path
                fullPathNewFilename = filePath + "/" + newFilename + extension
                print("Renaming '" + fullPath + "' into '" + fullPathNewFilename)
                success = xbmcvfs.rename(fullPath,fullPathNewFilename)
                # Warning, if something goes wrong
                if success != True:
                    xbmcgui.Dialog().ok(addonname, "There was an error renaming. Please check the permissions.")