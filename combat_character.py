'''
CHARACTER & SKILLS

'''

from functions import *
import char_templates

class Character(object):

    def __init__(self, gbf, slot, character_ele, skills):
        #log('Creating character')
        self.slot = slot
        self.gbf = gbf
        #self.hp_elem = ''
        self.skills_elem = skills
        self.character_ele = character_ele #don't use it
        #self.img = self.setImg()
        self.name = self.setCharacterName()
        self.skills = self.setSkills()
        self.skillStates = []
        #log('Character created')


    def setCharacterName(self):
        name = self.character_ele['name']
        if config.username_rovax == name and char_templates.attribute == 0: #set the attribute for the skills to use
            char_templates.attribute = int(self.character_ele['attr'])
        #name = char_templates.getCharNameFromSrc(self.img)
        #log(name)
        return name

    def setSkills(self):
        #skills = char_templates.char_skills[self.name]
        skills = []
        for key, value in self.skills_elem['list'].items():
            skillname = value[0]['ability-name']
            skills.append(skillname)
        return skills

    def getSkillPos(self,sname):
        if config.username_rovax in self.name: #if its the mc(skills can be in several positions)
            index = self.skills.index(sname) if sname in self.skills else -1
            return index
        else: #rest of the chars have the positions mapped in a dict
            index = char_templates.getPosFromSkill(sname)
            return index-1

    def useSkill(self,name):
        try:
            condition = self.character_ele['condition']
            sealed = condition['seal_flag']
            if sealed: #will trigger exception if not sealed
                return 1
        except Exception:
            pass
        try:
            i = self.getSkillPos(name)
            if i != -1 :
                s = self.getSingleSkillEle(i+1)
                if s.getSingleSkillState():
                    if self.checkSkillOugi(name):
                        s.clickSkill()
                        return 1
                else:
                    return 1 #fix for when we get to the raid from a timeout and skill are already pressed
            return 0
        except Exception:
            log('Exception using skill')
            traceback.print_exc()
            raise

    def checkSkillOugi(self,name):
        # check the ougi cost
        ougi_cost = char_templates.getSkillOugiCost(name)
        if ougi_cost:
            #char_name = char_templates.getCharFromSkill(name)
            if not ougi_cost <= self.getOugi():
                return 0 #can't use the skill
        return 1

    def getOugi(self):
        #ougi = self.gbf.execute_script("return stage.gGameStatus.player.param[" + str(self.slot-1) + "].recast")
        char_ele = self.gbf.execute_script('return stage.gGameStatus.player.param[' + str(
            self.slot - 1) + ']')  # needs to be in real time to avoid problems
        ougi = char_ele['recast']
        #if not self.ougitext_elem:
            #self.ougitext_elem = self.character_ele.find_elements_by_class_name('txt-gauge-value')
        return int(ougi) #self.ougitext_elem[0].text
    
    def getHp(self):
        #if not self.hp_elem:
            #self.hp_elem = self.character_ele.find_elements_by_class_name('prt-gauge-hp-inner')
        #hp = self.hp_elem.get_attribute('style').split()[1]
        char_ele = self.gbf.execute_script('return stage.gGameStatus.player.param['+str(self.slot-1)+']') #needs to be in real time to avoid problems
        hp = (char_ele['hp']*100)/char_ele['hpmax']
        return int(hp) #int(hp[0:-2])

    def getSingleSkillEle(self,pos):
        if self.skills_elem:
            jskill = self.skills_elem['list'][str(pos)][0]
            skill = Skill(self, pos, jskill, self.gbf)
            #return self.skills_elem[pos-1]
            return skill

        jskill = self.gbf.execute_script('return stage.pJsnData.ability['+str(self.slot)+'].list['+str(pos)+'][0]')
        skill = Skill(self,pos,jskill,self.gbf)
        return skill


class Skill(object):

    def __init__(self, char, pos, skill_inf, gbf):
        self.char = char
        self.pos = pos
        self.skill_inf = skill_inf
        self.name = skill_inf['ability-name']#self.getName()
        self.gbf = gbf
        self.skill_id = skill_inf['ability-id']
        #log('Created skill: '+self.name)

        #stage.gGameStatus.attackQueue.param


    def getSkillEle(self):
        auxclass = 'ability-character-num-' + str(self.char.slot) + '-' + str(self.pos)
        self.skill_ele = find_visible_class(self.gbf, auxclass)
        return self.skill_ele[0]

    def clickSkill(self):
        try:
            clickCoords(self.getSkillLoc(), self.gbf, config.skillOffset,verify=False)
            return 1
        except Exception:
            #little hack to keep trying to use skills for some time until no exceptions occur
            t = Timer()
            done = 0
            while not done and not t.check_timeout(config.wait_until_less):
                try:
                    #auxclass = 'ability-character-num-' + str(self.char.slot) + '-' + str(self.pos)
                    #ele = find_visible_class(self.gbf, auxclass)[0]
                    ele = self.getSkillEle()
                    clickCoords(self.getSkillLoc(ele), self.gbf, config.skillOffset,verify=False)
                    done = 1
                except Exception:
                    log('Double exception clicking skill')
                    continue
                else:
                    log('Else triggered')
                    # the rest of the code
                    return 1
                    #break

    def getSkillLoc(self, ele=''):
        if not ele:
            ele = self.getSkillEle()#self.skill_inf
        width = 23.58 #fix for viramate resizing the icons
        height = 23.58
        x = ele.location['x'] + config.tabposx
        y = ele.location['y'] + config.tabposy
        return [x, y, width, height]

    def getSingleSkillState(self):
        #this is the turns left to recast: 0 is available otherwise not
        #r = self.skill_inf.get_attribute('ability-recast')
        r = self.skill_inf['ability-recast']
        #sealedchar = self.gbf.execute_script('return stage.gGameStatus.player.param[' + str(self.char.slot - 1) + '].condition.seal_flag')
        #if sealedchar:
            #r = '1' #different to 0 so it returns false
        return r == '0'