import os, re
from IPython import ColorANSI

class ConsoleManager():
    """Terminal input/output"""
    def __init__(self):
        self.isNumber = re.compile(r"^\d+$").match
        self.Color = ColorANSI.TermColors()
        pass
    
    def yellow(self, str):
        return self.Color.Yellow + str + self.Color.Normal
        
    def ask(self, texto):
        """ask a question on terminal"""
        try:
            return raw_input( self.yellow( "%s: " % (texto,)))
        except KeyboardInterrupt:
            print
            return self.ask(texto)
        
    def ask_options(self, text, options):
        """Expect for a value from several options"""
        ret = ""
        while ret not in options:
            ret = self.ask(text)
        return ret

    def ask_int(self, texto):
        """Ask for an integer"""
        inp = ""
        while not self.isNumber(inp):
            inp = raw_input( self.yellow( "%s: " %(texto,) ) )
        return int(inp)

    def clear(self):
        os.system('clear')
        
    def printc(self, str):
        print self.Color.Green + str + self.Color.Normal
        