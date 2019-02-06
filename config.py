#config.py
#configuration file
from time import sleep, strftime

CHROME_ARGUMENTS = '--disable-infobars --disable-session-crashed-bubble'
CHROME_ARGUMENTS_TWITTER = '--disable-infobars --disable-session-crashed-bubble'
LOG_FILE = '[{}]asgbfBot.log'.format(strftime('%m-%d_%H%M'))

profile = 'profile' #Selenium chrome webdriver profile
base_dir = '.'

tabname = "Granblue Fantasy - Google Chrome"
xscreensize = 0
yscreensize = 0
tabposx = 0
tabposy = 0
browser_navigation_panel_width = 0
browser_navigation_panel_height = 0
tabSize = [417, 750]
mmto = [0.05, 0.2]  # Mouse Movement Time Offset = randomize from 0.2 to 0.4 seconds
coordOffset = [35,66] # offset for the button coordinates x,y
skillOffset = [25,25] # offset for skills when in combat
# Enter ID tab coordOffset = [35,66] # offset for the button coordinates x,y
smallCoordOffset = 1 #offset for the buttons from image matching

wait_until_seconds = 10
wait_until_less = 2.5
randomSleep = [0.5,1]
maxtimeFindRaid = 20*60 #20 min
runDefaultTimeout = 20*60 #time to w8 while one bot is active until it resets to the homepage

blueChestMaxPeople = 10 #maximum allowed people inside a blue chest raid to join in
blueChestMinHp = 75 #minimum hp threshold of a blue chest raid to join in

#dummy variables to get info on long periods of botting
totalExpGain = 0
totalRankGain = 0
raidsFinished = 0

username_rovax = 'PUT YOUR USERNAME HERE' #user name for combat(MC name) and double sliming purposes(Main account name)

'''
GENERIC POPUPS
'''
poperrs = ("This raid battle is full. You can't participate.",
           'This raid battle is already full.\nThe Home screen will now appear.',
           'This raid battle has already ended. The Home screen will now appear.',
           'This raid battle has already ended.',
           "The number that you entered doesn't match any battle.",
           "You're already taking part in this raid battle.",
           "You can only provide backup in up to three raid battles at once.")

poppending = "Check your pending battles."

'''
GAME LOCATIONS
'''
coop = 'http://game.granbluefantasy.jp/#coopraid'
torch = 'http://game.granbluefantasy.jp/#coopraid/room/entry/601431'
slime = 'http://game.granbluefantasy.jp/#coopraid/room/entry/601011'
joinraid = 'http://game.granbluefantasy.jp/#quest/assist'
raidfinder1 = 'http://gbf-raidfinder.aikats.us/'
pendingb = 'http://game.granbluefantasy.jp/#quest/assist/unclaimed'

#quests
gw_page = 'http://game.granbluefantasy.jp/#event/teamraid040'

test_trial = 'http://game.granbluefantasy.jp/#trial_battle'
special_daily = 'http://game.granbluefantasy.jp/#quest/extra'
featured_daily = 'http://game.granbluefantasy.jp/#quest/index'
shinyslime = 'http://game.granbluefantasy.jp/#quest/supporter/400181/4'
flying_sprout = 'http://game.granbluefantasy.jp/#quest/supporter/101121/3'

current_event = 'http://game.granbluefantasy.jp/#quest/extra/event/11013'

'''
SUMMONS
'''
summonDefCoords = [0,0,0,0] #[x, y, width, height] default coords for the 1st summon, dummy variable

'''
COMBAT
'''
attackDefCoords = [0,0,0,0] #attack button default coords, dummy variable to get the coords ingame
maxWtillCombat = 30
maxWbetweenAttacks = 30
maxCombaTime = 60 * 5 #TODO: dinamically adjust by raid or if we have cheatengine running
attackskip = 1

'''
GENERAL TELEGRAM
'''
telegram_bot = ''
telegram_chatId = 'PUT CHAT ID HERE'
telegram_token = 'PUT TELEGRAM TOKEN HERE'
useBerries = False
usePots = True #true by default since we're not gonna use this bot for anything else than spamming
minBP = 6 #minimum bp to find a raid, let some to play with
minap = 40
questmode = 'gw' #test_trial, gw, sslime, halo, trial, event_special, fav
questmodes = ['test_trial', 'gw', 'sslime', 'halo', 'trial', 'event_special', 'showdown', 'fav']
donm = True #does NM event quests TODO: global for gw and others
gwmode = 'nm' #gw quest to spam: ex , nm
gwmodes = ['ex','nm']
active_bot_coop = 0
active_bot_raidfinder = 0
active_bot_quest = 0
vpaused = False #pause variable for verification purposes only
paused = False

'''
VERIFICATION
'''
verifytext = ('Verify','Verification','verify','verification','VERIFY','VERIFICATION',
              'captcha','automated','tools')
falsepositives = [{'class': 'page', 'type': 'text/css'}, #this one seems like the actual verification button's css
                  {'id': 'tpl-pop-twitter-auth', 'type': 'text/template'}, #in combat
                  {'id': 'tpl-pop-post-twitter', 'type': 'text/template'}, #in combat
                  {'id': 'tpl-pop-re-post-twitter', 'type': 'text/template'}, #in combat
                  {'id': 'tpl-pop-re-post-twitter', 'type': 'text/template'}, #in combat
                  {'id': 'tpl-pop-selectable-campaign', 'type': 'text/template'}] #in mypage

'''
MAIN BOT OBJECTS
'''
#to reference outside its respective methods
AP = 0
BP = 0
user_main = ''

lastmsg = ''
BOT_RAIDFINDER = ''
BOT_COOP = ''
BOT_QUEST = ''
pending_raid_hrefs = []
