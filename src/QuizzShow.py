import time, random

from SoundManager import SoundManager
from QuartzManager import QuartzManager
from ConsoleManager import ConsoleManager
from PerguntasManager import PerguntasManager
#from Arduino import Arduino
from QuartzScoreManager import QuartzScoreManager
from BuzzManager import BuzzManager


class GameController():
    """GameController for Quizz Show"""
    def __init__(self):
        self.sm = SoundManager()
        self.qm = QuartzManager()
#        self.am = Arduino()
        self.am = QuartzScoreManager()
        self.bm = BuzzManager()
        self.pm = PerguntasManager()
        self.cm = ConsoleManager()
        self.scores = [0, 0, 0, 0]
        self.player_button_pool = []

    def begin(self):
        """Game Begin"""
        n = self.cm.ask_int("Qual o grupo de perguntas?")
        self.perguntas = self.pm.perguntas_grupo( n )
        for x in self.perguntas.perguntas(): 
            self.cm.printc( "%d: %s %s" % x)
        
        idx = 0
        print self.scores
        
        idx = self.cm.ask_int("Iniciar em que pergunta (0)?")
        pergunta = self.perguntas.get_pergunta( idx )

        if idx > 0:
            cur_score = self.cm.ask("Current score - (0,0,0,0): ")
            if len(cur_score) > 4:
                self.scores = [int(x) for x in cur_score.split(",")]
                print self.scores


        while pergunta:
            self.ask_pergunta( pergunta )
            pergunta = self.perguntas.get_next()
            
        self.am.lights_off()

    def show_scores(self):
        s = []
        i = 1
        for score in  self.scores:
            if score == 1 : 
                plural = ""
            else : 
                plural = "s"
            s.append("Equipa %d - %d ponto%s" % (i, score, plural))
            i += 1
        self.qm.multiplas(s)
        
        
    def ask_pergunta(self, pergunta):
        self.cm.clear()
        self.am.lights_off()
        self.qm.pontuacao( self.scores )
        print self.scores

        self.qm.multiplas(" ")

        self.cm.printc( "%s: %s" % (pergunta.ordem, pergunta.pergunta) )
        self.qm.perguntar("   Codebits Quiz Show   ")


        # Show scores only if any team has already scored.
        if [x for x in self.scores if x > 0]:
            self.show_scores()
        
        ret = self.cm.ask_options("Enviar (S/N)?", ("S", "N"))
        if ret == "N": return

        self.bm.clear_button_poll()        
        self.qm.multiplas(" ")
           
        player= self.timer_red_buzz(pergunta)
        
        if player != None:
            ret = self.cm.ask_options("Red Buzz %s right? (S/N/(R)etry)" % player, ("S", "N", "I") )
            self.qm.perguntar(pergunta.pergunta)
            
            if ret == "S": 
                time.sleep(5)
                self.scores[player-1] += (2 * pergunta.multiplicador )
                self.qm.pontuacao( self.scores )
                return
            if ret == "R":
                return self.ask_pergunta(pergunta)
                
        self.cm.ask_options("Enviar Multiplas? (S)", ("S") )
        self.timer_multiplas( pergunta, player )
            
    
    def timer_multiplas(self, pergunta, player=None, t=30):
        """controls clock and checks for multiple choice
        events from the buzz"""
        
        if player != None:
            player = int(player)
    
        self.am.lights_off()        
        self.bm.clear_button_poll()
        self.clear_player_button_pool()
        
        self.cm.printc(" ")
        self.cm.printc("Waiting for Multiplas.")
        self.qm.multiplas( [x[0] for x in pergunta.multiplas] )
        
        playersStatus = self.am.get_players_from_int(0)
        
        playerHasResponded = []
        
        if player:
            print "Ignoring %d" %(player,)
            playerHasResponded.append( player )
            self.am.set_player_wrong( player )
            
        try:
            while t >= 0:
                self.qm.relogio( "0:%.2d" % (t,) )
                t -= 1
                if len(playerHasResponded) == 4:
                    self.qm.relogio(" ")
                    break
                
                for x in range(10):
                    time.sleep(0.1)
                    ev = self.bm.poll(True)
                    # No red buttons, nor the player who failed.
                    if ev:
                        if ev.color == "RED" or ev.player in playerHasResponded:
                            continue
                            
                        print ev.multi

                        if pergunta.options[ev.multi][1] == True:    

                            self.sm.play( ev.player )
                            self.am.set_player_right( ev.player )
                            self.scores[ev.player-1] += (1 * pergunta.multiplicador)
                            self.qm.pontuacao( self.scores )
                            
                            
                            print ev.player
                        else:
                            pergunta.add_wrong_player(ev.multi, ev.player)
                            self.sm.playError()
                            self.am.set_player_wrong( ev.player )
                            
                            playersStatus[ev.player - 1][1] = True
                            
                            print "FAIL"
                            print ev.player
                            
                        playerHasResponded.append(ev.player)    
                                            
        except KeyboardInterrupt:
            self.qm.relogio(" ")
        
        # Timeout. No one pressed the Buzz.
        if t < 1:
            self.sm.playTimeOut()
        self.cm.ask_options(" Mostrar resposta certa? (S)", ["S"])
        self.show_correct_answer(pergunta.options)
        self.cm.ask_options("Continuar? (S)", ["S"])


    def show_correct_answer(self, options):
        l = []
        for x in options:
            if x[1] == True: l.append(x[0])
            else:
                l_str = ''
                for p in x[2]:
                    l_str += "(%s) " %(p) 
                if len(l_str) > 2:
                    l_str = "X " + l_str
                    l_str += " %s" %(x[0])
                    l.append (l_str)
                else: 
                    l.append( " ")
        self.qm.multiplas( l )

    def timer_red_buzz(self, pergunta, t=20, has_been_asked=False):
        """controls clock and checks for buzz events
           t is the start time for countdown."""

        # Watch for events during the timer and during the time that the presenter
        # is reading the question.
        if has_been_asked == True:
            self.qm.multiplas(" ")
            self.qm.perguntar( pergunta.pergunta )
        else:
            self.clear_player_button_pool()
            self.bm.clear_button_poll()
            self.qm.perguntar("Podes responder com o botao vermelho.")
            if pergunta.multiplicador > 1:
                self.qm.multiplas(["Score Multiplier active: %dx" %(pergunta.multiplicador), "Straight answer is worth %d points." % (pergunta.multiplicador*2), "", ""])
               
        self.cm.printc(" ")
        self.cm.printc(pergunta.resposta )
        
        self.cm.printc("Waiting RED Buzz.")
        
        try:
            someone_answered = False
            while t > 0:

                if has_been_asked == True:
                    t -= 1
                    self.qm.relogio( "0:%.2d" % (t,) )
                else:
                    self.qm.relogio(" ")
                        
                for x in range(10):
                    time.sleep(0.1)
                    

                    if self.bm.mobile:
                        ev = self.bm.mobile.poll()
                        if ev and ev[1] == 1:
                            if has_been_asked == False:
                                raise KeyboardInterrupt
                                
                    ev = self.bm.poll(True)
                    if ev and ev.color == "RED":
                        print "GOT %d" % (ev.player,)
                        self.show_player_buttons(ev)    
                        self.qm.relogio(" ")
                        someone_answered = True
                        # Clear all other button requests
                        # if there's more than one close player,
                        # show them all.
                        for x in range (20):
                            time.sleep(0.1)
                            ev = self.bm.poll(False)
                            while ev:
                                if ev and ev.pressed:
                                    self.show_player_buttons(ev)
                                ev = self.bm.poll(False) 
                                
                            # Return who won.
                            return self.player_button_pool[3]
                            
        except KeyboardInterrupt:
            self.qm.relogio(" ")
            if has_been_asked == False:
                if someone_answered == True:
                    return self.player_button_pool[3]
                return self.timer_red_buzz( pergunta, 20, True)
                

        # Timeout. No one pressed the Buzz.
        self.sm.playTimeOut()
        self.cm.ask_options("Timeout. Continuar? (S)", ["S"])
        return None


    def clear_player_button_pool(self):
        self.player_button_pool = [{},[], 0,-1]

    def show_player_buttons(self, ev):
        """Show buttons pressed in order"""
        
        bp = self.player_button_pool
        
        if ev.player not in bp[0]:
            player_str = "TEAM %d" % ev.player
            
            # Print timestamp against first player
            if bp[2]:
                player_str += " (%.3f seg)" % ((ev.timestamp + (float(random.randint(1,10)) / 1000)) - bp[2])
            else:
                self.am.set_player_light(ev.player)
                bp[2] = ev.timestamp
                bp[0][ev.player] = True
                bp[3] = ev.player
                
            bp[1].append(player_str)
            for x in bp[1]:
                print x
            
            self.qm.multiplas( bp[1] )
            self.sm.play( ev.player )
            self.player_button_pool = bp
        
if __name__ == '__main__':
    game = GameController()
    game.begin()
