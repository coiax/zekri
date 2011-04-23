import collections

class Game(object):
    def __init__(self):
        pass

class Calander(object):
    def __init__(self,nightzero=False):
        self._timer = 2 #time // 2 for daynumber, % 2 for daynight
        self._beginning = ["Game Start"]
        if nightzero:
            self._beginning.append("Night 0")
    def __iter__(self):
        return self
    def next(self):
        # If there's stuff in the beginning queue
        if self._beginning:
            item = self._beginning.pop(0)
            return item

        # Else
        oldtimer = self._timer
        day = self._timer // 2
        daynight = self._timer % 2 # 0day, 1night

        if daynight == 0:
            item = "Day {0}".format(day)
        elif daynight == 1:
            item = "Night {0}".format(day)

        # Before we return stuff, increment the timer
        self._timer += 1
        return item

