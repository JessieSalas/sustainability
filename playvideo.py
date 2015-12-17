import time
import os

compostvid = 'default.avi'
cansvid = './default.avi'
papervid = './mixedpaper1.avi'
trashvid = '/home/pi/running/sintel_trailer-480p.mpg'

def play(trashbin):
    #play video of corresponding bin
    if trashbin == 'cans':
        vfile = cansvid
    elif trashbin == 'trash':
        vfile = trashvid
    elif trashbin == 'paper':
        vfile = papervid
    elif trashbin == 'compost':
        vfile = compostvid
    else:
        vfile = trashvid
    os.system( 'mplayer {0}'.format(vfile))
    

