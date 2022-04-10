import sys
from argparse import ArgumentParser

import wordle_util
from guess_result import GuessResult


def main(result_strings, number, rescue_number, hard_mode, print_type):
    print()
    entry_pool = None
    for i, result_str in enumerate(result_strings):
        guess_result = GuessResult(result_str=result_str)
        entry_pool = wordle_util.get_remaining_entries(guess_result, entry_pool)
        wordle_util.print_result_and_scores(print_type, i, guess_result)
    print()

    candidates, rescue_candidates = wordle_util.get_scored_candidates(entry_pool, 6 - len(result_strings), rescue_number, hard_mode)
    if rescue_candidates:
        print(f'Here are the top {len(rescue_candidates)} rescue suggestions:\n')
        for rescue_candidate in rescue_candidates:
            print(rescue_candidate)
        print()
    if len(candidates) == 1:
        print(f'Found one candidate after {len(result_strings)} guesses:')
    elif len(candidates) > number:
        print(f'Found {len(candidates)} candidates after {len(result_strings)} guesses. Here are the first {number}:')
    else:
        print(f'Found {len(candidates)} candidates after {len(result_strings)} guesses:')
    print()
    for candidate in candidates[:number]:
        print(candidate)
    print()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-r', '--results', nargs='+', default=[], help='Results of previous guesses')
    parser.add_argument('-n', '--number', type=int, default=20, help='Number of suggestions')
    parser.add_argument('--rescue', type=int, default=5, help='Number of rescue suggestions')
    parser.add_argument('--hard-mode', action='store_true', default=False, help='Hard mode')
    parser.add_argument('--output-format', default='unicode', help="Output format ('unicode' or 'ascii')")
    args = parser.parse_args()

    if args.output_format not in ('unicode', 'ascii'):
        print("Output format must be 'unicode' or 'ascii'")
        sys.exit()

    main(args.results, args.number, args.rescue, args.hard_mode, args.output_format)
