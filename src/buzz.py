import socket, time, csv, cascata
import sys, os, re
import sys
import time
import serial
from BuzzManager import BuzzManager



#arduino = serial.Serial("/dev/cu.usbserial-A7006vJk")
arduino = serial.Serial("/dev/cu.Arrogantbastardale-Blue-1")

class SoundManager():
    def __init__(self):
        self.pSound = [True]
        for x in range(1,5):
            self.pSound.append(NSSound.alloc())
            print "Loading Player %d sound." %(x,)
            self.pSound[x].initWithContentsOfFile_byReference_("%s/p%d.mp3" % (sound_path, x), True)
            
    def play(self, player):
        s = self.pSound[player]
        s.setCurrentTime_(0)
        s.play()


import PyHID

        


class Broadcast():
    def __init__(self):
        self.dir_perguntas = '/Users/joaop/Dropbox/quiz/data/2008/'                
        self.perguntas = self.get_nivel_perguntas() 
        self.n_cascatas = 6
        self.start_sockets()
        self.check_cascata()
        
        self.buzz  = BuzzManager()
        self.sound = SoundManager()
        
        print "%d perguntas carregadas." %(len(self.perguntas), )
        print

        
    def start(self):
        self.ask("Iniciar cascata? ")
        self.pergunta_actual = 0
        self.perguntar_cascata()
        

    def perguntar_cascata(self):
        pergunta_actual = self.pergunta_actual
        pergunta = self.perguntas[pergunta_actual]
        c_info = self.cascata_info()
        
        os.system('clear')

        print "Pergunta #%d" %(pergunta_actual +1)
        print c_info
        print
        print len(pergunta[1])
        print
        ask = self.ask(pergunta[1] + "\n\n \t'ok' - enviar pergunta - \n\t's' ou 'a', per. Seguinte/Snterior, \n\t'r' - Reescrever pergunta, \n\t'm' Saltar de pergunta\n\n")
        if ask == 'r':
            pergunta[1] = self.ask("Texto da pergunta? ")
        if ask == 'ok':
            self.perguntar(pergunta[1])
            self.status( c_info )
            self.counterOne()
            print "\n\n\nRelogio acabou para pergunta directa\n\n\
            n"
            ask = self.ask("Avancar para opcoes multiplas? (s/N)")
            if ask == 's':
                self.counterMultiple()
            
            self.pergunta_actual = self.pergunta_actual + 1     
            try:
                raw_input("Carregar em Enter para avancar nas perguntas.\n")
            except KeyboardInterrupt:
                pass
                
        elif ask == 's':
            self.pergunta_actual = self.pergunta_actual +1
        elif ask == 'a':
            self.pergunta_actual = self.pergunta_actual -1
        if ask == 'm':
            self.pergunta_actual = int(self.ask("Numero da Pergunta?"))       
        return self.perguntar_cascata()
    
    def cascata_info(self):
        pergunta_actual = self.pergunta_actual 
        self.set_cascata_status(pergunta_actual)
        
        print self.n_equipas
        print self.equipa_actual
        return ("%da Cascata %s, Equipa #%d") % \
            (self.cascata_count, self.tipo_cascata, self.n_equipas[self.equipa_actual]  )
        
    
    def set_cascata_status(self, n):
        pergunta_actual = n
        equipas = self.equipas
        tipos_cascatas      = ['Ascendente', 'Descendente']
        self.numero_cascata = pergunta_actual / equipas
        self.equipa_actual  = pergunta_actual % equipas 
        
        self.tipo_cascata   = tipos_cascatas[ self.numero_cascata % 2]
        self.cascata_count  = ((pergunta_actual/equipas)+2)/2
    
    def ask_equipas(self):
        n_equipas = self.ask("Numeros das %d equipas do Nivel? " % (self.equipas))
        n_equipas = [int(x) for x in re.split(',\s*', n_equipas)]
        
        if len(n_equipas) != self.equipas:
            print "Numero errado de equipas. %d, precisamos de %d." \
                  % (len(n_equipas), self.equipas)
            return self.ask_equipas()
        return n_equipas        
        

    # Criar valores para a cascata, com base no nivel e numero  de perguntas.
    def check_cascata(self):
        self.numero_perguntas = len(self.perguntas)
        niveis = [0,15,10,6]
        self.equipas = niveis[self.nivel]
        if self.nivel == 1:
            self.n_equipas = [x+1 for x in range(self.equipas)]
        else:
            self.n_equipas =  self.ask_equipas()
        
        numero_perguntas = self.equipas * 6
        print "Nivel %d tem %d perguntas, %d equipas" \
            % (self.nivel, numero_perguntas, self.equipas) 
        
        if numero_perguntas != self.numero_perguntas:
            print "Numero errado de Perguntas!"
            sys.exit(0)

        
    def start_sockets(self):
        broadcast_host = '127.0.0.1'
        self.sPergunta = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sRelogio = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sMultiplas = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                
        self.sPergunta.connect((broadcast_host, 50000))
        self.sRelogio.connect((broadcast_host, 51000))
        self.sMultiplas.connect((broadcast_host, 52000))

    def get_nivel_perguntas(self):
        self.nivel = int(self.ask("Nivel da Cascata? "))
        ficheiro = "%s/final_nivel%d.txt" % (self.dir_perguntas, self.nivel)
        try:
            os.stat(ficheiro)
            return self.get_perguntas(ficheiro)
        except OSError:
            print "%s nao existe" %(ficheiro,)
            return self.get_nivel_perguntas()
            
    def get_perguntas(self, ficheiro):
        cread = csv.reader(open(ficheiro, "rb"), dialect="excel")
        perguntas = []
        for row in cread:
               if len(row) < 4 : continue
               perguntas.append([row[0], row[1]])
        return perguntas
               
    def ask(self,texto):
            return raw_input(texto)


    def utf32encode(self, s):
        s = s.encode('utf-16be')
        ret = ''
        i= 0
        while i < len(s):
            ret += '\0\0' + s[i:i+2]
            i += 2
        return ret

    def display(self, socket, string):
            socket.send(self.utf32encode(string))
            
    def perguntar(self, texto):
        self.display(self.sPergunta, texto)   

    def relogio(self, texto):
        self.display(self.sRelogio, texto)
    
    def status(self, texto):
        self.display(self.sMultiplas, texto)

    def clear(self):
        self.perguntar(" ")
        self.relogio(" ")
        self.status(" ")
    
    def showPlayerButtons(self, ev):
        """Show buttons pressed in order"""
        bp = self.player_button_pool
        if ev.player not in bp[0]:
            player_str = "JOGADOR %d" % ev.player
            
            # Print timestamp against first player
            if bp[2]:
                player_str += " (%.3f seg)" % (ev.timestamp - bp[2])
            else:
                arduino.write( str(ev.player) )
                bp[2] = ev.timestamp
                
            bp[1].append(player_str)
            self.status( "|".join(bp[1]) )
            self.sound.play( ev.player )
            self.player_button_pool = bp
            
        
    
    def counterOne(self, t=5):
        self.player_button_pool = [{},[], 0]
        # Make sure event poll is empty
        while self.buzz.poll(False): pass
        
        try:
            while t >= 0:
                t -= 1
                self.relogio( "Directa 0:%.2d" % (t,))
                
                for x in range(10):
                    time.sleep(0.1)
                    ev = self.buzz.poll(True)
                    if ev and ev.color == "RED":
                        self.showPlayerButtons(ev)
                        self.relogio(" ")
                        # Clear all other button requests
                        # if there's more than one close player,
                        # show them all.
                        for x in range (15):
                            time.sleep(0.1)
                            ev = self.buzz.poll(False)
                            while ev:
                                if ev and ev.pressed:
                                    self.showPlayerButtons(ev)
                                    ev = self.buzz.poll(False) 
                        # clean remaining calls
                        return                        

            for x in range(10):
                self.relogio( "TEMPO!!!")
                time.sleep(0.25)
                self.relogio(" ")

        except KeyboardInterrupt:
            self.relogio(" ")


if __name__ == '__main__':
    b = Broadcast()
    b.start()
