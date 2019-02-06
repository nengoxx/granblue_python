'''
QUEST BOT

'''
from selenium.webdriver.common.keys import Keys
from seleniumrequests import Chrome
from selenium import webdriver

import char_templates
from functions import *
import combat

class Questspam(object):
    gbf = ''
    questurl = ''
    joined = False
    timeout = False
    STATE = ''
    questmode = ''
    gwmode = ''
    isnm = False #NM quests spawned

    # The class "constructor" - It's actually an initializer
    def __init__(self, gbf):
        log('Creating quest bot')
        self.gbf = gbf
        self.active = True
        self.STATE = 0
        self.questmode = config.questmode
        self.gwmode = config.gwmode
    
    def checkquestpage(self):
        try:
            if self.questmode == 'test_trial':
                if self.gbf.current_url != config.test_trial:
                    log('Not in quest page')
                    return False
                else:
                    return True
        except Exception:
            log('Exception in checkquestpage')
            return False
     
    def gotoquestpage(self):
        log('Going to the quest page')
        if not self.checkquestpage():
            if self.questmode == 'test_trial': #trial mode
                get_v(self.gbf,config.test_trial)
                if wait_until_class('btn-quest-group-banner', self.gbf):
                    self.STATE = 1
            elif self.questmode == 'gw': #guild war mode
                get_v(self.gbf,config.gw_page)
                if wait_until_class_displayed('prt-player-area', self.gbf):
                    self.STATE = 1
            elif self.questmode == 'sslime': #solo slime(shiny slime) mode
                get_v(self.gbf,config.special_daily)
                if wait_until_id_displayed('tab-normal-quest', self.gbf):
                    self.STATE = 1
            elif self.questmode == 'halo': #angel halo
                get_v(self.gbf,config.special_daily)
                if wait_until_id_displayed('tab-normal-quest', self.gbf):
                    self.STATE = 1
            elif self.questmode == 'trial': #aurora trial
                get_v(self.gbf,config.special_daily)
                if wait_until_id_displayed('tab-normal-quest', self.gbf):
                    self.STATE = 1
            elif self.questmode == 'event_special': #event with special quests
                get_v(self.gbf,config.current_event)
                if wait_until_id_displayed('tab-normal-quest', self.gbf):
                    self.STATE = 1
            elif self.questmode == 'showdown': #sagi showdown
                get_v(self.gbf,config.special_daily)
                if wait_until_id_displayed('tab-normal-quest', self.gbf):
                    self.STATE = 1
            elif self.questmode == 'fav': #favourite quests
                get_v(self.gbf,config.featured_daily)
                if wait_until_class_displayed('btn-favorite', self.gbf):
                    clickButton('btn-favorite', self.gbf)
                    sleep(1)
                    if wait_until_class_displayed('btn-recommend', self.gbf):
                        self.STATE = 1

    def enterFavquest(self):
        log('Entering Favorite quest')
        questlist = self.gbf.find_elements_by_class_name("prt-list-contents")
        for quest in questlist:
            if not quest.is_displayed():  # if its not displayed
                continue
            log('Quest found, selecting 1st quest')
            clickButton('prt-quest-detail', quest)
            self.STATE = 2
            break
        
    def enterTestTrialBattle(self):
        log('Looking for the correct quest')
        #iterate through all the quests and find the dark element one
        clickButton('btn-quest-group-banner', self.gbf)
        quest_list = self.gbf.find_elements_by_class_name("prt-quest-banner")
        for quest in quest_list:
            questid = (quest.find_elements_by_class_name("btn-set-quest")[0]).get_attribute('data-chapter-id')
            #quest ids are from 99001-fire to 99006-dark
            if questid != "99006":
                continue
            log('Quest found')
            clickButton('btn-set-quest', quest)
            self.STATE = 2
            
    def enterSSlime(self):
        log('Entering Shiny Slime Search quest')
        questlist = self.gbf.find_elements_by_class_name("prt-list-contents")
        for quest in questlist:
            if not quest.is_displayed(): #if its not displayed
                continue
            questitle = quest.find_elements_by_class_name("txt-quest-title")
            if not questitle or questitle[0].text != 'Shiny Slime Search!': #if its the quest we're looking for
                continue
            #selectbtn = quest.find_elements_by_class_name("btn-stage-detail")
            log('Quest found')
            clickButton('btn-stage-detail',quest)
            if not wait_until_class_displayed('btn-set-quest', self.gbf):
                #Select button not clicked or quest option not shown
                return
            break
            
        #quest selected, now selecting the correct mode: data-quest-id="400181"
        #iterate through the buttons instead because the banners don't have the data-quest-id attribute
        questoptions = self.gbf.find_elements_by_class_name("btn-set-quest")#prt-quest-banner")
        for option in questoptions:
            if not option.is_displayed():
                continue
            if not option or option.get_attribute('data-quest-id') != "400151": 
                #id changes from weekly to weekend version: week-400181, weekends-400151
                #str: Shiny Slime Search!\nAP-30
                continue
            log('Correct quest option found')
            if clickButton(option,self.gbf,4): #'btn-set-quest',option):
                self.STATE = 2
            break

    def enterAH(self):
        log('Entering Angel Halo quest')
        questlist = self.gbf.find_elements_by_class_name("prt-list-contents")
        for quest in reversed(questlist): #reversed to get the nm version first since spawns below
            if not quest.is_displayed():  # if its not displayed
                continue
            questitle = quest.find_elements_by_class_name("txt-quest-title")
            if questitle and questitle[0].text == 'Dimension Halo':
                #quest id:510051
                get_v(self.gbf, 'http://game.granbluefantasy.jp/#mypage')
                self.STATE = 0
                sendTelegramMsg('Angel Halo NM Spawned!')
                switchPause(True)
                checkPause()
                log('Angel Halo NM Spawned!')
                #input('Angel Halo NM Spawned!')
                return
            if not questitle or questitle[0].text != 'Angel Halo':
                continue
            # selectbtn = quest.find_elements_by_class_name("btn-stage-detail")
            log('Quest found')
            self.gbf.execute_script("arguments[0].scrollIntoView();", quest)
            clickButton('btn-stage-detail', quest)
            if not wait_until_class_displayed('pop-quest-detail', self.gbf):
                # Select button not clicked or quest option not shown
                return
            break

        # quest selected, now selecting the correct mode: data-quest-id="400181"
        # iterate through the buttons instead because the banners don't have the data-quest-id attribute
        questoptions = self.gbf.find_elements_by_class_name("btn-set-quest")  # prt-quest-banner")
        for option in questoptions:
            if not option.is_displayed():
                continue
            if not option or option.get_attribute('data-quest-id') != "510031":
                continue
            log('Correct quest option found')
            if clickButton(option, self.gbf, 4):
                self.STATE = 2
            break

    def enterSpecialEvent(self):
        log('Entering Event quest')
        questlist = self.gbf.find_elements_by_class_name("btn-stage-detail")
        for quest in questlist:
            if not quest.is_displayed():  # if its not displayed
                continue
            if quest and quest.get_attribute('data-title') == "Nihilith: The Finale"\
                    and quest.get_attribute('data-group') == '3':
                log('Event NM Spawned!')
                if not config.donm:
                    get_v(self.gbf, 'http://game.granbluefantasy.jp/#mypage')
                    self.STATE = 0
                    sendTelegramMsg('Event NM Spawned!')
                    input('Event NM Spawned!')
                    #log('Event NM Spawned!')
                    return
                self.isnm = True
                clickButton(quest, self.gbf, 4)
                if not wait_until_class_displayed('pop-quest-detail', self.gbf):
                    # Select button not clicked or quest option not shown
                    return
                break
            if not quest or quest.get_attribute('data-title') != "Ward Off Nihilith's Power!":
                continue
            log('Quest found')
            clickButton(quest, self.gbf,4)
            if not wait_until_class_displayed('pop-quest-detail', self.gbf):
                # Select button not clicked or quest option not shown
                return
            break

        # quest selected, now selecting the correct mode: data-quest-id="400181"
        # iterate through the buttons instead because the banners don't have the data-quest-id attribute
        questoptions = self.gbf.find_elements_by_class_name("btn-set-quest")  # prt-quest-banner")
        for option in questoptions:
            if not option.is_displayed():
                continue
            if not option or (not self.isnm and option.get_attribute('data-quest-id') != "729941")\
                    or (self.isnm and option.get_attribute('data-quest-id') != "729991"):
                continue
            log('Correct quest option found')
            if clickButton(option, self.gbf, 4):
                self.STATE = 2
            break

    def enterTrial(self):
        log('Entering Trial quest')
        questlist = self.gbf.find_elements_by_class_name("prt-list-contents")
        for quest in reversed(questlist): #reversed to get the nm version first since spawns below
            if not quest.is_displayed():  # if its not displayed
                continue
            questitle = quest.find_elements_by_class_name("txt-quest-title")
            if not questitle or questitle[0].text != 'The Aurora Trial':
                continue
            # selectbtn = quest.find_elements_by_class_name("btn-stage-detail")
            log('Quest found')
            self.gbf.execute_script("arguments[0].scrollIntoView();", quest)
            clickButton('btn-stage-detail', quest)
            if not wait_until_class_displayed('pop-quest-detail', self.gbf):
                # Select button not clicked or quest option not shown
                return
            break

        # quest selected, now selecting the correct mode: data-quest-id="400181"
        # iterate through the buttons instead because the banners don't have the data-quest-id attribute
        questoptions = self.gbf.find_elements_by_class_name("btn-set-quest")  # prt-quest-banner")
        for option in questoptions:
            if not option.is_displayed():
                continue
            if not option or option.get_attribute('data-quest-id') != "599851":
                continue
            log('Correct quest option found')
            if clickButton(option, self.gbf, 4):
                self.STATE = 2
            break

    def enterShowdown(self):
        log('Entering Showdown quest')
        questlist = self.gbf.find_elements_by_class_name("prt-list-contents")
        for quest in reversed(questlist): #reversed to get the nm version first since spawns below
            if not quest.is_displayed():  # if its not displayed
                continue
            questitle = quest.find_elements_by_class_name("txt-quest-title")
            if not questitle or questitle[0].text != 'Sagittarius Showdown':
                continue
            # selectbtn = quest.find_elements_by_class_name("btn-stage-detail")
            log('Quest found')
            self.gbf.execute_script("arguments[0].scrollIntoView();", quest)
            clickButton('btn-stage-detail', quest)
            if not wait_until_class_displayed('pop-quest-detail', self.gbf):
                # Select button not clicked or quest option not shown
                return
            break

        # quest selected, now selecting the correct mode: data-quest-id="400181"
        # iterate through the buttons instead because the banners don't have the data-quest-id attribute
        questoptions = self.gbf.find_elements_by_class_name("btn-set-quest")  # prt-quest-banner")
        for option in questoptions:
            if not option.is_displayed():
                continue
            if not option or option.get_attribute('data-quest-id') != "500211":
                continue
            log('Correct quest option found')
            if clickButton(option, self.gbf, 4):
                self.STATE = 2
            break
                

    def enterGwEX_plus(self):
        log('Entering gw Ex+ quest')
        ex_plus_banner = find_visible_class(self.gbf,'img-btn-raid')
        for banner_img in ex_plus_banner:
            if banner_img.get_attribute('alt') == 'btn_ex_raid':
                correct_banner = banner_img
                break
        self.gbf.execute_script("arguments[0].scrollIntoView();", correct_banner)
        clickButton(correct_banner,self.gbf,4)
        ex_plus_q_banner = find_visible_class(self.gbf, 'img-quest')
        for banner_img in ex_plus_q_banner:
            if banner_img.get_attribute('alt') == '2040066000_ex':
                correct_banner = banner_img
                clickButton(correct_banner, self.gbf, 4)
                self.STATE = 2
                return
        self.STATE = 0

    def enterGwNM90(self):
        log('Entering gw NM90 quest')
        ex_plus_banner = find_visible_class(self.gbf,'img-btn-raid')
        for banner_img in ex_plus_banner:
            if banner_img.get_attribute('alt') == 'btn_hell_raid_1':
                correct_banner = banner_img
                break
        self.gbf.execute_script("arguments[0].scrollIntoView();", correct_banner)
        clickButton(correct_banner,self.gbf,4)

        #THIS IS FOR WHEN THERES ONLY 1 NM MODE
        only_90_ok_button = find_visible_class(self.gbf, 'btn-offer')
        if only_90_ok_button:
            clickButton(only_90_ok_button[0], self.gbf, 4)
            self.STATE = 2
            return
        #THIS DOESNT WORK IF ITS DAY 1 SINCE THERES ONLY 1 RAID
        ex_plus_q_banner = find_visible_class(self.gbf, 'img-quest')
        for banner_img in ex_plus_q_banner:
            if banner_img.get_attribute('alt') == '2040119000_ex':
                correct_banner = banner_img
                clickButton(correct_banner, self.gbf, 4)
                self.STATE = 2
                return

        self.STATE = 0
                
                
    def run(self):
        resetStateTime = Timer()
        while self.active:
            if resetStateTime.check_timeout(config.runDefaultTimeout):
                log('Timeout for quest bot, resetting to initial state...')
                get_v(self.gbf, 'http://game.granbluefantasy.jp/#mypage')
                self.STATE = 0
                resetStateTime.reset()
            self.stateSelector(self.STATE)

    def stateSelector(self,state):
        if state == 0:
            self.joined = False
            self.gotoquestpage()
        elif state == 1:
            if self.questmode == 'test_trial':
                self.enterTestTrialBattle()
            elif self.questmode == 'gw':
                if self.gwmode == 'ex':
                    config.minap = 40
                    self.enterGwEX_plus()
                elif self.gwmode == 'nm':
                    config.minap = 30
                    self.enterGwNM90()
            elif self.questmode == 'sslime':
                self.enterSSlime()
            elif self.questmode == 'halo':
                config.minap = 10
                self.enterAH()
            elif self.questmode == 'trial':
                config.minap = 20
                self.enterTrial()
            elif self.questmode == 'event_special':
                config.minap = 30
                self.enterSpecialEvent()
            elif self.questmode == 'showdown':
                config.minap = 15
                self.enterShowdown()
            elif self.questmode == 'fav':
                config.minap = 22
                self.enterFavquest()
        elif state == 2: #select summon
            try:
                checkUsingElixirs(self.gbf)
                ss = SummonSelector(self.gbf)
                ss.select()
                self.STATE = 3
            except Exception: #exceptions caused by popups TODO:check others
                log('Exception at state 2')
                #check if somehow we exited from a quest and we are already in combat
                if self.gbf.find_elements_by_class_name("btn-attack-start"):
                    self.STATE = 3
                    return
                if checkPopup(self.gbf):
                    return
                #self.STATE = 0
        elif state == 3: #enter combat
            self.joined = True
            combatBot = combat.make_combatbot(self.gbf)
            if self.questmode == 'test_trial':
                char_templates.skillCombosType = self.gwmode
                combatBot.combatMode = 1
                combatBot.dismissInitialDialog()
            elif self.questmode == 'sslime':
                combatBot.combatMode = 2
            elif self.questmode == 'gw':
                char_templates.skillCombosType = self.gwmode
                combatBot.combatMode = 1
            if self.isnm:
                char_templates.skillCombosType = config.gwmodes[1] #nm
                combatBot.combatMode = 1
                self.isnm = False
            combatBot.run()
            self.STATE = 0

def make_questbot(gbf):
    questbot = Questspam(gbf)
    return questbot
