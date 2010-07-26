import PyHID
import time

class BuzzEvent():
    def __init__(self, buzz, event):
        """Buzz Event result"""
        self.ev = event
        self.buzz = buzz

        self.pressed = self.ev[1]
        self.player = self.buzz.playerN[ self.ev[0] ]
        self.buttonNumber = self.ev[0]

        self.color = self.buzz.buttonPair[self.ev[0]][2]
        self.multi = self.buzz.buttonPair[self.ev[0]][3]
 
        self.timestamp = self.ev[2]

class BuzzManager():
    def __init__(self):
        PyHID.initialise()
        devices = PyHID.scan_devices()
        mobile = []
#        print [x.name for x in devices]
#        ir =  [x for x in devices if x.name == 'Logitech Buzz(tm) Controller V1'][0]
        ir =  [x for x in devices if x.name == 'Wbuzz'][0]
        
        mobile =  [x for x in devices if x.name == 'C902']

        if mobile:
            mobile = mobile[0]
            mobile.enable_monitoring()
            mobile.elements[4].enable_monitoring()

        ir.enable_monitoring()
        time.sleep(0.5)
        ir.elements[28].write(1)
        
        self.ir = ir
        self.mobile = mobile
        
        self.setup_buttons()

    def clear_button_poll(self):
        while self.poll(False): pass
        if self.mobile:
            while self.mobile.poll(): pass
            
    def poll(self, onlyReturnButtonDown=True):
        """polls data from pyhid"""
        ev = self.ir.poll()
#        if ev:
#            print "EV: %s" %(ev,)
        if not ev: return False
        if onlyReturnButtonDown:
            if ev[1] == 1:
                return BuzzEvent(self, ev)
            else:
                return False
        else:
            return BuzzEvent(self, ev)

    def setup_buttons(self):
            buttons = range(2,25)
            buttonPair = [[] for x in range(2,25) ]
            playerN = range(2,25)
        
            colors = ["RED", "D Yellow", "C Green", "B Orange", "A Blue"]
            
            # Multi is used to identify values on a reply array.
            multi  = [4, 3, 2, 1, 0]
            
            for x in range(2,23):
                b = self.ir.elements[x]
                b.enable_monitoring()
                player = (x - 2) / 5
                but = (x - 2) % 5
                buttons[x] = "Player %d - %s" %(player+1, colors[but] )
#                print "%d - %s" % (x, buttons[x])
                
                buttonPair[x] = [player+1, but, colors[but], multi[but]]
                playerN[x] = player + 1
        
            self.buttons = buttons
            self.playerN = playerN
            self.buttonPair = buttonPair
            
