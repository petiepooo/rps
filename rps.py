#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' rps.py - an app to play rock paper scissors (lizard spock)
'''

from __future__ import print_function

class Game(object):
    ''' class for generalized rock/paper/scissors games '''
    def __init__(self, sequence='rock bends scissors cuts paper covers rock'):
        self.set_sequence(sequence)

    def set_sequence(self, sequence, strict=True):
        ''' sets the class variables based on the sequence
            takes string, outputs nothing
            string should be of form
            'obj1 action obj2 action ... action obj1'
        '''
        split_seq = sequence.split(' ')
        if strict and split_seq[0] != split_seq[-1]:
            raise ValueError('sequence must end and start with same object')

        self.count = 3
        length = len(split_seq) - 1
        while self.count * (self.count - 1) < length:
            self.count += 2
        if strict and self.count * (self.count - 1) != length:
            raise ValueError('sequence must have an odd object count with action between each')

        self.objects = []
        for index in range(0, length, 2):
            if split_seq[index] not in self.objects:
                self.objects.append(split_seq[index])
        if strict and len(self.objects) != self.count:
            raise ValueError('unexpected number of objects in sequence')

        offsets = []
        self.beats = []
        for index in range(0, length, 2):
            idx1 = self.objects.index(split_seq[index])
            idx2 = self.objects.index(split_seq[index + 2])
            diff = (idx2 - idx1) % self.count
            if diff not in offsets:
                offsets.append(diff)
                self.beats.append(list([None] * self.count), )
            offset = offsets.index(diff)
            self.beats[offset][idx1] = split_seq[index + 1]

        if strict and len(offsets) != self.count // 2:
            raise ValueError('sequence does not have full coverage between objects')

        self.beat_offset = [None] * self.count
        for idx, item in enumerate(offsets):
            self.beat_offset[item] = idx

    def is_valid_obj(self, obj):
        ''' validates obj, returns boolean '''
        try:
            _ = self.objects.index(obj)
        except ValueError:
            return False
        return True

    def result(self, obj1, obj2):
        ''' takes two players found in self.objects, prints results, returns second object '''
        diff = (self.objects.index(obj2) - self.objects.index(obj1)) % len(self.objects)
        if diff == 0:
            print('Tie ({0} vs. {0})'.format(obj1))
        else:
            winner, loser = obj1, obj2
            if self.beat_offset[diff] is None:
                diff = self.count - diff
                winner, loser = obj2, obj1
            action = self.beats[self.beat_offset[diff]][self.objects.index(winner)]
            if action:
                print('{} {} {}'.format(winner, action, loser))
            else:
                print('Unspecified ({} vs. {})'.format(obj1, obj2))
        return obj2	# allows reduce() to work


def main():
    ''' called when run from CLI '''
    import argparse
    from functools import reduce as reduce_func

    parser = argparse.ArgumentParser('Rock Paper Scissors game')
    parser.add_argument('-s', '--sheldon', help='enable lizard and spock', action='store_true')
    parser.add_argument('-t', '--test', help='print test sequence', action='store_true')
    parser.add_argument('-p', '--permissive', help='allow incomplete sequence', action='store_true')
    parser.add_argument('-c', '--custom', metavar='SEQ', help='use a custom sequence')
    parser.add_argument('objects', nargs='*')
    args = parser.parse_args()

    rps = Game()

    if args.custom:
        rps.set_sequence(args.custom, strict=not args.permissive)

    if args.sheldon:
        rps.set_sequence('scissors cuts paper covers rock crushes lizard poisons '
                         'spock smashes scissors decapitates lizard eats paper '
                         'disproves spock vaporizes rock bends scissors')
    if args.test:
        if args.sheldon:
            reduce_func(rps.result, ['scissors', 'paper', 'rock', 'lizard', 'spock',
                                     'scissors', 'lizard', 'paper', 'spock', 'rock'])
            print('and as it always has,')
            rps.result('rock', 'scissors')
        else:
            reduce_func(rps.result, ['scissors', 'paper', 'rock', 'scissors'])

    elif len(args.objects) > 1:
        for obj in args.objects:
            if not rps.is_valid_obj(obj):
                exit('ERROR: {} is not a valid object'.format(obj))
        reduce_func(rps.result, args.objects)
    else:
        print('nothing to do')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
