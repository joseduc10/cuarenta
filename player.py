#!/usr/bin/python
import cuarenta

class InvalidPlayerNameError(Exception): pass

class Player:
    def __init__(self,name):
        if type(name) is not str:
            raise InvalidPlayerNameError, "name must be a string" 
        if not name.strip():
            raise InvalidPlayerNameError, "name must have characters other than spaces" 
        self.name = name 

    def move(self):
        raise NotImplementedError, "Method has not been implemented"

class HumanPlayer(Player):

    def move(self, gameState):
        self.printState(gameState)
        return self.requestMove(gameState)

    def printState(self, gameState):
        myCards = gameState['curPlayer']['hand']
        myScore = gameState['curPlayer']['score']
        oppScore = gameState['oppPlayer']['score']
        cardsOnTable = gameState['cardsOnTable']
        myDiscardPile = gameState['curPlayer']['discardPile']
        oppDiscardPile = gameState['oppPlayer']['discardPile']
        print "Opponent State"
        print "Score: %s" %oppScore
        print "Cards in Discard Pile: %s" %oppDiscardPile
        print "Your State"
        print "Score: %s" %myScore
        print "Cards in Discard Pile: %s" %myDiscardPile
        print "Hand: ", 
        for c in cards: print c,
        print "Cards on table:"
        for c in cards: print c,

    def requestMove(self, gameState):
        myCards = gameState['curPlayer']['hand']
        cardsOnTable = gameState['cardsOnTable']
        validMoves = Round.validMoves
        move = self.getTypeOfMove(validMoves)
        cardPlayed = self.getCardPlayed(myCards)
        hitCards, carryCards = [], []
        if hitCards != Round.LAY:
            hitCards, carryCards = self.getTableCards(cardsOnTable)
        moveObject = {'cardPlayed':cardPlayed, 'moveType':move,
                      'hitCards':hitCards, 'carryCards':carryCards}
        return moveObject

    def getTypeOfMove(self, validMoves):
        print "Select Type of Move:"
        for i, m in enumerate(validMoves):
            print "%s) %s" %(i+1,m.title())
        m = raw_input('> ')
        while m not in [str(i) for i in range(1,len(validMoves)+1)]:
            print "Invalid move. Try Again"
            m = raw_input('> ')
        return validMoves[int(m)-1]

    def getCardPlayed(self, cards):
        print "Select Card To Play:"
        for i, c in enumerate(cards):
            print "%s) %s" %(i+1,c.title())
        c = raw_input('> ')
        while c not in [str(i) for i in range(1,len(cards)+1)]:
            print "Invalid card. Try Again"
            c = raw_input('> ')
        return cards[int(c)-1]

    def getTableCards(self, cardsOnTable):
        hit, carry = [], []
        print "Select Cards To Hit:"
        for i, c in enumerate(cardsOnTable):
            print "%s) %s" %(i+1,c.title())
        c = raw_input('> ').split()
        while not (set(c) <= set([str(i) for i in range(1,len(cardsOnTable)+1)])) and \
                   len(set(c)) != len(c):
            print "Invalid card(s). Try Again"
            c = raw_input('> ').split()
        for i in c:
            hit.append(cardsOnTable[int(i)-1])
        print "Select Cards To Carry:"
        for i, c in enumerate(cardsOnTable):
            print "%s) %s" %(i+1,c.title())
        c = raw_input('> ').split()
        while not (set(c) <= set([str(i) for i in range(1,len(cardsOnTable)+1)])) and \
                   len(set(c)) != len(c):
            print "Invalid card(s). Try Again"
            c = raw_input('> ').split()
        for i in c:
            carry.append(cardsOnTable[int(i)-1])
        return hit, carry
