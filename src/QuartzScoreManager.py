import socket, struct

class QuartzScoreManager():
    """docstring for QuartzManager"""
    def __init__(self):
        self.start_sockets()
        self.clear()

    def start_sockets(self):
#        broadcast_host = '127.0.0.1'
        broadcast_host = '225.0.0.0'
        MYGROUP = broadcast_host

        self.white_color = "1,1,1,1"
        self.red_color = "1,0,0,1"
        self.black_color = "0,0,0,0"
        self.clear_string = self.black_color

        self.player_sockets = []
        
        for port in (55001, 55010, 55020, 55030):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            s.bind(("192.168.2.1", port))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.player_sockets.append([s, port ])

    def display(self, my_socket, string):
        for x in range(3):
            ttl = struct.pack('b', 1)        
            s, port = my_socket
            s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)
            s.sendto(self.utf32encode(string), ("225.0.0.0", port))


    def utf32encode(self, s):
        s = s.encode('utf-16be')
        ret = ''
        i= 0
        while i < len(s):
            ret += '\0\0' + s[i:i+2]
            i += 2
        return ret

    def playerColor(self, player, color):
        player = player -1
        if player < len(self.player_sockets):
#            print "Sending %s to %d" % (color, player)
            self.display(self.player_sockets[player], color)

    def playerColors(self, colors):
        if colors == " ":
            # clear
            print "Clearing display"
            for s in self.player_sockets:
                self.display(s, self.black_color)
        else:
            i = 0
            for s in self.player_sockets:
                self.display(s, colors[i])
                i = i + 1
    
    def set_player_wrong(self, player):
        self._set_light(player, self.red_color)
        
    def set_player_right(self, player):
        self._set_light(player, self.white_color)

    def _set_light(self, player, color):
        self.display(self.player_sockets[player-1], color)
    
    def set_player_light(self, player):
        self.set_player_right(player)
    
    def set_player_lights(self, players):
        # player[0] - correct (white)
        # player[1] - wrong (red)
        
        i = 0
        for player in players:
            if player[0] == True:
                self.display(self.player_sockets[i], self.white_color )
                                
            if player[1] == True:
                self.display(self.player_sockets[i], self.red_color)
            i = i +1

    
    def get_players_from_int(self, n):
        p = [[False,False] for x in range(4)]
        for x in range(4):
            for l in 0,1:
                light = 1 << x  + (l*4)
                if  light & n: 
                    p[x][l] = True
        return p        
        
    def lights_off(self):
        for s in self.player_sockets:
            self.display(s, self.black_color)
    
    def clear(self):
        self.playerColors(" ")
