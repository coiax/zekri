import collections
import logging
import random
logger = logging.getLogger(__name__)

class Game(object):
    def __init__(self):
        self._counter = 0

        self.usernameid = {}
        self.players = set() # contains player ID

        self.aliveplayers = set()
        # is a subset of players. These are people who can vote.

        self.playerroles = {}
        self.votetracker = {}
    def register(self,username):
        id = self._counter
        self._counter += 1

        self.usernameid[username] = id
        self.players.append(id)
    def unregister(self,username):
        id = self.usernameid.pop(username,None)
        if id not in self.players:
            logger.getChild("game.unregister").warn("{0} is not a registered user.".format(username))
        self.players.discard(id)

    def assign_roles(self,roles):
        if self.playerroles != {}:
            raise MafiaException("Game has already assigned roles.")

        roles = list(roles)
        random.shuffle(roles)

        ids = list(self.players)

        if len(ids) != len(roles):
            raise MafiaException("Wrong number of roles; want {0}, got {1}".format(len(ids),len(roles)))

        while roles:
            role = roles.pop()
            id = ids.pop()
            self.playerroles[id] = role

    def start_game(self):
        self.aliveplayers = self.players.copy()

    def vote(self,playerid,votingfor):
        if playerid not in self.aliveplayers:
            playername = self.usernameid[playerid]
            s = "Player {0} (id={1}) is not alive, and cannot vote.".format(playername,playerid)
            raise MafiaException(s)
        # The special votingfor id of -1 indicates No Lynch or Skip to Night
        self.votetracker[playerid] = votingfor
    def unvote(self,playerid):
        if playerid not in self.aliveplayers:
            playername = self.usernameid[playerid]
            s = "Player {0} (id={1}) is not alive, and cannot unvote.".format(playername,playerid)
            raise MafiaException(s)
        del self.votetracker[playerid]

    def tabulate_vote(self):
        """Returns a dict mapping ids to people voting for those ids"""
        tally = collections.defaultdict(list)

        for playerid,votingfor in self.votetracker.items():
            tally[votingfor].append(playerid)
        return tally
    def nonvoters(self):
        """Returns a set of the playerids who aren't voting"""
        voters = set(self.votetracker.keys())
        # Woo, set subtraction
        return self.players - voters
    def check_majority(self):
        """Returns the id if any of the voting options has reached a majority,
        otherwise false"""
        tally = self.tabulate_vote()
        needed = majority(len(self.aliveplayers))
        for target,people in tally.items():
            if len(people) >= majority:
                return target
        return False


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

class MafiaException(Exception):
    pass

def majority(num):
    """Returns the number for a majority. Breaks down if num is 2 or less."""
    if num < 3:
        logger.warn("{0} passed to majority function.".format(num))
    return (num // 2) + 1
