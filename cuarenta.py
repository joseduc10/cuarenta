#!/usr/bin/python
import random

class CuarentaDeck:
    SUITS = {'H':'Hearts', 'S':'Spades', 'C':'Clubs', 'D':'Diamonds'}
    RANKS = {str(i):i for i in xrange(2,8)}
    RANKS['A'] = 1; RANKS['J'] = 8; RANKS['Q'] = 9; RANKS['K'] = 10
    CARDS = [(j,i) for i in SUITS for j in RANKS]

    def __init__(self):
        self.deck = self.CARDS[:]

    def shuffle(self):
        random.shuffle(self.deck)

    def draw(self):
        if self.deck:
            return ''.join(self.deck.pop())
        else:
            return None

    def cardsLeft(self):
        return len(self.deck)

    def reset(self):
        self.deck = self.CARDS[:]

    def getCardValue(self,card):
        if card not in self.CARDS:
            raise Exception, "Invalid card %s" %card
        return self.RANKS[card[0]]

class Round:
    MERCY_RULE = 15
    SUM, HIT, LAY = 'sum','hit','lay'
    validMoves = [SUM,HIT,LAY]

    '''
        Represents a round of a match
    '''
    def __init__(self, players, deck):
        assert type(players) == list and len(players) == 2
        self.deck = deck
        self.players = players
        self.scores = [0,0]
        self.discardPiles = [0,0]
        self.tableCards = []
        self.lastMove = None
        self.lastCardPlayed = None
        self.curPlayer = None
        self.deckHolder =  None
        self.winner = None

    def start(self, firstPlayer=0):
        assert(firstPlayer in [0,1])
        self.curPlayer = firstPlayer
        self.deckHolder = (firstPlayer+1)%2
        self.deck.reset()
        self.deck.shuffle()
        while self.winner == None:
            if not self.deck.cardsLeft():
                self.resetDeck()
                continue
            self.playNextHand()

    def getGameState(self, hands):
        gameState = {'curPlayer': {}, 'oppPlayer': {}, 'discardPile':[]}
        gameeState['curPlayer'] = {'hand':hands[self.curPlayer], 
                                   'score':self.scores[self.curPlayer]}
        gameeState['oppPlayer'] = {'hand':hands[(self.curPlayer+1)%2], 
                                   'score':self.scores[(self.curPlayer+1)%2]}
        gameState['cardsOnTable'] = tableCards
        return gameState

    def playNextHand(self):
        hands = [[],[]]
        hands[self.curPlayer] = [self.deck.draw() for i in xrange(5)]
        hands[(self.curPlayer+1)%2] = [self.deck.draw() for i in xrange(5)]
        while self.winner != None and (hands[0] or hands[1]):
            print "It's %s's turn" %self.players[self.curPlayer].name
            gameSate = self.getGameState(hands)
            move = self.players[self.curPlayer].move(gameState)
            while not self.processMove(move, playerHand):
                print "Attempted invalid move"
                print move
                print "Try again"
                move = self.players[self.curPlayer].move(gameState)
            self.curPlayer = (self.curPlayer+1) % 2

    def resetDeck(self):
        self.deck.reset()
        self.deck.shuffle()
        self.deckHolder = (self.deckHolder+1)%2
        if self.discardPiles[0] > 19:
            pilePoints = (self.discardPiles-19) + 5
            if pilePoints % 2 == 1: 
                pilePoints += 1
                self.scores[0] += pilePoints
            if self.scores[0] >= 40 or pilePoints > MERCY_RULE:
                self.winner = 0
        elif self.discardPiles[1] > 19:
            pilePoints = (self.discardPiles-19) + 5
            if pilePoints % 2 == 1: 
                pilePoints += 1
                self.scores[1] += pilePoints
            if self.scores[2] >= 40 or pilePoints > MERCY_RULE:
                self.winner = 1
        self.discardPiles = [0,0]

    def processMove(self, move, playerHand):
        #check that player has the card they wish to play
        assert('cardPlayed' in move and  move['cardPlayed'] in playerHand)
        #check that player selected a valid move
        assert('moveType' in move and move['moveType'] in validMoves)
        #check that move object has valid fields
        assert('hitCards' in move and type(move['hitCards']) == list)
        assert(len(move['hitCards']) in [1,2])
        assert('carryCards' in move and type(move['carryCards']) == list)
        #check that cards to be hit are on the table
        if not (set(move['hitCards']) <= set(self.tableCards)):
            return False
        #check that cards to be carried are on the table
        if not (set(move['carryCards']) <= set(self.tableCards)):
            return False
        #check that the same card is not picked for hit and carry
        if set(move['hitCards']).intersection(set(move['carryCards'])):
            return False
        if not self.checkGameLogic(move):
            return False
        self.lastMove = move['moveType']
        self.lastCardPlayed = move['cardPlayed']    
        return True

    def checkGameLogic(self, move):
        #Game logic
        if move['moveType'] == LAY:
            self.tableCards.append(move['cardPlayed'])
        elif move['moveType'] == HIT:
            #check that the played card and card on table have the same value
            cardPlayed = move['cardPlayed']
            hitCard = move['hitCards'][0]
            if CuarentaDeck.getCardValue(cardPlayed) != CuarentaDeck.getCardValue(hitCard):
                return False
            #check that the carry cards form a valid straight
            carryCardValues = [CuarentaDeck.getCardValue(i) for i in move['carryCards']]
            carryCardValues.sort()
            checkStraight = CuarentaDeck.getCardValue(cardPlayed)+1
            for i in carryCardValues:
                if checkStraight != carryCardValues:
                    return False
                checkStraight += 1
            #update player's score if needed
            if self.lastMove == LAY and self.lastCardPlayed == hitCard:
                self.scores[self.curPlayer] += 2
                print "2 points for Caida"
            self.discardPiles[self.curPlayer].append(cardPlayed)
            #remove cards from table and add to player's pile
            self.discardPiles[self.curPlayer].append(\
                              self.tableCards.pop(self.tableCards.index(hitCard)))
            for card in move['carryCards']:
                self.discardPiles[self.curPlayer].append(\
                                  self.tableCards.pop(self.tableCards.index(card)))
        elif move['moveType'] == SUM:
            #check that card played sums to hit cards
            cardPlayed = move['cardPlayed']
            cardPlayedValue = CuarentaDeck.getCardValue(cardPlayed)
            hitCards = move['hitCards']
            hitCardValues = [CuarentaDeck.getCardValue(i) for i in hitCards]
            if cardPlayedValue > 7 or sum(hitCardValues) != cardPlayedValue:
                return False
            #check that the carry cards form a valid straight
            carryCardValues = [CuarentaDeck.getCardValue(i) for i in move['carryCards']]
            carryCardValues.sort()
            checkStraight = CuarentaDeck.getCardValue(cardPlayed)+1
            for i in carryCardValues:
                if checkStraight != carryCardValues:
                    return False
                checkStraight += 1
            self.discardPiles[self.curPlayer].append(cardPlayed)
            #remove cards from table and add to player's pile
            for card in move['hitCards']:
                 self.discardPiles[self.curPlayer].append(\
                                  self.tableCards.pop(self.tableCards.index(card)))
            for card in move['carryCards']:
                 self.discardPiles[self.curPlayer].append(\
                                   self.tableCards.pop(self.tableCards.index(card)))
        #update player's score
        if not self.tableCards:
            self.scores[self.curPlayer] += 2
            print "2 points for Limpia"
        return True


