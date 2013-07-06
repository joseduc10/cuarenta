#!/usr/bin/python
import random

class CuarentaDeck:

def __init__(self):
    self.suits = {1:'S', 2:'C', 3:'H', 4:'D'}
    self.ranks = {i:str(i) for i in range(2,8)}
    self.ranks[1] = 'A'; self.ranks[8] = 'J'; self.ranks[9] = 'Q'; self.ranks[10] = 'K'
    self.deck = [(self.suits[i],self.ranks[j]) for i in sorted(self.suits) for j in sorted(self.ranks)]

def shuffle(self):
    random.shuffle(self.deck)

def draw(self):
    return self.deck.pop()

def cardsLeft(self):
    return len(self.deck)

def reset(self):
    self.deck = [(self.suits[i],self.ranks[j]) for i in sorted(self.suits) for j in sorted(self.ranks)]

class Round:
    '''
        Represents a round of a match
    '''
def __init__(self):
    pass

class Match:
    GAME_TYPE_SOLO = 'SOLO'
    GAME_TYPE_TEAM = 'TEAM'

def __init__(self, players, matchType='SOLO', rounds=3, firstPlayer=None):
    '''
    Inputs:
    - players: list of players
    - matchType: either GAME_TYPE_SOLO or GAME_TYPE_TEAM
    - rounds: positive odd integer. Number of rounds to play
    - firstPlayer: integer in range [0,len(players)-1]. Starting player
    '''
    self.players = players
    self.deck = CuarentDeck()
    self.score = [0,0] 
    self.rounds = [Round(self.players, self.deck) for i in range(1,rounds+1)]
    self.firstPlayer = firstPlayer

def startGame(self, startPlayerDecision=None):
    '''
    Main working function that manages the game.
    Inputs:
    - startPlayerDecision: function that decides which player goes first
    '''
    #decide who starts
    if self.firstPlayer == None:
        startPlayerDecision = startPlayerDecision or self.highCard
    self.firstPlayer = startPlayerDecision()
    self.startPlayerDecision = startPlayerDecision or self.highCard
    print "Starting Game"
    for i, round in enumerate(self.rounds):
        print "Round %d" %(i+1)
        round.start(self.firstPlayer)
        self.score[round.winner] += 1
        print "Round ended"
        self.printRoundResults(round)
        print "------------------------"
    print "End of Game"
    self.printGameSummary()

def highCard(self):
    self.deck.shuffle()
    a,b = 0,0
    while a == b:
        a,b = self.deck.draw()[1], self.deck.draw()[1]
    return int(a > b)

def printResults(self, r):
print "Winner: %s" %r.players[r.winner].name
print "Round Score: %s %s - %s %s" %(r.players[0].name, r.scores[0], r.players[1].name, r.scores[1])
print "Global Score: %s %s - %s %s" %(self.players[0].name, self.scores[0], self.players[1].name, self.scores[1])

def printGameSummary(sel):
print "Winner: %s" %r.winner.name
print "Final Score: %s %s - %s %s" %(r.players[0].name, r.scores[0], r.players[1].name, r.scores[1])


def testDeck():
print "Starting test"
print "Initialize cuarenta deck"
deck = CuarentaDeck()
print "Cards left in deck:", deck.cardsLeft()
print "Drawing 10 cards"
for i in range(10):
print deck.draw()
print "Cards left in deck:", deck.cardsLeft()
print "Shuffling deck"
deck.shuffle()
print "Drawing 5 cards"
for i in range(5):
print deck.draw()
print "Cards left in deck:", deck.cardsLeft()
print "Resetting deck"
deck.reset()
print "Cards left in deck:", deck.cardsLeft()
print "Finishing test"  

if __name__=="__main__": testDeck()
