# from pynput import keyboard
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException

import char_templates
from libs.imagesearch.imagesearch import *
import random
from os import makedirs, path
from time import time as time_now
from time import sleep, strftime
import pyautogui
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False
import config
from tabman import *
from timer import *
from telegram_bot import *
import traceback
import pathlib
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


'''
LOGS & DEBUG
'''
def log(message):
    '''Prints to console and outputs to log file'''
    if message == config.lastmsg: #dont spam
        return
    config.lastmsg = message
    try:
        with open('.\\logs\\' + config.LOG_FILE, 'a',
                  encoding='utf-8', newline='') as fout:
            #message = '[%s] %s' % (strftime('%a %H:%M:%S'), message)
            message = '[%s] %s' % (strftime('%H:%M:%S'), message)
            print(message)
            print(message,file=fout)
    except FileNotFoundError:
        makedirs('.\\logs')
        log('Created log folder')
        log(message)

'''
def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

def pause(self):
    if not self.IsPaused:
        self.IsPaused = True
         #PAUSE
    else:
        self.IsPaused = False
         #UNPAUSE
'''


'''
WEB ELEMENT SEARCH
'''
def wait_until_class(classname, driver, secs=config.wait_until_seconds):
    try:
        WebDriverWait(driver, secs).until(
            EC.presence_of_element_located((By.CLASS_NAME, classname))
        )
        #log('Element: '+classname+' located before '+ str(secs))
        return 1
    except TimeoutException:
        #log(str(Exception))
        log('Element: '+classname+' not located')
        return 0

def wait_until_id(idname, driver, secs=config.wait_until_seconds):
    try:
        WebDriverWait(driver, secs).until(
            EC.presence_of_element_located((By.ID, idname))
        )
        return 1
    except TimeoutException:
        log('Element: ' + idname + ' not located')
        return 0

def wait_until_xp(xp, driver, secs=config.wait_until_seconds):
    try:
        WebDriverWait(driver, secs).until(
            EC.presence_of_element_located((By.XPATH, xp))
        )
        return 1
    except TimeoutException:
        log('Element: ' + xp + ' not located')
        return 0

def wait_until_class_displayed(classname, driver, secs=config.wait_until_seconds):
    try:
        WebDriverWait(driver, secs).until(
            EC.visibility_of_element_located((By.CLASS_NAME, classname))
        )
        #log('Element: '+classname+' located before '+ str(secs))
        return 1
    except TimeoutException:
        #log(str(Exception))
        log('Element: '+classname+' not located')
        return 0
    
def wait_until_id_displayed(idname, driver, secs=config.wait_until_seconds):
    try:
        WebDriverWait(driver, secs).until(
            EC.visibility_of_element_located((By.ID, idname))
        )
        return 1
    except TimeoutException:
        log('Element: ' + idname + ' not located')
        return 0
    
def find_visible_class(driver, name, single=False):
    #returns a list of visible elements
    l= []
    try:
        for i in driver.find_elements_by_class_name(name):
            if i.is_displayed():
                if single: #dont make a list if we just want a single element(first one)
                    return i
                l.append(i)
    except Exception:
        log('Exception locating visible element')
    if single: # don't return a list since it will trow an exception in the caller method
        return
    return l
        
'''
def ele_check(ele, driver ,wait=1):
    try:
        if ele[0] == '/':
            WebDriverWait(driver, wait).until(
                EC.visibility_of_element_located((By.XPATH, ele))
            )
            return True
        else:
            WebDriverWait(driver, wait).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ele))
            )
            return True
    except TimeoutException:
        return False
    except UnexpectedAlertPresentException as exp:
        log('%s\nAlert detected, dismissing' % exp)
        driver.switch_to_alert().accept()
        return ele_check(ele)
'''
   
def check_ap(driver,wait=1):
    try:
        if wait:
            wait_until_class("txt-stamina-value", driver)
        bp = driver.find_elements_by_class_name("txt-stamina-value")[0]
        total = bp.get_attribute("title")
        num = total.split("/")[0]
        config.AP = num
        log("AP: "+str(num))
        return (int)(num)
    except Exception:
        log('Exception in check_ap')
        raise #return 0


def check_bp(driver,wait=1):
    try:
        if wait:
            wait_until_class("prt-user-bp-value", driver)
        bp = driver.find_elements_by_class_name("prt-user-bp-value")[0]
        # num = bp.get_attribute("title")
        num = bp.get_attribute("data-current-bp")
        config.BP = num
        log("BP: " + str(num))
        return (int)(num)
    except Exception:
        log('Exception in check_bp')
        return 0
        #pass

