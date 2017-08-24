#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' rps.py - an app to play rock paper scissors (lizard spock)
'''

from __future__ import print_function

class Game(object):
    ''' class for generalized rock/paper/scissors games '''
    def __init__(self, sequence='rock bends scissors cuts paper covers rock',
                 debug=False, strict=True):
        self.debug = debug
        self._set_sequence(sequence, strict=strict)

    def _set_sequence(self, sequence, strict=True):
        ''' sets the class variables based on the sequence
            takes string, outputs nothing
            class variables:
               count - the number of objects
               objects - a list of the objects
               beats - a list of lists of actions
               beat_offset - offset into beats list for list to use for diff between objects
        '''
        split_seq = sequence.split(' ')
        if strict and split_seq[0] != split_seq[-1]:
            raise ValueError('SEQ must start and end with the same object')

        length = len(split_seq)
        # refactor; classic list comprehension pattern
        self.objects = list()
        for index in range(0, length, 2):
            if split_seq[index] not in self.objects:
                self.objects.append(split_seq[index])
        self.count = len(self.objects)
        if self.debug:
            print('length: {}, count: {}'.format(length, self.count))
            print('objects: {}'.format(self.objects))
        if strict and self.count * (self.count - 1) != length - 1:
            raise ValueError('SEQ must have an odd object count with an action between each')

        offsets = list()
        self.beats = list()
        self.beat_offset = [None] * self.count
        for index in range(0, length - 2, 2):
            if split_seq[index + 1] != '-':
                idx1 = self.objects.index(split_seq[index])
                idx2 = self.objects.index(split_seq[index + 2])
                diff = (idx2 - idx1) % self.count
                if diff not in offsets:
                    offsets.append(diff)
                    self.beat_offset[diff] = len(self.beats)
                    self.beats.append(list([None] * self.count))
                self.beats[offsets.index(diff)][idx1] = split_seq[index + 1]
        if self.debug:
            print('beats: {}'.format(self.beats))
            print('beat_offset: {}'.format(self.beat_offset))
        if strict and len(offsets) != self.count // 2:
            raise ValueError('SEQ must have only one action between object pairs')
        if strict and len([y for x in self.beats for y in x if y is None]):
            raise ValueError('SEQ must have an action between all opject pairs')

    def action(self, obj1, obj2):
        ''' takes two players found in self.objects, returns action '''
        winner = obj1
        index = self.objects.index(winner)
        diff = (self.objects.index(obj2) - index) % len(self.objects)
        offset = self.beat_offset[diff]
        if self.debug:
            print('difference: {}, offset: {}, index: {}'.format(diff, offset, index))

        if diff == 0:
            return 'ties', False
        else:
            if offset is None or self.beats[offset][index] is None:
                winner = obj2
                index = self.objects.index(winner)
                diff = self.count - diff
                offset = self.beat_offset[diff]
                if self.debug:
                    print('swapping sides; offset: {}, index: {}'.format(offset, index))

            if offset is None or self.beats[offset][index] is None:
                return None, False

            else:
                return self.beats[offset][index], winner == obj2

    def iterate(self, objects):
        ''' iterate through a list of objects, calling self.action() for each pair '''
        for obj1, obj2 in zip(objects, objects[1:]):
            action, swapped = self.action(obj1, obj2)
            if swapped:
                obj1, obj2 = obj2, obj1
            if action:
                print('{} {} {}'.format(obj1, action, obj2))
            else:
                print('{} and {} have no winner'.format(obj1, obj2))

    def is_valid_obj(self, obj):
        ''' validates obj, returns boolean '''
        try:
            _ = self.objects.index(obj)
        except ValueError:
            return False
        return True

def main():
    ''' called when run from CLI '''
    from argparse import ArgumentParser

    parser = ArgumentParser(description='Rock Paper Scissors game',
                            epilog='SEQ format: "rock bends scissors cuts paper covers rock"')
    parser.add_argument('-d', '--debug', help='enable debug output', action='store_true')
    parser.add_argument('-t', '--test', help='print test output', action='store_true')
    parser.add_argument('-p', '--permissive', help='allow incomplete sequence', action='store_true')
    seq = parser.add_mutually_exclusive_group()
    seq.add_argument('-s', '--sheldon', help='enable lizard and spock', action='store_true')
    seq.add_argument('-c', '--custom', metavar='SEQ', help='use a custom sequence')
    parser.add_argument('objects', help='eg. rock, paper, and scissors (>= 2)', nargs='*')
    args = parser.parse_args()
    if args.debug:
        print(args)

    if args.sheldon:
        rps = Game(sequence='scissors cuts paper covers rock crushes lizard poisons '
                            'spock smashes scissors decapitates lizard eats paper '
                            'disproves spock vaporizes rock bends scissors',
                   debug=args.debug)
    elif args.custom:
        rps = Game(sequence=args.custom, debug=args.debug, strict=not args.permissive)
    else:
        rps = Game(debug=args.debug)

    if args.test:
        rps.iterate(['scissors', 'paper', 'rock'])
        if args.sheldon:
            rps.iterate(['rock', 'lizard', 'spock', 'scissors', 'lizard', 'paper', 'spock', 'rock'])
            print('and as it always has,')
        rps.iterate(['rock', 'scissors'])
    elif len(args.objects) > 1:
        for obj in args.objects:
            if not rps.is_valid_obj(obj):
                exit('ERROR: {} is not a valid object'.format(obj))
        rps.iterate(args.objects)
    else:
        parser.print_usage()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
