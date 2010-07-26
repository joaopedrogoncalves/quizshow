import MySQLdb
from random import shuffle
import time

class PerguntasManager():
    def __init__(self,Debug=False, db="codebits2009", user="root"):
        self.Debug = Debug
        self.db = MySQLdb.connect(db=db, user=user, use_unicode=True, passwd="teste")
        self.cursor = self.db.cursor()

    def fetch(self):
        return self.cursor.fetchall()
        
    def query(self, sql):
        if self.Debug:
            print sql
        return self.cursor.execute( sql )

    def _pergunta_query(self, sql):
        count = self.query( sql )
        return Perguntas( self.fetch() ) 

    def todas_as_perguntas(self):
        return self._pergunta_query("SELECT id, grupo, ordem, score, pergunta, opcaoA, opcaoB, opcaoC, opcaoD, opcaoCerta FROM perguntas ORDER BY id")
        
    def perguntas_grupo(self, g):
        return self._pergunta_query("SELECT id, grupo, ordem, score, pergunta, opcaoA, opcaoB, opcaoC, opcaoD, opcaoCerta FROM perguntas WHERE grupo = %d ORDER BY ordem" % (g,) )
        
        
class Perguntas(object):
    """Perguntas class"""
    def __init__(self, perguntas_list):
        self.perguntas_list = perguntas_list
        self.perg_idx = 0
    
    def count(self):
        return len(self.perguntas_list)
        
    def get_pergunta(self, idx):
        if idx < 0 or idx > len(self.perguntas_list):
            raise
        
        self.perg_idx = idx
        return Pergunta( self.perguntas_list[idx] )
        
    def get_next(self):
        self.perg_idx += 1
        if self.perg_idx < len(self.perguntas_list):
            ret = Pergunta(self.perguntas_list[self.perg_idx])
            return ret
        else:
            return False
    
    def perguntas(self):
        return [(i, x[4], x[5:9]) for i, x in enumerate(self.perguntas_list)]


class Pergunta():
    """Pergunta individual"""
    def __init__(self, p):
        self.p = p
        self.id = p[0]
        self.grupo = p[1]
        self.ordem = p[2]
        self.multiplicador = int(p[3])
        self.pergunta = p[4]
        self.resposta = p[5]
        self.options = []
        for x in 5,6,7,8:
            self.options.append([p[x], False, []])
        self.options[ p[9]-1 ][1] = True
        
        shuffle(self.options)
        self.multiplas = self.options

    def add_wrong_player(self, option, player):
        self.options[option][2].append(player)
        
    def wrong_players(option):
        return option[2]    

if __name__ == "__DISABLEDmain__":
    import QuartzManager
    qm = QuartzManager.QuartzManager()
    perg = PerguntasManager(Debug=True)
    pcount = perg.todas_as_perguntas()
    for p_l in perg.perg_list:
        pergunta = Pergunta(p_l)
        
        print pergunta.pergunta
        qm.perguntar(pergunta.pergunta)
        mult = []
        for op in pergunta.options:
            if op[1] == True: mult.append(op)
            else: mult.append([" ", False])
            
        qm.multiplas([x[0] for x in pergunta.options])    
        time.sleep(2)    
        qm.multiplas([x[0] for x in mult])
        time.sleep(2)
    
    
