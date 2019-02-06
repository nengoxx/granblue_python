'''
COOP BOT

'''
from functions import *
import images
import combat

class Coop(object):
    gbf = ""
    STATE = ''

    # The class "constructor" - It's actually an initializer
    def __init__(self, gbf):
        log('Initializing coop bot...')
        self.gbf = gbf
        self.inroom = False
        self.active = True
        self.STATE = 0


    def testAttack(self):
        if self.gbf.find_elements_by_class_name("btn-attack-start"):
            self.inroom = True  #exit the loop if we're attacking
            return True
        return False
    
    def gotoCoop(self):
        log('Going to coop room...')
        get_v(self.gbf,config.coop)
        self.STATE = 1

    def createTorch(self):
        if self.testAttack():
            self.STATE = 2
            return
        get_v(self.gbf,config.torch)
        #wait_until_class('btn-entry-room', self.gbf)
        clickButton('btn-entry-room', self.gbf) #create a room ok button
        sleep(config.wait_until_less)
        self.STATE = 1

    def selectCoopParty(self):
        log('Selecting coop party...')
        wait_until_class('btn-make-ready-large', self.gbf)
        #but = self.gbf.find_elements_by_class_name('btn-make-ready-large')
        clickButton('btn-make-ready-large', self.gbf)  # select party
        clickButton('btn-usual-ok', self.gbf) #ok party

    def getRoomState(self):
        if self.testAttack():
            self.STATE = 2
            return
        #w8 till we are inside of the room
        wait_until_class('btn-make-ready-large', self.gbf)
        #wait_until_class('btn-quest-start', self.gbf)
        if not self.gbf.find_elements_by_class_name('btn-quest-start'):
           self.inroom = False
           self.STATE = 0
           raise Exception
        self.inroom = True

        selectPartyNotReady = self.gbf.find_elements_by_class_name('not-ready')
        #startDisabled = self.gbf.find_elements_by_class_name("disable") #4elements
        if selectPartyNotReady:
            self.selectCoopParty()
        #startDisabled = self.gbf.find_elements_by_class_name("disable") #4elements
        startEnabled = self.gbf.find_elements_by_class_name("se-quest-start")
        startEnabled2 = self.gbf.find_elements_by_class_name("btn-execute-ready")
        startEnabled_host = self.gbf.find_elements_by_class_name("btn-quest-start")
        if startEnabled_host and not config.user_main:
            if self.gbf.find_elements_by_class_name("btn-quest-start") and 'disable' in (self.gbf.find_elements_by_class_name("btn-quest-start")[0]).get_attribute("class"):
               log('Refreshing coop room...')
               clickButton('btn-members-refresh', self.gbf)
        if not selectPartyNotReady and (startEnabled or startEnabled2):
            if startEnabled:
                log("Starting coop quest... 'btn-quest-start'")
                clickButton('btn-quest-start', self.gbf)  # quest start
                sleep(2)
                clickButton('btn-quest-start', self.gbf)
                self.STATE = 2
            else:
                log("Starting coop quest... 'btn-execute-ready'")
                clickButton('btn-execute-ready', self.gbf)
                sleep(2)
                clickButton('btn-execute-ready', self.gbf)
                self.STATE = 2

    def run(self):
        self.inroom = False
        while self.active:
            self.stateSelector(self.STATE)

    def stateSelector(self,state):
        if state == 0:
            self.gotoCoop()
        elif state == 1:
            try:
                self.getRoomState()
            except Exception:
                if not self.inroom:
                    self.STATE = 0
                    #self.createTorch()
        elif state == 2:
            checkUsingElixirs(self.gbf)
            combatBot = combat.make_combatbot(self.gbf)
            if config.user_main:
                combatBot.combatMode = 2
            combatBot.run()
            self.inroom = False
            self.STATE = 0


def make_coopbot(gbf):
    coopBot = Coop(gbf)
    if not config.user_main:#use pots if its the alt hosting slimes
        config.usePots = True
    return coopBot




