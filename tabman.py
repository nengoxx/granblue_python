'''
TAB AND WINDOW MANAGER

Locates the Chrome tabs and moves them in their correct positions & sizes

'''
import ctypes
import config
import functions
from functions import *

def getWindows():
    config.xscreensize,config.yscreensize = pyautogui.size()

    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    GetWindowText = ctypes.windll.user32.GetWindowTextW
    GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    IsWindowVisible = ctypes.windll.user32.IsWindowVisible

    MoveWindow = ctypes.windll.user32.MoveWindow

    titles = []
    tabs = []

    def foreach_window(hwnd, lParam):
        if IsWindowVisible(hwnd):
            length = GetWindowTextLength(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buff, length + 1)
            titles.append(buff.value)
            if buff.value == config.tabname:
                tabs.append(hwnd)

        return True

    EnumWindows(EnumWindowsProc(foreach_window), 0)

    # Set Windows
    #webdriver.set_window_position()
    i = 0
    for tab in tabs:
        MoveWindow(tab, i, 0, config.tabSize[0], config.tabSize[1], True)
        i += config.tabSize[0]

    functions.log("Active tabs: " + str(len(tabs)))    #+" - "+str(titles))


