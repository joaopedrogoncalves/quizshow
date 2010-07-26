import socket

class QuartzManager():
    """docstring for QuartzManager"""
    def __init__(self):
        self.start_sockets()
        self.clear()

    def start_sockets(self):
        broadcast_host = '127.0.0.1'

        self.sPergunta  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sPergunta1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sPergunta2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.sRelogio  =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.sMultiplas1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                
        self.sMultiplas2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)      
        self.sMultiplas3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)      
        self.sMultiplas4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)      

        self.sPontuacao = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                  
        
        self.sPergunta.connect((broadcast_host, 50000))
        self.sPergunta1.connect((broadcast_host, 50010))
        self.sPergunta2.connect((broadcast_host, 50020))

        self.sRelogio.connect((broadcast_host, 51000))

        self.sMultiplas1.connect((broadcast_host, 52000))
        self.sMultiplas2.connect((broadcast_host, 52010))
        self.sMultiplas3.connect((broadcast_host, 52020))
        self.sMultiplas4.connect((broadcast_host, 52030))

        self.sPontuacao.connect((broadcast_host, 53000))


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
        text_len = len(texto) / 3
        if len(texto) > 50:
            self.display(self.sPergunta, texto[0:text_len])   
            self.display(self.sPergunta1, texto[text_len:text_len*2])   
            self.display(self.sPergunta2, texto[text_len*2:])   
        else:            
            self.display(self.sPergunta, texto)   
            self.display(self.sPergunta1, " ")   
            self.display(self.sPergunta2, " ")   
            

    def relogio(self, texto):
        self.display(self.sRelogio, texto)
        
    def pontuacao(self, score):
        """score e' uma lista com 4 valores."""
        self.display(self.sPontuacao, "T1: %.2d T2: %.2d T3: %.2d T4:%.2d" % tuple(score) )

    def multiplas(self, perguntas):
        if perguntas == " ":
            # clear
            self.display(self.sMultiplas1, " ")
            self.display(self.sMultiplas2, " ")
            self.display(self.sMultiplas3, " ")
            self.display(self.sMultiplas4, " ")
        else:
            perguntas = list(perguntas)
            if len(perguntas) < 4:
                while len(perguntas) < 4:
                    perguntas.append(" ") 
            self.display(self.sMultiplas1, perguntas[0])
            self.display(self.sMultiplas2, perguntas[1])
            self.display(self.sMultiplas3, perguntas[2])
            self.display(self.sMultiplas4, perguntas[3])
        
        
    def clear(self):
        self.perguntar("    ")
        self.relogio(" ")
        self.multiplas(" ")
        self.display(self.sPontuacao, " ")
