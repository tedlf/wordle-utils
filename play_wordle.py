import sys
from argparse import ArgumentParser

import wordle_util


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-a', '--answer')
    parser.add_argument('-g', '--guesses', nargs='+', default=[], help='Initial guesses')
    parser.add_argument('--hard-mode', action='store_true', default=False, help='Hard mode')
    parser.add_argument('--output-format', default='unicode', help="Output format ('unicode' or 'ascii')")
    args = parser.parse_args()

    if not args.guesses:
        print('You must enter at least one guess')
        sys.exit()
    if args.output_format not in ('unicode', 'ascii'):
        print("Output format must be 'unicode' or 'ascii'")
        sys.exit()

    print()
    wordle_util.play(args.answer, args.guesses, args.output_format, args.hard_mode)
    print()