def check_name(driver):
    try:
        main = False
        wait_until_class("btn-user-name", driver)
        username = (driver.find_elements_by_class_name("btn-user-name")[0]).text
        if username == config.username_rovax:
            main = True
            config.user_main = True
        log("User: " + str(username))
        return main
    except Exception:
        log('Exception in check_name')
        return 0
        #pass

'''
AUTOMATION
'''
def switchPause(paused=''):
    if paused !='':
        config.paused = bool(paused)
    else:
        config.paused = not config.paused
    sendTelegramMsg('Paused: '+str(config.paused))
    log('Paused: '+str(config.paused))

def checkPause():
    while config.paused:
        sleep(1)

def randomMoveT():  # Randomize mouse movement time
    return config.mmto[0] + config.mmto[1] * random.random()

def r(num, rand):
    return num + rand*random.random()

def randCoords(coords, offset = config.coordOffset):  # random mouse clicking
    [x1, y1, w, h] = coords
    #offset as percentage of the size
    xoffset = (w *(offset[0]/100))/2
    yoffset = (h *(offset[1]/100))/2
    x1 = x1 + xoffset
    x2 = w - xoffset*2
    y1 = y1 + yoffset
    y2 = h - yoffset*2
    #log("Coords Between x: (" + str(x1)+' '+str(x1+x2)+'), offset: '+str(xoffset))
    #log("Coords Between y: (" + str(y1) + ' ' + str(y1+y2)+'), offset: '+str(yoffset))
    #auxx = r(x1 + xoffset, w - xoffset*2)
    #auxy = r(y1 + yoffset, h - yoffset*2)
    auxx = r(x1,x2)
    auxy = r(y1,y2)
    return [auxx, auxy]


def mouseMove(coords):
    '''
    auxx,auxy = pyautogui.position()
    a=config.xscreensize/abs(coords[0]-auxx)
    b=config.yscreensize/abs(coords[1]-auxy)
    '''
    pyautogui.moveTo(coords[0], coords[1], duration=randomMoveT())  # pyautogui.moveTo(x,y,duration=num_seconds)


def findButton(name, GBF, by):
    button=''
    if by == 1: #select search method{class,id,xpath}
        #TODO fix that wait, interferes when spamming click to avoid missed click in the game(ex. coop)
        wait_until_class(name, GBF, config.wait_until_less)
        #aux = GBF.find_elements_by_class_name(name)
        #button = aux[0]
        button = find_visible_class(GBF,name,single=True)
    elif by == 2:
        wait_until_id(name, GBF, config.wait_until_less)
        button = GBF.find_elements_by_id(name)[0]
    elif by == 3:
        wait_until_xp(name, GBF, config.wait_until_less)
        button = GBF.find_element_by_xpath(name)
    elif by == 4:
        #pass directly by web element
        button = name
    width = button.size['width']
    height = button.size['height']
    x = button.location['x'] + config.tabposx
    y = button.location['y'] + config.tabposy
    return [x, y, width, height]


def clickButton(name, GBF, by=1,verify=True):
    try:
        clicked = False
        coords = ''
        #log('-Clicking: ' +str(name))
        if verify:
            checkVerify()
        while not clicked:
            #sleep(r(config.randomSleep[0],config.randomSleep[1]))
            coords = findButton(name, GBF, by)
            randcords = randCoords(coords)
            mouseMove(randcords)
            pyautogui.click(button='left')
            #print(strftime('%H:%M:%S') + ' Clicked at: ' + str(randcords))
            #check if button has been clicked
            #fcoords = findButton(name, GBF, by)
            #if fcoords[0] != -1:
                #log('-Clicked: '+ name)
            clicked = True
        return coords
    except Exception:
        log('Exception at button click')
        return
    
def clickButtonSkill(name, GBF, by=1):
    try:
        clicked = False
        coords = ''
        #log('-Clicking: ' +str(name))
        checkVerify()
        while not clicked:
            #sleep(r(config.randomSleep[0],config.randomSleep[1]))
            coords = findButton(name, GBF, by)
            randcords = randCoords(coords,config.skillOffset)
            mouseMove(randcords)
            pyautogui.click(button='left')
            #print(strftime('%H:%M:%S') + ' Clicked at: ' + str(randcords))
            #check if button has been clicked
            #fcoords = findButton(name, GBF, by)
            #if fcoords[0] != -1:
                #log('-Clicked: '+ name)
            clicked = True
        return coords
    except Exception:
        log('Exception at button click')
        return

