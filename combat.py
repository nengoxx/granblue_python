'''
COMBAT BOT

'''
import char_templates
import json
from functions import *
from combat_character import *
import images

class Combat(object):

    # The class "constructor" - It's actually an initializer
    def __init__(self, gbf):
        log('Creating combat bot')
        self.gbf = gbf
        wait_until_class('btn-attack-start', self.gbf, config.maxWtillCombat)
        if self.gbf.find_elements_by_class_name("btn-attack-start"):
            self.incombat = True
        else:
            self.incombat = False
        self.active = True
        self.autoed = False
        self.prt_turn_num = ''
        self.summons = []
        self.turn = 0
        self.lasturn = 0
        self.torched = False
        self.attacktimes = 0
        self.combatMode = 0  # 0=leech, 1=skills, 2=torch
        self.chars = []
        self.initturn = 1  # 1: initial turn, 2 or more:not initial(doesnt add up beyond 2)
        self.attacking = False  # between attack button showing(can't do anything)
        #self.skillList = [] #directly use the skills from here(no ougi check for now)
        self.skillsused = 0 #total skills used for turn 1 buffing before anything
        self.skillstouse = [] #list to get from char templates
        self.attackbutton = ''
        self.popup = 1 #popup appeared, use it to not attack
        self.potsused = 0
        log('Combat bot created')


    def testAttack(self):
        try:
            if checkPopup(self.gbf):
                self.resetElements()
                self.popup = 1
                return False
            pushed = self.gbf.execute_script('return stage.gGameStatus.attackQueue.attackButtonPushed')
            #self.attackbutton = self.gbf.find_elements_by_class_name("btn-attack-start")
            if not pushed: #self.attackbutton and self.attackbutton[0].is_displayed():
                self.incombat = True
                self.attacking = False #finished the attack, button back to normal
                return True
            return False
        except Exception:
            #traceback.print_exc()
            #log(str(Exception))
            return False

    def fastCheckPopup(self):
        if checkPopup(self.gbf):
            self.resetElements()
            self.popup = 1
            return False

    def getSkillZone(self):
        skillZone = self.gbf.find_elements_by_class_name("prt-command")[0]
        width = skillZone.size['width']
        height = skillZone.size['height']
        x = skillZone.location['x'] + config.tabposx
        y = skillZone.location['y'] + config.tabposy
        return [x, y, x+width, y+height]

    def attack(self,force=0):
        if self.combatMode == 2 and not force:
            self.attackTorch()
            return
        elif self.combatMode == 1 and not force:
            self.attackWSkills()
            return
        if self.incombat == False:
            return
        if self.testAttack():
            if config.attackDefCoords[0] != 0:
                clickCoords(config.attackDefCoords,self.gbf,verify=False)
                self.attacking = True
                self.attacktimes += 1
                log('Attacked '+ str(self.attacktimes)+ ' times')
            else:
                self.attackbutton = self.gbf.find_elements_by_class_name("btn-attack-start")
                if self.attackbutton and self.attackbutton[0].is_displayed():
                #self.attackbutton = find_visible_class(self.gbf,"btn-attack-start")
                    config.attackDefCoords = clickButton(self.attackbutton[0], self.gbf,4,verify=False)
                    self.attacking = True
                    self.attacktimes += 1
                    log('Setting up attack button coords')
                    log('Attacked '+ str(self.attacktimes)+ ' times')
        #self.auto()
    
    def getTorchSkills(self):
        start = time.time()
        plainskillids = ['2999','200011'] #groundzero 5*, glory+disparia
        plainskills = []
        pskill1 = find_visible_class(self.gbf,"ability-character-num-1-1")[0]
        if pskill1 and pskill1.get_attribute('ability-id') == plainskillids[1] and pskill1.get_attribute("ability-recast") == '0':
            log('sm skill found')
            if not find_visible_class(pskill1,'ico-ability-shine'):
                log('sm skill not being used')
                plainskills.append(pskill1)
        pskill2 = []
        pskill2.append(find_visible_class(self.gbf,"ability-character-num-2-3")[0]) #2nd char 3rd skill
        pskill2.append(find_visible_class(self.gbf,"ability-character-num-3-3")[0]) #3rd
        pskill2.append(find_visible_class(self.gbf,"ability-character-num-4-3")[0]) #4th
        for s in pskill2:
            if s.get_attribute('ability-id') in plainskillids and s.get_attribute("ability-recast") == '0':
                if not find_visible_class(s,'ico-ability-shine'):
                    plainskills.append(s)
        end = time.time()
        #print('Found skills time: ' + str(end - start))
        #print('Skills found: '+str(len(plainskills)))
        if plainskills:
            return plainskills
        
    def attackWSkills(self):
        try:
            #self.setupChars()
            self.get_turn()
            if self.turn > 1 and self.initturn:
                self.initturn = 0
            if self.initturn: #if its the 1st turn use the start configuration(skills)
                self.startConfig()
                self.skipAttack()
                '''
                try:
                    if self.chars and (not self.chars[0].name == 'MC_Lucha_Kungfu' or not self.chars[0].getSingleSkillState(3)): #check if tag team is being used to not realod when attacking by it
                        self.skipAttack()
                except Exception:
                    pass
                '''
            else:
                self.setupSkills()
                self.setupChars()
                self.use_potions()
                self.use_skills()
                if self.skillstouse and (self.skillsused < len(self.skillstouse) - 1):
                    log("Couldn't use all the skills, retrying")
                    self.chars = []
                    return
                if self.turn > 5: #use luci just once
                    self.use_summons(1)
                if self.popup:
                    self.popup = 0
                    return
                #else:
                self.attack(1)
                self.skipAttack()
        except Exception:
            #traceback.print_exc()
            self.resetElements()
        return
        
    def startConfig(self):
        #log('Start Config')
        try:
            self.setupSkills()
            self.setupChars()
            self.use_skills()
            if self.skillstouse and (self.skillsused < len(self.skillstouse) - 1):#len(char_templates.skillCombos(self.turn))-1:
                log("Couldn't use all the skills, retrying")
                self.chars = []
                return
            self.use_summons()
            if self.popup:
                self.popup = 0
                return
            #else:
            self.attack(1) #force attack
        except Exception:
            traceback.print_exc()
            self.resetElements()
        return

    def use_potions(self):
        return #TODO rework it for regular potions
        if char_templates.current_raidname in char_templates.no_pot_raids:
            #don't use pots for zoi teams
            return
        #blue gw pot = 35% hp heal
        #self.setupChars()
        #for i in range(4):
        if self.potsused >= 1:
            return
        charstoheal = 0
        charstoheal_urgent = 0
        for c in self.chars:
            charhp = c.getHp()
            if charhp <= 100-45:
                charstoheal += 1
            elif charhp <= 100-35:
                charstoheal += 0.5 # count them as half a char
            if charhp <= 25:
                charstoheal_urgent += 1
        if charstoheal >= 3 or (charstoheal >= 2.5 and charstoheal_urgent >= 1):
            log('Using potions')
            clickButton('btn-temporary',self.gbf,1,verify=False)
            wait_until_class_displayed('img-temporary',self.gbf,2)
            potionbuttons = find_visible_class(self.gbf,'img-temporary')
            if not potionbuttons:
                clickButton('btn-temporary', self.gbf, 1, verify=False)
                wait_until_class_displayed('img-temporary', self.gbf, 2)
                potionbuttons = find_visible_class(self.gbf, 'img-temporary')
            if len(potionbuttons) >= 3:
                clickButton(potionbuttons[3],self.gbf,4,verify=False)
                wait_until_class_displayed('btn-usual-ok', self.gbf, 3)
                clickButton('btn-usual-ok', self.gbf, 1, verify=False)
                self.potsused += 1

    def use_skills(self):
        if not self.testAttack():
            return 0
        skillsused = 0
        if not self.skillstouse:
            #TODO: check when self.skillstouse is null and is used in other methods
            #log(str(skillsused) + ' skills used')
            self.skillsused = skillsused
            return
        log('Using skills')
        #self.setupChars()  # when theres no skills we dont setup the chars so we force it here
        skillstouse = self.skillstouse[:] #dont remove the skills while we traverse them, [:] is to copy the list by value, not reference
        for skill in skillstouse:
            if not skill in char_templates.skill_pos:
                self.skillstouse.remove(skill)
                continue
            self.fastCheckPopup()
            skillchar = char_templates.getCharFromSkill(skill)
            c = self.chars[int(skillchar)-1]
            try:
                if c.useSkill(skill):
                    skillsused += 1
            except Exception:
                if c.useSkill(skill):
                    skillsused += 1
            '''
            for c in self.chars:
                skillchar = char_templates.getCharFromSkill(skill)
                if skillchar and c.name != skillchar:
                    continue
                try:
                    if c.useSkill(skill):
                        skillsused += 1
                        break
                except Exception:
                    if c.useSkill(skill):
                        skillsused += 1
                        break
            '''
        log(str(skillsused)+' skills used')
        self.skillsused = skillsused

    def setupSkills(self):
        jskills = self.gbf.execute_script('return stage.pJsnData.ability')
        self.jskills = jskills
        self.skillstouse = char_templates.skillCombos(self.turn)
        char_templates.skill_pos.clear() #delete all entries
        for key_char_pos, value in jskills.items():
            #Make a dictionary to map the skills to a char position for the turn and a skill position forever
            for key_skill_pos, value_2 in value['list'].items():
                skillname = value_2[0]['ability-name']
                skillrecast = value_2[0]['ability-recast'] #TODO: set a list to use the skills for this turn
                if skillrecast == '0':
                    char_templates.skill_pos[skillname] = [key_char_pos,key_skill_pos]
                #{skillname : key_char_pos}
                #{skillname : key_skill_pos}
        return jskills


    def skipAttack(self):
        if not config.attackskip:
            return
        log('Waiting to skip attack')
        while not self.testAttack():
            try:
                if self.checkFinished() or checkPopup(self.gbf):
                    break
                #if self.chars[0].isAttacking() or self.chars[1].isAttacking() or self.chars[2].isAttacking():
                autoshow = self.gbf.execute_script('return stage.gGameStatus.enable_auto_button')
                atk_action = self.gbf.execute_script('return stage.gGameStatus.attack_action')
                if autoshow and atk_action == 'normal_attack_result':
                    players = self.gbf.execute_script('return stage.gGameStatus.player.param')
                    self.gbf.refresh()
                    self.resetElements()
                    ougichars = 0
                    ougireq = 100
                    for slot in players: #check and wait for the character ougiing to avoid turn popups
                        ougireq = ougireq - (10*ougichars)
                        if slot['recast'] >= ougireq:
                            ougichars += 1
                    if ougichars == 2:
                        log('2 chain burst')
                        sleep(9-3) #its 2 sec slower than viramate
                    elif ougichars == 3:
                        log('3 chain burst')
                        sleep(10-3)
                    elif ougichars == 4:
                        log('4 chain burst')
                        sleep(11-3)
                    #TODO: make a global timer and check it after setting up character and skills
                    return
            except Exception:
                self.chars = []
                #traceback.print_exc()
                continue

    
    def setupChars(self):
        if self.chars:
            return
        log('Setup characters')
        jchars = self.gbf.execute_script('return stage.gGameStatus.player.param')
        jskills = self.jskills
        slot = 1
        for char in jchars:
            try:
                c = Character(self.gbf, slot, char, jskills[str(slot)])
            except Exception:
                log('Exception creating char')
                #traceback.print_exc()
                continue
            self.chars.append(c)
            slot += 1
        '''
        cs = find_visible_class(self.gbf,'btn-command-character')
        slot = 1
        for char in cs:
            try:
                c = Character(slot,char,self.gbf)
            except Exception:
                log('Exception creating char')
                #traceback.print_exc()
                continue
            self.chars.append(c)
            slot += 1
        '''

    def attackTorch(self):
        try:
            if self.getTorchSkills():
                self.torched = False
            #locate attack button
            if self.testAttack() and not self.torched:
                #wait_until_class('btn-attack-start', self.gbf,10)
                sx1,sy1,sx2,sy2 = self.getSkillZone()
                mouseClickImage(images.sm1, imagesearcharea(images.sm1,sx1,sy1,sx2,sy2),config.smallCoordOffset)
                sleep(1)#too much spam
                mouseClickImage(images.sarasa3, imagesearcharea(images.sarasa3,sx1,sy1,sx2,sy2),config.smallCoordOffset)
                sleep(1)#too much spam
                #clickButton('ability-character-num-2-3', self.gbf) #2nd char 3rd skill(sarasa's gz)
                #clickButton('ability-character-num-1-1', self.gbf) #mc sm awaken
                self.torched = True
        except Exception:
            log("Exception in 'attackTorch'")

    def auto(self):
        wait_until_class_displayed('btn-auto', self.gbf, config.wait_until_less)
        btnauto = self.gbf.find_elements_by_class_name("btn-auto")
        if 'display: block;' in (self.gbf.find_elements_by_class_name("btn-auto")[0]).get_attribute("style"):
            self.autoed = True
            return
        autobtn = self.gbf.find_elements_by_class_name("btn-auto")[0]
        clickButton("on", autobtn)

    def checkFinished(self):
        try:
            diedtips = find_visible_class(self.gbf,"prt-tips")
            if diedtips:# and diedtips[0].location['x']!=0: #'display: none;'  == 'display: block;'
                self.incombat = False
                log('You died, exiting raid')
                return 1
            if self.gbf.find_elements_by_class_name("prt-result-cnt"):
                self.incombat = False
                log('Reward room, combat finished')
                config.raidsFinished += 1
                log('Raids finished: '+str(config.raidsFinished))
                #expGain = self.gbf.find_elements_by_class_name("prt-popup-header")[0]
                #self.rewards()
                return 1
            if find_visible_class(self.gbf,'prt-popup-header',single=True).text == 'Salute Participants':
                self.incombat = False
                log('You died, exiting raid')
                return 1
            return 0
        except Exception:
            #traceback.print_exc()
            return 0
        
    def rewards(self):
        e = self.gbf.find_elements_by_class_name('txt-exp-plus')
        if e:
            expgained = e[1]#theres 2
        r = self.gbf.find_elements_by_class_name('txt-rankpt-plus')
        if r :
            rankgained = r[1]
        if e and r:
            config.totalExpGain += int(expgained.text)
            config.totalRankGain += int(rankgained.text)
    
    def dismissInitialDialog(self):
        log('Dismissing initial combat dialogs')
        while not self.testAttack(): #w8 till attack button is visible
            wait_until_class('prt-popup-header', self.gbf, config.maxWtillCombat)
        popups = self.gbf.find_elements_by_class_name('pop-usual')
        actual_popup = ''
        for popup in popups:
            if not popup.is_displayed(): #'pop-show' in popup.get_attribute("class"):
                continue
            actual_popup = popup
            break
        
        if actual_popup and 'pop-trialbattle-notice' in actual_popup.get_attribute("class"): #trial battle popup
            clickButton('btn-usual-close', actual_popup)
        return
    
    def get_turn(self):
        #start_time = time.time()
        try:
            num = int(self.gbf.execute_script('return stage.gGameStatus.turn'))
            log('Turn: '+str(num))
            if num != 0:
                self.turn = num
            #print("--- %s seconds ---" % (time.time() - start_time))
            return num
        except Exception:
            log('Exception getting turn number')
            #traceback.print_exc()
            self.resetElements()
            return 0

    '''
    def use_summons_old(self,reverse=0):
        start_time = time.time()
        if not self.testAttack():
            return
        try:
            if not self.summons:
                #log('Setting up summons')
                self.summons = self.gbf.find_elements_by_class_name('quick-summon')
            if reverse:
                for s in reversed(self.summons): #start from the end
                    if not s.is_displayed():
                        continue
                    if not 'unavailable' in s.get_attribute("class"):
                        log('Using summon')
                        clickButton(s,self.gbf,4)
                        print("--- %s seconds ---" % (time.time() - start_time))
                        return
            else:
                for s in self.summons:
                    if not s.is_displayed():
                        continue
                    if not 'unavailable' in s.get_attribute("class"):
                        log('Using summon')
                        clickButton(s,self.gbf,4)
                        print("--- %s seconds ---" % (time.time() - start_time))
                        return
            print("--- %s seconds ---" % (time.time() - start_time))
        except Exception:
            traceback.print_exc()
            #log('Exception using summon')
            self.summons = ''
    '''

    def use_summons(self,reverse=0):
        #start_time = time.time()
        avail = int(self.gbf.execute_script('return stage.pJsnData.summon_enable'))
        if not self.testAttack() or not avail:
            return
        try:
            jsummons = self.gbf.execute_script('return stage.pJsnData.summon')
            jsummons.append(self.gbf.execute_script('return stage.pJsnData.supporter'))
            for idx, jsummon in enumerate(jsummons):
                if jsummon['name'] in char_templates.usable_summons and jsummon['recast'] == '0':
                    log('Using summon')
                    self.summons = self.gbf.find_elements_by_class_name('quick-summon')
                    clickButton(self.summons[idx], self.gbf, 4, verify=False)
                    #print("--- %s seconds ---" % (time.time() - start_time))
                    return

            #print("--- %s seconds ---" % (time.time() - start_time))
        except Exception:
            #traceback.print_exc()
            #log('Exception using summon')
            self.summons = ''



    def resetElements(self):
        self.summons = ''
        self.chars = []
        #self.skillList = []
        self.skillstouse = []
        #self.turn = 0
        self.prt_turn_num = ''
        self.attackbutton = ''

    def run(self):
        combaTimer = Timer()
        while self.incombat == True and not combaTimer.check_timeout(config.maxCombaTime):
            self.checkFinished()
            if not self.autoed:
                self.attack()
        return True



def make_combatbot(gbf):
    combatbot = Combat(gbf)
    return combatbot
