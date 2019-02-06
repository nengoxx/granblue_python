from functions import *

class Timer(object):
    '''Simple object to determine when we should refresh'''

    def __init__(self):
        functions.log('Timer created')
        self.start_time = time_now()

    def reset(self):
        self.start_time = time_now()

    def check_timeout(self, maxtime):
        if (time_now() - self.start_time) > maxtime:
            return True
        return False