def clickCoords(coords, GBF, offset=0, verify=True):
    if verify:
        checkVerify()
    if offset:
        randcords = randCoords(coords,offset)
    else:
        randcords = randCoords(coords)
    mouseMove(randcords)
    pyautogui.click(button='left')

def keyClick():  # Refresh
    pyautogui.press('f5')


def mouseClickImage(img, coords, offset=config.smallCoordOffset):
    if coords[0] != -1:
        click_image(img, coords, "left", randomMoveT(), offset)


'''
def mouseClick(coords):
    pyautogui.moveTo(coords[0], coords[1], duration=randomMoveT())  # pyautogui.moveTo(x,y,duration=num_seconds)
    pyautogui.click(button='left')
    # pyautogui.click(x=moveToX, y=moveToY, clicks=num_of_clicks, interval=secs_between_clicks, button='left')
'''
'''
ANTI-BAN

-Check verification when buttons are clicked, before loading another page and before scrolling
'''
def get_v(driver, url):
    checkVerify()
    driver.get(url)
    
def scroll_v(times):
    checkVerify()
    
def checkVerify( recheck=0 ):
    if not config.BOT_RAIDFINDER and not config.BOT_COOP and not config.BOT_QUEST:
        log('Verification error, no bot instances to check')
        input('Press any key to continue...')
        return

    driver=''
    bot= ''
    if config.BOT_COOP:
        bot = config.BOT_COOP
        driver = config.BOT_COOP.gbf
    if config.BOT_RAIDFINDER:
        bot = config.BOT_RAIDFINDER
        driver = config.BOT_RAIDFINDER.gbf
    if config.BOT_QUEST:
        bot = config.BOT_QUEST
        driver = config.BOT_QUEST.gbf
        
    try:
        #TODO: check if driver is the root window to work with it
        if True:#'supporter' in driver.current_url:
            if driver.find_elements_by_class_name('prt-supporter-confirm') or driver.find_elements_by_class_name('prt-supporter-battle-announce'):
                #TODO: check the button in the fav window(not displayed)
                log("- VERIFICATION, found: 'prt-supporter-confirm'")
                log('Stopping for verification')
                sendTelegramMsg("- VERIFICATION, found: 'prt-supporter-confirm'")
                saveScreenshot(driver)
                sendTelegramScreenShot()
                config.vpaused = True
                while config.vpaused:
                    sleep(1)
                return
                #input('Press any key to continue...')



        for text in config.verifytext:
            verilist = driver.find_elements_by_xpath("//*[contains(text(), '" + text + "')]")
            for veritem in verilist:
                attr = driver.execute_script(
                    'var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;',
                    veritem)
                
                if veritem.is_displayed():
                    log('- Found '+ text + ' displayed: '+str(attr))
                
                forcedCheck = False
                if attr == config.falsepositives[0] and veritem.is_displayed():
                    forcedCheck = True
                    
                if attr not in config.falsepositives or forcedCheck or veritem.is_displayed():
                    log('- VERIFICATION, found: ' + text + ' ' + str(attr))
                    log('Stopping for verification')
                    sendTelegramMsg('- VERIFICATION, found: ' + text + ' ' + str(attr))
                    saveScreenshot(driver)
                    sendTelegramScreenShot()
                    config.vpaused = True
                    while config.vpaused:
                        sleep(1)
                    #input('Press any key to continue...')

    except Exception:
        log('Exception while checking verification!')
        traceback.print_exc()
        #sendTelegramMsg('Exception while checking verification!')
        sleep(5)
        checkVerify(1)
        if recheck == 1:
            saveScreenshot(driver)
            sendTelegramScreenShot()
            config.vpaused = True
            while config.vpaused:
                sleep(1)
        #input('Press any key to continue...')
        '''
        Triggered when network error(check popup)
        '''
        pass

def saveScreenshot(driver):
    pathlib.Path('screen').mkdir(exist_ok=True)
    if os.path.isfile('screen/screen.png'):
        os.remove('screen/screen.png')
    pyautogui.screenshot('screen/screen.png',region=(0,0, config.tabSize[0], config.tabSize[1]))
    #driver.save_screenshot('screen/screen.png')

'''
INGAME MISC. ACTIONS
'''
def checkUsingBerries(driver):
    #check in case we're constantly spamming using berries
    #berries are always gonna be lower than 2
    if config.useBerries and check_bp(driver) <= 1:  # just used berries and gonna use more
        if wait_until_class("btn-use-full", driver, config.wait_until_less):
            useBerries(driver)
   
