import config
import argparse
from sys import argv

from seleniumrequests import Chrome
from selenium import webdriver

import coop
import raidfinder
import quest
from tabman import *
from functions import *

import cProfile
import psutil


def init():
    check_ap(GBF)
    check_bp(GBF)
    check_name(GBF)

    #side borders are both the same size so the offset is half of it
    config.browser_navigation_panel_width = GBF.execute_script('return window.outerWidth - window.innerWidth;')/2
    config.tabposx = GBF.get_window_position()['x'] + config.browser_navigation_panel_width
    # quick fix to substract just the lower part of the screen, and get the offset for the upper part(should be similar to the side borders
    config.browser_navigation_panel_height = GBF.execute_script('return window.outerHeight - window.innerHeight;')-config.browser_navigation_panel_width
    config.tabposy = GBF.get_window_position()['y'] + config.browser_navigation_panel_height
    #log("Browser width offset: " + str(config.browser_navigation_panel_width)+ "px")
    #log("Browser height offset: " + str(config.browser_navigation_panel_height) + "px")
    #log('Tab position: '+str(config.tabposx)+','+str(config.tabposy))
    mloop()

def mloop():
    while 1:
        if config.active_bot_coop:
            config.BOT_COOP = coop.make_coopbot(GBF)
            config.BOT_COOP.run()
        elif config.active_bot_raidfinder:
            config.BOT_RAIDFINDER = raidfinder.make_raidfinder(GBF)
            config.BOT_RAIDFINDER.run()
        elif config.active_bot_quest:
            config.BOT_QUEST = quest.make_questbot(GBF)
            config.BOT_QUEST.run()

def main():
    log("A Simple Granblue Fantasy Bot started")
    global GBF
    timestart = time_now()
    profile = path.abspath(".\\" + config.profile)

    parser = argparse.ArgumentParser(prog='asgfb.py',
                                     description='A Simple Granblue Fantasy Bot',
                                     usage='asgfb.py [profile] [options]\nexample: python asgfb.py profile2 -s',
                                     formatter_class=argparse.MetavarTypeHelpFormatter)

    parser.add_argument('profile', nargs='?',
                        help='overwrites the default profile path', type=str)

    parser.add_argument('--login', '-l',
                        help='pauses the script upon starting up to allow logging in', action='store_true')
    parser.add_argument('--start', '-s',
                        help='starts the script', action='store_true')
    parser.add_argument('--coop', '-c',
                        help='starts the script(coop slime)', action='store_true')
    parser.add_argument('--quest', '-q',
                        help='starts the script(quest bot)', action='store_true')
    parser.add_argument('--berries', '-b',
                        help='uses berries to spam joining raids', action='store_true')

    args = parser.parse_args()

    if len(argv) == 1:
        parser.print_help()
        quit()

    if args.profile is not None:
        log('Changing profile path to {}'.format(args.profile))
        profile = path.abspath('.\\' + args.profile)

    options = webdriver.ChromeOptions()
    log('Using profile at: {}'.format(profile))
    options.add_argument('user-data-dir=%s' % profile)
    for cargs in config.CHROME_ARGUMENTS.split():
        options.add_argument(cargs)
    GBF = Chrome(chrome_options=options)
    GBF.get('http://game.granbluefantasy.jp/#mypage')
    
    #TODO better window handling
    getWindows()
    setupTelegram()
    #for p in psutil.process_iter():
        #log(str(p.name()))
    if "cheatengine-x86_64.exe" in (p.name() for p in psutil.process_iter()):
        config.maxCombaTime = 20 * 60 #4 times
        #config.runDefaultTimeout = 80 * 60
        log('CheatEngine found, max combat time: '+str(config.maxCombaTime)+' seconds')
        #log('CheatEngine found, max run time: ' + str(config.runDefaultTimeout) + ' seconds')

    if args.login:
        log('Pausing to login')
        input('Press enter to continue...')

    if args.berries:
        log('Using Berries!')
        config.useBerries = True

    if args.start:
        input('Press any key to start botting...')
        log('Starting raid finder bot...')
        config.active_bot_raidfinder = 1
        init()
    
    if args.coop:
        input('Press any key to start botting...')
        log('Starting co-op bot...')
        config.active_bot_coop = 1
        init()
    
    if args.quest:
        input('Press any key to start botting...')
        log('Starting quest bot...')
        config.active_bot_quest = 1

        cProfile.run('init()', 'restats')
        #init()

    input('Press enter to exit...')

    GBF.close()
    quit()






if __name__ == '__main__':
    #TIMER = timer.Timer()
    #config.init()

    try:
        main()
    except TimeoutException:
        raise
    except (ConnectionResetError, ConnectionError,
                ConnectionAbortedError):
        #GBF.close()
        raise
    except Exception:
        traceback.print_exc()
        raise