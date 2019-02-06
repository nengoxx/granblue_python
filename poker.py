'''
POKER BOT

'''
from selenium.webdriver.common.keys import Keys
from seleniumrequests import Chrome
from selenium import webdriver
from functions import *
import combat
import images

#TODO: Finish the poker bot
class Poker(object):
    gbf = ''
    timeout = False
    STATE = ''


    def __init__(self, gbf):
        log('Creating poker bot')
        self.gbf = gbf
        self.active = True
        self.STATE = 0

    def getDoubleUpCard(self):
        card = self.gbf.execute_script('return JSON.stringify(window.doubleUp_card_1)'))
        cardnum = int(card[-1])
        return cardnum

    def getCardToKeep(self):
        cards = self.gbf.execute_script('return JSON.stringify(window.cards_1_Array)'))

    def run(self):
        resetStateTime = Timer()
        get_v(self.gbf, 'http://game.granbluefantasy.jp/#casino/game/poker/200040')
        while self.active:
            if resetStateTime.check_timeout(20*60):
                log('Timeout for poker bot, resetting to initial state...')
                self.gbf.refresh()
                get_v(self.gbf,'http://game.granbluefantasy.jp/#casino/game/poker/200040')
                self.STATE = 0
                resetStateTime.reset()
            self.stateSelector(self.STATE)

    def stateSelector(self,state):
        if state == 0:
            return


def make_poker(gbf):
    poker = Poker(gbf)
    return poker