def useBerries(driver, wait=0):
    if not config.useBerries:
        return 0
    #if not wait_until_class('prt-popup-header', driver, config.wait_until_less):
    if not driver.find_elements_by_class_name("prt-popup-header"):
        return 0
    if (driver.find_elements_by_class_name("prt-popup-header")[0]).text == 'Not enough EP':
        log('Using berries')
        buttonlist = driver.find_elements_by_class_name("btn-use-full")
        for button in buttonlist:
            if 'index-3' in button.get_attribute("class"):
                clickButton(button, driver,4)
        wait_until_class('btn-usual-ok', driver)
        if (driver.find_elements_by_class_name("prt-popup-header")[0]).text == 'Use Item':
            clickButton('btn-usual-ok', driver)
            return 1
    return 0 #theoretically unreachable
    #for driver.find_elements_by_class_name("index-3")[0] in driver.find_elements_by_class_name("btn-use-full"):
    
def checkUsingElixirs(driver):
    ap = 0
    try:
        ap = check_ap(driver,0)
    except Exception:
        log("Couldn't check if using elixirs")
        return
    if config.usePots and ap < config.minap:  # just used ap and gonna use more
        if wait_until_class("btn-use-full", driver, config.wait_until_seconds):
            useElixirs(driver)

def useElixirs(driver):
    if not config.usePots:
        return 0
    #if not wait_until_class('prt-popup-header', driver, wait):
    if not find_visible_class(driver,"prt-popup-header"):
        return 0
    if (find_visible_class(driver,"prt-popup-header")[0]).text == 'Not enough AP':
        log('Using half pots')
        buttonlist = find_visible_class(driver,"btn-use-full")
        for button in buttonlist:
            if 'Half Elixir' in button.get_attribute('data-item-name'): #TODO clicks the dropdown menu
                clickButton(button, driver,4)
        wait_until_class('btn-usual-ok', driver)
        if (driver.find_elements_by_class_name("prt-popup-header")[0]).text == 'Use Item':
            clickButton('btn-usual-ok', driver)
            return 1
    return 0 #theoretically unreachable
    #for driver.find_elements_by_class_name("index-3")[0] in driver.find_elements_by_class_name("btn-use-full"):

def checkPopup(driver):
        try:
            #title_popup = (find_visible_class(driver, "prt-popup-header")[0]).text
            #text_popup = (find_visible_class(driver, "txt-popup-body")[0]).text
            title_popup = find_visible_class(driver, "prt-popup-header", single=True)
            if title_popup:
                checkVerify()
                title_popup = title_popup.text
            else:
                raise Exception #no popup
            text_popup = find_visible_class(driver, "txt-popup-body", single=True)
            if text_popup:
                text_popup = text_popup.text
            if useBerries(driver):
                log('Use berries popup')
            if title_popup == 'エラー':
                log('Network Error')
                clickButton('btn-usual-ok', driver, verify=False)
                return 1
            if title_popup == 'Access Verification':
                log('Verification Triggered')
                checkVerify()
                input('Press any key to continue...')
                return 1
            elif title_popup == 'Processing':
                log('Processing turn')
                clickButton('btn-usual-ok', driver, verify=False)
                return 1
            elif title_popup == 'Use Skill':
                log('Clicked Skill too Fast')
                clickButton('btn-usual-ok', driver, verify=False)
                clickButton('btn-usual-cancel', driver, verify=False)
                return 1
            elif title_popup == 'Skill' or title_popup == 'Skill.':
                #TODO: when the title is Skill. is when trying to cast puppet strings(orchid) when already in effect
                #TODO: check further if this is the correct popup for a skill overlapping with other player's
                log('Overlapping skill')
                clickButton('btn-usual-ok', driver, verify=False)
                return 1
            elif title_popup == 'This battle has ended.':
                #TODO: check further if this is the correct popup for a skill overlapping with other player's
                log('Battle has ended')
                clickButton('btn-usual-ok', driver, verify=False)
                return 1
            elif title_popup == 'Summons Details':
                log('Clicked Summon too Fast')
                clickButton('btn-usual-cancel', driver, verify=False)
                return 1
            elif title_popup == 'Resume Quests':
                log('Resuming quest')
                clickButton('btn-usual-ok', driver, verify=False) #its called the same
                return 1
            elif find_visible_class(driver,"pop-result-assist-raid") or (text_popup in config.poperrs):
                log('Error joining raid, popup')
                clickButton('btn-usual-ok', driver, verify=False)
                return 1
            elif text_popup == config.poppending:
                log('We got pending battles')
                clearPendingBattles(driver)
                return 1
            return 0
        except Exception:
            #log('Exception at checkPopup (No popup?)')
            return 0

