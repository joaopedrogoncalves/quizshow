import Arduino
import time

a = Arduino.Arduino()
print "OFF"
a.send_msg(0)
print "Starting"
time.sleep(1)
for x in range(32):
    for x in range(8):
        print x+1
        time.sleep(0.1)
        print "\tON"
        a.send_msg(1<<x)
        time.sleep(0.1)
        a.send_msg(0)
        print "\tOFF"
        

time.sleep(1)
a.send_msg(255)
