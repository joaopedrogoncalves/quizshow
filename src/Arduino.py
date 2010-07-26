# Arduino Client and server. If run from __main__, becomes a server. 
# If imported acts as a client.

import serial
import socket, traceback
import time, sys


class Arduino():
    """Arduino Client, sends data via UDP, handles relay lights"""
    def __init__(self, udp_port=9999):
        self.udp_port = udp_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.connect( ("127.0.0.1", udp_port) )
        self.lights_off()

    def send_msg(self, msg):
        self.socket.send(str(msg))
        
    
    def lights_off(self):
        self.send_msg( 0 )
    
    def set_player_light(self, player):
        p =  self.get_players_from_int(1<< player-1)
        self.set_player_lights(p)
        
    def set_player_lights(self, players):
        """
        Sets players lights by receiving an Array with four
        pairs, True and False, representing each player's 
        right and wrong light.
        """

        n = self._get_lights_int(players)
        self.last_state = n
        self.send_msg( n )
        
    def get_players_from_int(self, n):
        p = [[False,False] for x in range(4)]
        for x in range(4):
            for l in 0,1:
                light = 1 << x  + (l*4)
                if  light & n: 
                    p[x][l] = True
        return p
    
    def _get_lights_int(self, players):                
        if len(players) != 4:
            raise TypeError
        state = 0
        for i, p in enumerate(players):
            for l in 0,1:
                light = 1 << i  + (l*4)
                if p[l] == True: state |= light
        return state
            
class ArduinoServer():
    """Arduino Serial communications"""
    def __init__(self, port="/dev/cu.usbserial-A7006vJk", udp_port=9999):
        self.serial_port = port
        self.udp_port = udp_port
    
        self.init_serial()
        self.init_udp()
        
    def send_raw(self, msg):
        self.port.write(msg)
        return True
        
    def send(self, data):
        self.send_raw(chr(data))
        return True

    def init_udp(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print "Starting with %d" %(self.udp_port,)
        self.socket.bind( ("localhost", self.udp_port) )
        
# Make sure pins are working correctly.
    def init_serial(self):
        self.port = serial.Serial(port=self.serial_port, timeout=1)
        print "Testing Arduino pins in %s (%s)" %(self.port, str(self.serial_port) )
        for x in range(5):
            self.send(255)
            time.sleep(0.5)
            self.send(0)
            time.sleep(0.5)
        print "Done."

        
    def pass_message(self):
        try:
            message, address = self.socket.recvfrom(128)
            print "Got Message(%s) Proxying to Arduino.\n\n" %(message,)
            self.send( int(message) )
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            traceback.print_exc()



if __name__ == '__main__':
    server = ArduinoServer()
    print "UDP Daemon ready on port 9999."
    while 1:
        server.pass_message()


"""

while 1:
    try:
        message, address = s.recvfrom(8192)
        print "Got %s from" % message, address
        s.sendto(message, address)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        traceback.print_exc()
        

sys.exit(0)

class Arduino():
#Arduino Serial Manager. Just sends bits via UDP
    def __init__(self, arg):
        super(Arduino, self).__init__()
        self.arg = arg
    








def s(b):
    port.write(chr(b))

print "Clean up"

for x in range(5):
    s(0)
    time.sleep(0.5)
    s(255)
    time.sleep(0.5)

print "Done."


pins = range(8)
pins.reverse()

for x in pins:
    s(0)
    print "OFF"
    time.sleep(0.5)
    v = 1 << x
    s(1 << x)
    print "%d (%d)" % (x, v) 
    time.sleep(1)

def decide(): 
    while buzz.poll(False): pass
    state = 0
    counter = 500
    won = 0 
    s(0)
    while 1:
        time.sleep(0.01)
        if state != 0:
            counter -= 1
            print counter
            if counter < 0:
                return

        e = buzz.poll(False)
        if e and e.color == "RED":
            if won == e.player: continue
            if e.pressed: 
                if state > 0:
                    light = 1 << (e.player + 3)
                else:
                   light = 1 << (e.player -1)
                   won = e.player
                   print "Player %d won" %(e.player)

                state = state | light
                s(state)
#            else:
#                state = state ^ light
#                s(state)

#            return
#       else:
#           s(0)

#       s(state)


#for x in range(255):
#    print x
#    port.write(chr(x))
#    print port.read(10)

"""