def clearPendingBattles(driver):
    log('Clearing pending battles')
    try:
        #either click ok button or goto the pending battles section
        get_v(driver,config.pendingb)
        wait_until_id('prt-unclaimed-list',driver) #first w8 for the correct window, then w8 for the actual list
        wait_until_class('lis-raid',driver) #conflicts with the actual raid list
        pending_list = driver.find_elements_by_class_name("lis-raid")
        for raids in pending_list:
            raidhref = raids.get_attribute('data-href')
            if raidhref == "":
                continue
            config.pending_raid_hrefs.append(raidhref)

        #log('Clearing '+str(len(config.pending_raid_hrefs))+' pending battles from: '+str(config.pending_raid_hrefs))
        while len(config.pending_raid_hrefs) != 0:
            for hrefs in config.pending_raid_hrefs:
                get_v(driver,'http://game.granbluefantasy.jp/#'+hrefs)
                #takes a while to load the next result screen and interferes with the wait until class
                if driver.current_url == 'http://game.granbluefantasy.jp/#'+hrefs and wait_until_class('prt-result-cnt',driver):
                    config.pending_raid_hrefs.remove(hrefs)
                    get_v(driver,config.pendingb) #avoid problems from going result to result
                    wait_until_id('prt-unclaimed-list', driver)

    except Exception:
        log("Exception in 'clearPendingBattles'")



'''
SUMMON SELECTION
'''

class SummonSelector(object):
    #select summons (and party) before a raid
    gbf = ''
    raidname = ''
    raidhp = ''
    raidbp = ''
    pplin= ''
    failedjoin = False
    joined = False
    simplesummon = True

    def __init__(self,d):
        log('Creating summon selector')
        self.gbf = d
        if not self.gbf.find_elements_by_class_name("btn-attack-start"): #we are attackign already
            wait_until_class('lis-supporter', self.gbf, config.wait_until_less*2)
        self.raidname = self.gbf.find_elements_by_class_name('txt-raid-name')
        if self.raidname: #for quests this doesnt exist
            self.raidname = self.raidname[0].text
        self.raidhp = self.gbf.find_elements_by_class_name('prt-raid-gauge-inner')
        if self.raidhp:
            self.raidhp = self.raidhp[0].get_attribute('style').split('%')[0].split(' ')[1]
            self.raidhp = int(self.raidhp)
        #self.raidbp = (self.gbf.find_elements_by_class_name('prt-use-ap')[0]) #no idea why its called ap here
        self.pplin = self.gbf.find_elements_by_class_name('prt-flees-in')
        if self.pplin: #for quests this doesnt exist
            self.pplin = int(self.pplin[0].text)


    def findVisibleSummon(self):
        #start = time.time()
        supporter_list = self.gbf.find_elements_by_class_name("lis-supporter")
        if not supporter_list:
            raise Exception #not in summon list
        
        if config.summonDefCoords[0] != 0 and self.simplesummon:
            clickCoords(config.summonDefCoords,self.gbf)
            return

        #support_levels = self.gbf.find_elements_by_class_name("txt-summon-level")
        for supports in supporter_list:
            if not supports.is_displayed():
                continue
            if (supports.find_elements_by_class_name("txt-summon-level")[0]).text == "":
                continue

            selected_support = supports
            log('Found summon')
            break
        #end = time.time()
        #print('Summon selection time: ' + str(end - start))
        #get the coords for the 1st summon in the list
        config.summonDefCoords = clickButton("prt-button-cover",selected_support)

    def select(self):
        try:
            if self.pplin == 30:
                log('Raid already full')
                raise Exception #no need to try if raid is full
            if self.raidname in char_templates.blue_chest_raids and (self.raidhp < config.blueChestMinHp or self.pplin >= config.blueChestMaxPeople):
                log('Raid at too low hp or too many people inside')
                raise Exception
            self.findVisibleSummon()
            #TODO usual ok button causes problems
            if not wait_until_class('btn-usual-ok', self.gbf, config.wait_until_less):
                self.findVisibleSummon() #retry clicking the summon if button didnt show
            if not clickButton('btn-usual-ok', self.gbf):
                raise Exception  # summon not clicked after all

            if wait_until_class('pop-result-assist-raid', self.gbf, config.wait_until_less): #pop-usual
                raise Exception #raid full or finished
            if self.gbf.find_elements_by_class_name("txt-popup-body"):
                raise Exception #pending battles

            joined = True
            #return 1
        except Exception:
            #log(str(Exception))
            joined = False
            raise
            #return 0