class Match:

    def __init__(self, players, rounds=3):
        '''
        Inputs:
        - players: list of players
        - rounds: positive odd integer. Number of rounds to play
        '''
        self.players = players
        self.deck = CuarentaDeck()
        self.scores = [0,0] 
        self.rounds = [Round(self.players, self.deck) for i in xrange(rounds)]

    def startGame(self):
        '''
        Main working function that manages the game.
        Inputs:
        - startPlayerDecision: function that decides which player goes first
        '''
        firstPlayer = random.randint(0,1)
        print "Starting Game"
        for i, round in enumerate(self.rounds):
            print "Round %d" %(i+1)
            round.start(firstPlayer)
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
        print "Round Score: %s %s - %s %s" %(r.players[0].name, r.scores[0], 
                                             r.players[1].name, r.scores[1])
        print "Global Score: %s %s - %s %s" %(self.players[0].name, self.scores[0], 
                                              self.players[1].name, self.scores[1])

    def printGameSummary(sel):
        print "Winner: %s" %r.winner.name
        print "Final Score: %s %s - %s %s" %(r.players[0].name, r.scores[0], 
                                             r.players[1].name, r.scores[1])


def testDeck():
    print "Starting test"
    print "Initialize cuarenta deck"
    deck = CuarentaDeck()
    print "Cards left in deck:", deck.cardsLeft()
    print "Drawing 10 cards"
    for i in xrange(10):
        print deck.draw()
        print "Cards left in deck:", deck.cardsLeft()
    print "Shuffling deck"
    deck.shuffle()
    print "Drawing 5 cards"
    for i in xrange(5):
        print deck.draw()
        print "Cards left in deck:", deck.cardsLeft()
    print "Resetting deck"
    deck.reset()
    print "Cards left in deck:", deck.cardsLeft()
    print "Finishing test"  

if __name__=="__main__": 
    testDeck()
