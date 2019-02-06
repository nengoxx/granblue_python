'''
RAID FINDER BOT

'''
from selenium.webdriver.common.keys import Keys
from seleniumrequests import Chrome
from selenium import webdriver

import char_templates
from functions import *
import combat
import images

class Raidfinder(object):
    gbf = ''
    twitter = ''
    joined = False
    timeout = False
    STATE = ''
    current_raidname = ''

    # The class "constructor" - It's actually an initializer
    def __init__(self, gbf):
        log('Creating raid finder bot')
        self.gbf = gbf
        self.active = True
        self.STATE = 0


    '''
    def opentwitter(self):
        options = webdriver.ChromeOptions()
        for cargs in config.CHROME_ARGUMENTS_TWITTER.split():
            options.add_argument(cargs)
            self.twitter = Chrome(chrome_options=options)
            self.twitter.get(config.raidfinder1)
    '''
    def checkjoinraidmenu(self):
        try:
            idtab = self.gbf.find_elements_by_class_name('btn-tabs')[2] #3rd tab
            if idtab.get_attribute("class") == u'btn-tabs active':
                self.STATE = 1
                return 1
        except Exception:
            return 0

    def gotojoinraid(self):
        log('Accessing \'Enter ID\' tab')
        try:
            get_v(self.gbf,config.joinraid)
            wait_until_class('btn-tabs', self.gbf)  #enter id and such tabs
            clickButton('tab-id', self.gbf,2)   #enter id specific tab
            wait_until_class('btn-post-key', self.gbf)  #not neceessary as its there whole time
            idtab = self.gbf.find_elements_by_class_name('btn-tabs')[2] #3rd tab
            if idtab.get_attribute("class") == u'btn-tabs active':
                self.STATE = 1
            checkPopup(self.gbf) #function.py TODO:change all the calls to self.checkPopup() to the one in functions.py
        except Exception:
            log('Exception in gotojoinraid')
            traceback.print_exc()
            self.timeout = True

    def getraidcode(self):
        log('Getting raid code')
        findraidtime = Timer()
        codefound = False
        while not codefound:
            coords = imagesearch(images.join_gbfraiders)#imagesearch(images.now_raidfinder)
            #coords2 =
            #check if we found coords and which one is higher (> y)
            #if coords[0] == 0 or coords2[1] < coords[1]:
                #coords = coords2
            if coords[0] != -1:
                pyautogui.moveTo(coords[0], coords[1], config.mmto[0])
                pyautogui.click(coords[0], coords[1],1,0,button='left')
                codefound = True
                self.STATE = 2
                break

    def joinraid(self):
        log('Pasting raid code')
        try:
            if not self.checkjoinraidmenu():
                #TODO: check if we are in the correct menu
                self.STATE = 0
                return
            wait_until_class('frm-battle-key', self.gbf)
            text_area = self.gbf.find_elements_by_class_name("frm-battle-key")[0]
            #if not (text_area.text == ''): #clear previous text
            text_area.send_keys(Keys.CONTROL, "a")
            text_area.send_keys(Keys.DELETE)
            #text_area.clear()
            text_area.send_keys(Keys.CONTROL, "v")  # or Keys.COMMAND on Mac
            clickButton('btn-post-key', self.gbf)
            #self.checkPopup()
            self.STATE = 3
        except Exception:
            self.STATE = 1

    def checkPopup(self):
        #if wait_until_class('txt-popup-body', self.gbf, config.wait_until_less):
        try:
            if useBerries(self.gbf):
                self.STATE = 3
            title_popup = (self.gbf.find_elements_by_class_name("prt-popup-header")[0]).text
            text_popup = (self.gbf.find_elements_by_class_name("txt-popup-body")[0]).text
            if title_popup == 'エラー' or self.gbf.find_elements_by_class_name("pop-result-assist-raid") or (text_popup in config.poperrs): #error joining popup
                log('Error joining raid, popup')
                #clickButton('btn-usual-ok', self.gbf) #no need if state is set to 0 afterwards
                self.STATE = 0  # could be 0 if we want to relocate or reset to the tab
                return
            elif text_popup == config.poppending:
                log('We got pending battles')
                clearPendingBattles(self.gbf)
                self.STATE = 0
        except Exception:
            self.STATE = 0

    def run(self):
        resetStateTime = Timer()
        while self.active:
            if resetStateTime.check_timeout(config.runDefaultTimeout):
                log('Timeout for raidfinder bot, resetting to initial state...')
                self.gbf.refresh()
                get_v(self.gbf,'http://game.granbluefantasy.jp/#mypage')
                self.STATE = 0
                resetStateTime.reset()
            self.stateSelector(self.STATE)

    def stateSelector(self,state):
        if state == 0: #wrong place, go to join raid tab
            self.joined = False
            self.gotojoinraid()
        elif state == 1: #w8 for the code
            if check_bp(self.gbf) >= config.minBP or config.useBerries:
                self.getraidcode()
        elif state == 2: #input the code
            self.joinraid()
        elif state == 3: #select summon
            try:
                checkUsingBerries(self.gbf)
                ss = SummonSelector(self.gbf)
                ss.select()
                self.current_raidname = ss.raidname
                char_templates.current_raidname = ss.raidname
                self.STATE = 4
            except Exception: #exceptions caused by popups TODO:check others
                #self.STATE = 0
                self.checkPopup()
        elif state == 4: #enter combat
            self.joined = True
            combatBot = combat.make_combatbot(self.gbf)
            if self.current_raidname and self.current_raidname in char_templates.blue_chest_raids:
                combatBot.combatMode = 1
            combatBot.run()
            self.current_raidname = ''
            self.STATE = 0

def make_raidfinder(gbf):
    raidfinder = Raidfinder(gbf)
    return raidfinder
