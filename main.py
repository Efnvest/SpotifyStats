import os

from Compactor import dataCompacter
from Graphics.dataViewer import viewHistory







# Main file used for running th whole process
# Should include the compression of data and starting the visualizer.

## Could add a checker to se if a specific .json file exsist, avoids running the
# compactor more than once. 

#TODO: make a file and folder finder.
#TODO: controll for multiple runs, check for exsisting compact json file. Faster runtime. 
#TODO: seprat method for labled map of locations. 



file_Path = 'Compactor/streaming_summary.json'
    
if os.path.exists(file_Path):
    print('yes')
    viewHistory(file_Path)
else:
    print('no')
    dataCompacter.streamingHistory('SPOTIFY_FOLDER_HER/Spotify Extended Streaming History')
    viewHistory(file_Path)