import sys
from argparse import ArgumentParser
from collections import defaultdict

import wordle_util
from wordle_solutions import wordle_solns as original_solutions


def main(guesses, input_filename, hard_mode):
    histogram = defaultdict(int)
    if input_filename is not None:
        with open(input_filename) as input_file:
            target_words = [line.strip() for line in input_file.readlines()]
    else:
        target_words = original_solutions
    for i, answer in enumerate(target_words):
        histogram[wordle_util.play(answer, guesses, hard_mode=hard_mode)] += 1
        if i % 100 == 0:
            print(i)
    print()
    print(f'histogram for {guesses}')
    for number in sorted(histogram):
        print(f'{number},{histogram[number]}')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-g', '--guesses', nargs='+', default=[], help='Initial guesses')
    parser.add_argument('--file', help='Use input file instead of solution list')
    parser.add_argument('--hard-mode', action='store_true', help='Use hard mode')
    args = parser.parse_args()

    if not args.guesses:
        print('You must enter at least one guess')
        sys.exit()

    main(args.guesses, args.file, args.hard_mode)
