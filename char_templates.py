'''
CHARACTER TEMPLATES
info to connect the character image with the character skills ids/names and requirements

'''
import config

#img-chara-command => src url of the pic

skillCombosType = '' #same as quest gwmode: ex,nm
attribute = 0 #mc attribute set in combat char: fire,water,earth,wind,light,dark(from 1 to 6)
current_raidname = ''

'''
'Miserable Mist', 'Armor Break II ', 'Rage IV','Full Arsenal III','Clarity',  # mc
'Speed',"Order +","Discord +",  # gandalf
'Autoignition',  # eugen
"Gaze into Crystal Ball","Heaven's Moon ++","Tabula Rasa ++","Nakshatra","End Gaze", # arulu
"Collapse ++","Phantasmagoria ++","Reinforce"] #cag

'Bal-Sagoth +', #Amira
                            'Regulus Gloria +',  # Seruel
                            'Power Within ++', #Amira
                            'Royal Curtain ++', #Seruel
                            'Alone in Heaven +', 'The Power of One',  # Sandal
                            'Rage IV', 'Miserable Mist', 'Armor Break II ', #mc
                            'Half-God Half-Demon +',  # Amira (hack to give time for her to get charge bar)
                            'Full Arsenal III']  # mc
'''

skill_cost = { #from skill get costs
    'Reckoning Night':{'ougi_cost':30,'hp_cost':0}, #S.Heles
    'Half-God Half-Demon +':{'ougi_cost':100,'hp_cost':0}, #Amira
    'Rage IV':{'ougi_cost':30,'hp_cost':0},
    'Intercept II +':{'ougi_cost':40,'hp_cost':0}, #Eugen
    'Redouble ':{'ougi_cost':20,'hp_cost':0}, #Sturm
    'Luminiera Merge':{'ougi_cost':50,'hp_cost':0} #Vira
    }

skill_pos = { #from skill get position & char
    #THIS IS JUST AN EXAMPLE: the names of the chars will be changed to the current position of the character
    'Quick Raid ++':['Seruel',1],
    'Royal Curtain ++':['Seruel',2],
    'Regulus Gloria +':['Seruel',3],
    'Alone in Heaven +':['Sandalphon',1],
    'Ecliptica +':['Sandalphon',2],
    'The Power of One':['Sandalphon',3],
    'Carry On +':['Heles',1],
    'Graven Image +':['Heles',2],
    'Reckoning Night':['Heles',3],
    'Bal-Sagoth +':['Amira',1],
    'Power Within ++':['Amira',2],
    'Half-God Half-Demon +':['Amira',3]
}

usable_summons = ['Shiva','Luminiera Omega','Anat','Lucifer','Tiamat Omega','Athena','Bahamut'] #,'Kaguya'

blue_chest_raids = ['Grimnir (Impossible).','Rosequeen Showdown Impossible.','Lvl 100 Xeno Ifrit.','Avatar (Impossible).','Shiva (Impossible).','Metatron (Impossible).','Luminiera Omega (Impossible).']
no_pot_raids = ['Grimnir (Impossible).','Rosequeen Showdown Impossible.','Avatar (Impossible).','Shiva (Impossible).','Metatron (Impossible).','Luminiera Omega (Impossible).']

def getSkillOugiCost(name):
    try:
        return skill_cost[name]['ougi_cost']
    except Exception:
        return 0

def getSkillHpCost(name):
    try:
        return skill_cost[name]['hp_cost']
    except Exception:
        return 0

def getCharFromSkill(name):
    #input skill name & get char name
    try:
        return skill_pos[name][0]
    except Exception:
        return ''

def getPosFromSkill(name):
    #input skill name & get position(starts from 1)
    try:
        return int(skill_pos[name][1])
    except Exception:
        return 0

