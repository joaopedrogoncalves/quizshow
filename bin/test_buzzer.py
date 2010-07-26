import BuzzManager, time
#import QuartzScoreManager
from SoundManager import SoundManager
import sys, time

bm = BuzzManager.BuzzManager()
#qsm = QuartzScoreManager.QuartzScoreManager()
sm = SoundManager()


qs_red   = "1,0.3,0.3,1"
qs_white = "1,1,1,1"
qs_black = "0,0,0,0"

colors = {
  'A Blue': '0,0,1,1',
  'B Orange': '1,0.5,0,1',
  'C Green': '0,1,0,1',
  'D Yellow': '1,1,0,1',
  'RED': '1,0,0,1'
}

"""
for e in  bm.ir.elements[26:len(bm.ir.elements)]:
    print e
    for x in [0,2,4,255]:
        time.sleep(0.5)
        try:
            e.write(x)
            print " - wrote OK"
            sys.exit(0)
        except:
            print " - Failed to write"
            pass
        

sys.exit(0)
"""

while True:
    time.sleep(0.1)
    ev = bm.poll(False)
    if ev:
        if ev.pressed:
#            qsm.playerColor(ev.player, colors[ev.color])
            print ev.player
            print ev.color
            sm.play( ev.player )
#        else:
#            qsm.playerColor(ev.player, qs_black)
