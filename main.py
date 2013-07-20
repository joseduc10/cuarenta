#!/usr/bin/python
from cuarenta import Match
from player import HumanPlayer

def main():
    players = [HumanPlayer('Sherlock'), HumanPlayer('Moriarti')]
    match = Match(players)

    match.startGame()

if __name__=='__main__':
    main()