def skillCombos(int, element='default'):
    #skill queue list for early turns
    list=[]
    #TODO: use the attribute variable to setup the skills dinamically
    basic = ['Miserable Mist', 'Armor Break II ',"Defense Breach"]
    grimnir = ['Indicum +','Conjuction +']
    rosequeen = ['Miserable Mist', 'Armor Break II ', 'Rage IV','Full Arsenal III','Clarity',
                djeanne[2-1],zoi[2-1],zoi[1-1],zoi[3-1],orchid[3-1],
                vira[1-1],vira[2-1],vira[4-1],bk[1-1],bk[2-1],bk[3-1],
                orchid[1-1]]
    xenoifrit_fast = [altair[1-1],altair[2-1],altair[3-1],uno[2-1],
                 uno[1-1],"Double Trouble III",'Tag Team']
    ex_fast = [diantha[1-1],diantha[3-1],altair[1 - 1], "Miserable Mist","Defense Breach", altair[3 - 1], uno[2 - 1],
                      uno[1 - 1], "Double Trouble III", 'Tag Team']
    xenoifrit = ["Panacea III", "Veil",diantha[1-1],diantha[2-1],diantha[3-1], altair[1 - 1], altair[2 - 1],"Defense Breach", altair[3 - 1], uno[2 - 1],
                 quatre[1 - 1], quatre[2 - 1], uno[1 - 1], uno[3 - 1], "Double Trouble III", quatre[3 - 1], 'Tag Team']
    shiva = [altair[1 - 1], altair[3 - 1], uno[2 - 1], uno[1 - 1], "Double Trouble III", quatre[3 - 1], 'Tag Team']

    avatar_fast = [amira[1 - 1], amira[2 - 1], seruel[3 - 1],
              sandalphon[3 - 1], 'Rage IV', 'Full Arsenal III',
              amira[3 - 1]]
    avatar = [amira[1-1],amira[2-1],seruel[2-1],seruel[3-1],
              sandalphon[1-1],sandalphon[3-1],'Rage IV','Full Arsenal III',
              amira[3-1]]
    metatron = ['Rage IV', 'Full Arsenal III',
                 djeanne[2 - 1], zoi[2 - 1], zoi[1 - 1],
                 vira[2 - 1], vira[4 - 1], bk[1 - 1],
                 orchid[1 - 1]]


    priorityList_ex = []

    priorityList_nm = ['Miserable Mist', 'Armor Break II ', 'Rage IV','Full Arsenal III','Splitting Spirit']

    priorityListDefault = ['Miserable Mist', 'Armor Break II ', 'Rage IV','Full Arsenal III','Clarity']
    priorityListDefault_dark = ['Miserable Mist', 'Armor Break II ', 'Rage IV','Full Arsenal III','Clarity',
                           djeanne[2-1],zoi[2-1],zoi[1-1],zoi[3-1],orchid[3-1],
                           vira[1-1],vira[2-1],vira[4-1],bk[1-1],bk[2-1],bk[3-1]]
    priorityListDefault_dark_fast = ['Rage IV', 'Full Arsenal III',
                                     djeanne[2 - 1], zoi[2 - 1], zoi[1 - 1],
                                     vira[2 - 1], vira[4 - 1], bk[1 - 1]]

    priorityListDefault_wind = ['Miserable Mist', 'Armor Break II ', 'Rage IV','Full Arsenal III','Clarity',
                                wjeanne[1-1],wjeanne[3-1],birdman[1-1],birdman[3-1],nio[1-1],nio[2-1],nio[3-1]]


    priorityList2 = basic
    priorityList3 = basic
    priorityList4 = basic
    priorityList5 = basic


    if current_raidname == 'Grimnir (Impossible).':
        priorityList_ex = grimnir[:]
        priorityList2 = ['Tag Team']
    elif current_raidname == 'Rosequeen Showdown Impossible.':
        priorityList_ex = rosequeen[:]
        priorityList2 = priorityListDefault_dark[:]
        priorityList3 = priorityListDefault_dark[:]
        priorityList4 = priorityListDefault_dark[:]
        priorityList5 = priorityListDefault_dark[:]
        priorityListDefault = priorityListDefault_dark[:]
    elif current_raidname == 'Lvl 100 Xeno Ifrit.':
        priorityList_ex = xenoifrit_fast[:]
        priorityList2 = xenoifrit_fast[:]
        priorityList3 = xenoifrit_fast[:]
        priorityList4 = xenoifrit_fast[:]
        priorityList5 = xenoifrit_fast[:]
        priorityListDefault = xenoifrit[:]
    elif current_raidname == 'Shiva (Impossible).':
        priorityList_ex = shiva[:]
        priorityList2 = shiva[:]
        priorityList3 = shiva[:]
        priorityList4 = shiva[:]
        priorityList5 = shiva[:]
        priorityListDefault = shiva[:]
    elif current_raidname == 'Avatar (Impossible).':
        priorityList_ex = avatar_fast[:]
        priorityList2 = avatar_fast[:]
        priorityList3 = avatar_fast[:]
        priorityList4 = avatar[:]
        priorityList5 = avatar[:]
        priorityListDefault = avatar[:]
    elif current_raidname == 'Metatron (Impossible).' or current_raidname == 'Luminiera Omega (Impossible).':
        priorityList_ex = metatron[:]
        priorityList2 = metatron[:]
        priorityList3 = metatron[:]
        priorityList4 = metatron[:]
        priorityList5 = metatron[:]
        priorityListDefault = priorityListDefault_dark_fast[:]

    if config.active_bot_quest != 0 and (config.questmode == 'gw' or config.questmode == 'event_special'):
        if skillCombosType == 'nm':
            priorityList_ex = xenoifrit[:]
            priorityList2 = xenoifrit[:]
            priorityList3 = xenoifrit[:]
            #TODO: why .append returns null
            priorityList4 = xenoifrit[:]
            priorityList5 = xenoifrit[:]
            priorityListDefault = xenoifrit[:]
        else:
            priorityList_ex = ex_fast[:]
            priorityList2 = ex_fast[:]
            priorityList3 = ex_fast[:]
            priorityList4 = ex_fast[:]
            priorityList5 = ex_fast[:]
            priorityListDefault = ex_fast[:]

    list.append(priorityList_ex) #turn1
    list.append(priorityList2) #turn2
    list.append(priorityList3) #turn3
    list.append(priorityList4) #turn4
    list.append(priorityList5) #turn5

    if int == 1:
        return list[0]
    elif int == 2:
        return list[1]
    elif int == 3:
        return list[2]
    elif int == 4:
        return list[3]
    elif int == 5:
        return list[4]
    else:
        return priorityListDefault


