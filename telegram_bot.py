import traceback

import telegram
from selenium.webdriver.common.keys import Keys
from telegram.ext import Updater
from telegram.ext import CommandHandler
import time

import functions
import config

'''
Commands:
/start - demo
/screen - screenshots 1st instance
/pause - pauses the bot 
/qch <mode> - changes quest or gw quest mode to 'mode'
/berries - changes spam usage of berries 
/capcha <capcha> - inputs 'capcha' as the captcha text in the verification dialog
/vpause - pauses the bot after verification has triggered
'''

def setupTelegram():
    config.telegram_bot = telegram.Bot(token=config.telegram_token)
    print(config.telegram_bot.get_me())

    updater = Updater(token=config.telegram_token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    screenshot_handler = CommandHandler('screen', screenshot)
    inputCapcha_handler = CommandHandler('capcha', inputCapcha)
    vpause_handler = CommandHandler('vpause', vpause)
    pause_handler = CommandHandler('pause', pause)
    berries_handler = CommandHandler('berries', switchBerries)
    quest_handler = CommandHandler('qch', changeQuest)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(screenshot_handler)
    dispatcher.add_handler(inputCapcha_handler)
    dispatcher.add_handler(vpause_handler)
    dispatcher.add_handler(pause_handler)
    dispatcher.add_handler(berries_handler)
    dispatcher.add_handler(quest_handler)

    updater.start_polling()


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def screenshot(bot, update):
    try:
        driver = ''
        if config.BOT_COOP:
            driver = config.BOT_COOP.gbf
        if config.BOT_RAIDFINDER:
            driver = config.BOT_RAIDFINDER.gbf
        if config.BOT_QUEST:
            driver = config.BOT_QUEST.gbf

        functions.saveScreenshot(driver)
        sendTelegramScreenShot()

    except Exception:
        traceback.print_exc()
        pass

def sendTelegramMsg(msg):
    config.telegram_bot.send_message(chat_id=config.telegram_chatId, text=msg)

def sendTelegramScreenShot():
    try:
        config.telegram_bot.send_photo(chat_id=config.telegram_chatId, photo=open('screen/screen.png', 'rb'))
    except Exception:
        traceback.print_exc()
        pass

def inputCapcha(bot, update):
    try:
        driver = ''
        if config.BOT_COOP:
            driver = config.BOT_COOP.gbf
        if config.BOT_RAIDFINDER:
            driver = config.BOT_RAIDFINDER.gbf
        if config.BOT_QUEST:
            driver = config.BOT_QUEST.gbf

        text_area = functions.find_visible_class(driver,'frm-message', single=True)
        #text_area.send_keys(Keys.CONTROL, "a")
        #text_area.send_keys(Keys.DELETE)
        capchatext = update.message['text']
        if capchatext == '/capcha':
            config.telegram_bot.send_message(chat_id=config.telegram_chatId, text='Usage: /capcha <capcha>')
            return
        capchatext = capchatext.split(' ')[1]
        text_area.send_keys(capchatext)
        functions.clickButton('btn-talk-message', driver, verify=False)
        time.sleep(2)
        functions.saveScreenshot(driver)
        sendTelegramScreenShot()

    except Exception:
        traceback.print_exc()
        pass

def vpause(bot, update):
    config.vpaused = not config.vpaused
    config.telegram_bot.send_message(chat_id=config.telegram_chatId, text='VPaused: '+str(config.vpaused))

def pause(bot, update):
    config.paused = not config.paused
    config.telegram_bot.send_message(chat_id=config.telegram_chatId, text='Paused: '+str(config.paused))

def switchBerries(bot, update):
    config.useBerries = not config.useBerries
    config.telegram_bot.send_message(chat_id=config.telegram_chatId, text='Use Berries: '+str(config.useBerries))

def changeQuest(bot, update):
    try:
        text = update.message['text']
        if text != '/qch': #if its only /qch (no args) do nothing
            text = text.split(' ')[1]
        if text in config.questmodes:
            config.questmode = text
        elif text in config.gwmodes:
            config.gwmode = text
        else:
            config.telegram_bot.send_message(chat_id=config.telegram_chatId, text='Invalid quest mode.\nQuest Modes:\n'
                                                                                  +str(config.questmodes)+'\nGW Modes:\n'
                                                                                  +str(config.gwmodes))
        config.telegram_bot.send_message(chat_id=config.telegram_chatId, text='Quest Mode: ' + str(config.questmode))
        config.telegram_bot.send_message(chat_id=config.telegram_chatId, text='GW Mode: ' + str(config.gwmode))
    except Exception:
        traceback.print_exc()
        pass