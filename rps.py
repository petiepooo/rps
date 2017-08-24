#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods
''' rps.py - an app to play rock paper scissors (lizard spock)
'''

class Game(object):
    ''' Abstract base class '''
    def __init__(self):
        self.beats = self.beats
        self.objects = self.objects
        count = len(self.beats)
        self.beat_offset = [None] + [x for x in range(count)] + [x - 1 for x in range(count, 0, -1)]
        self.player_offset = [None] + [0 for x in range(count)] + [1 for x in range(count, 0, -1)]

    def is_valid(self, obj):
        ''' validates obj
            returns boolean
        '''
        try:
            _ = self.objects.index(obj)
        except ValueError:
            return False
        return True

    def result(self, obj1, obj2):
        ''' prints the result of a comparison
            takes two players found in self.objects
            returns nothing
        '''
        diff = (self.objects.index(obj2) - self.objects.index(obj1)) % len(self.objects)
        if diff == 0:
            print('Noone wins')
        else:
            players = [obj1, obj2]
            winner = players[self.player_offset[diff]]
            action = self.beats[self.beat_offset[diff]][self.objects.index(winner)]
            loser = players[(self.player_offset[diff] + 1) % 2]
            print('{} {} {}'.format(winner, action, loser))
        return obj2	# allows reduce to work

class Rps(Game):
    ''' Rock Paper Scissors class '''
    def __init__(self):
        self.objects = ['rock', 'scissors', 'paper']
        self.beats = [['bends', 'cuts', 'covers']]
        super(Rps, self).__init__()

class Rpsls(Game):
    ''' Rock Paper Scissors Lizard Spock class '''
    def __init__(self):
        self.objects = ['rock', 'scissors', 'lizard', 'paper', 'spock']
        self.beats = [['bends', 'decapitates', 'eats', 'disproves', 'vaporizes'],
                      ['crushes', 'cuts', 'poisons', 'covers', 'smashes']]
        super(Rpsls, self).__init__()

def main():
    ''' called when run from CLI '''
    import argparse
    from functools import reduce

    parser = argparse.ArgumentParser('Rock Paper Scissors game')
    parser.add_argument('-s', '--sheldon', help='print Sheldon\'s explanation', action='store_true')
    parser.add_argument('-c', '--classic', help='use classic objects', action='store_true')
    parser.add_argument('objects', nargs='*')

    args = parser.parse_args()
    print(args)

    if args.classic:
        rps = Rps()
    else:
        rps = Rpsls()

    if args.sheldon:
        reduce(rps.result, ['scissors', 'paper', 'rock', 'lizard', 'spock',
                            'scissors', 'lizard', 'paper', 'spock', 'rock'])
        print('and as it always has,')
        rps.result('rock', 'scissors')

    else:
        for obj in args.objects:
            if not rps.is_valid(obj):
                print('ERROR: {} is not a valid object'.format(obj))
                return
        reduce(rps.result, args.objects)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

