#!/usr/bin/python
import unittest
import player

class PlayerTests(unittest.TestCase):

    def testPlayerNameIsAString(self):
        '''player name must be a string'''
        self.assertRaises(player.InvalidPlayerNameError, player.Player, 123)

    def testPlayerNameIsNotEmptyString(self):
        '''player name must not be empty'''
        self.assertRaises(player.InvalidPlayerNameError, player.Player, '')

    def testPlayerNameIsNotJustSpacesAndTabs(self):
        '''player name must have characters other than spaces, new lines, etc'''
        self.assertRaises(player.InvalidPlayerNameError, player.Player, '\n  \t')

    def testBasePlayerThrowsNotImplementedError(self):
        '''base player class does not have a move method implemented'''
        p = player.Player('Jose')
        self.assertRaises(NotImplementedError, p.move)

if __name__=='__main__':
    unittest.main()
