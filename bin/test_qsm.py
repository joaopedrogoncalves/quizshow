import QuartzScoreManager
import sys, time
import random

qsm = QuartzScoreManager.QuartzScoreManager()
#sm = SoundManager()


qs_red   = "1,0.3,0.3,1"
qs_white = "1,1,1,1"
qs_black = "0,0,0,0"

colors = {
  'A Blue': '0,0,1,1',
  'B Orange': '1,0.5,0,1',
  'C Green': '0,1,0,1',
  'D Yellow': '1,1,0,1',
  'RED': '1,0,0,1',
  'black': qs_black,
  'white': qs_white,
}

a  = colors.values()
while True:

    for i in [1,2,3,4]:
#        random.shuffle(a)
        color = ''
        r = str(float(random.randrange(0,100))/100)
        for x in range(3):
#            color += str(float(random.randrange(0,100))/100)
            color += r
            color += ","
        color += "1"
#        print color
        qsm.playerColor(i , color)
    time.sleep(0.1)
#        qsm.playerColor(i, qs_black)
#        time.sleep(0.3)
#        qsm.playerColor(i, qs_white)
#