'''
Character skill names
'''
lyria = ["Rousing Wind +","Roaring Fire +",'','']
MC_reference = ['Miserable Mist', 'Armor Break II ', 'Rage IV','Full Arsenal III','Clarity',
                'Splitting Spirit',"Panacea III","Double Trouble III","Veil",'Tag Team']

#DIRT
gandalf = ['Speed',"Order +","Discord +"]
eugen = ['','','Autoignition']
cagliostro = ["Collapse ++","Phantasmagoria ++","Reinforce"]
arulumaya = ["Gaze into Crystal Ball","Heaven's Moon ++","Tabula Rasa ++","Nakshatra","End Gaze"]

#DARK
orchid =['Puppet Strings +','Ancestral Absorption +','Oblivion']
djeanne = ['Anti-Reversal +','Incision +','Eternal Chaos']
zoi = ['Resolution +','Conjuction +','Thunder']
bk = ['Quadspell +','Drain +','Acumen']
vira = ['Layer Rise II +','Evening Existance ++','Affection Oath +','Luminiera Merge']

#WATER
quatre = ["Gammadion Cross ++","Carnage ++","Avirati","Four-Sky's Sorrow"]
uno = ["Spiral Spear ++","Fleeting Spark ++","Arm the Bastion","One-Rift's Benediction"]
altair = ["Battleplan: Surround ++","Battleplan: Crane Down ++","Battleplan: Crescent Moon"]
diantha = ["Summer Encore +","Onstage +","Standing Ovation"]

#WIND
wjeanne = ['Reversal Tide +','Salvation +','Banner of the Brave']
birdman = ['Adamant Solace ++','Strike Solace +',"Stormwind's Solace +"]
nio = ['Ninanana +','Kuorria ++','Defandue +',"Nine-Realm's Security"]

#LIGHT
amira = ["Bal-Sagoth +","Power Within ++","Half-God Half-Demon +"]
sandalphon = ["Alone in Heaven +","Ecliptica +","The Power of One"]
seruel = ["Quick Raid ++","Royal Curtain ++","Regulus Gloria +"]