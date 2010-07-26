from AppKit import NSSound
sound_path = "/Users/joaop/Code/Python/codebits/sounds"
sound_path = "/Users/joaop/Dropbox/quiz/Codebits2009/sounds"

class SoundManager():
    def __init__(self):
        self.pSound = [True]
        for x in range(1,5):
            self.pSound.append(NSSound.alloc())
            print "Loading Player %d sound." %(x,)
            self.pSound[x].initWithContentsOfFile_byReference_("%s/p%d.mp3" % (sound_path, x), True)
        print "Loading Error and Timeout sounds"    
        self.pSoundError = NSSound.alloc()
        self.pSoundError.initWithContentsOfFile_byReference_("%s/erro.mp3" % (sound_path,), True)
        self.pSoundTimeOut = NSSound.alloc()
        self.pSoundTimeOut.initWithContentsOfFile_byReference_("%s/timeout.mp3" % (sound_path,), True)
        
    
    def _play(self, s_ref):
        s_ref.setCurrentTime_(0)
        s_ref.play()
        
    def play(self, player):
        self._play(self.pSound[player])
    
    
    def playTimeOut(self):
        self._play(self.pSoundTimeOut)
        
    def playError(self):
        self._play(self.pSoundError) 


sm = SoundManager()

