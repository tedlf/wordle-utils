# If the human player wins, the final utility of the game is the number of guesses required.
# If Adversarial Wordle wins, the final utility of the game is 100 (any number greater than 6 would work).

import sys

import wordle_util
from guess_result import GuessResult
from argparse import ArgumentParser


class WordleState:
    def __init__(self, guess_results, possible_solutions, guess):
        self.guess_results = guess_results
        self.possible_solutions = possible_solutions
        self.guess = guess

    def get_player(self):
        """ Return 1 for Adversarial Wordle, -1 for Human player """
        if self.guess is not None:
            return 1
        else:
            return -1

    def print_state(self, print_type):
        for i, result in enumerate(self.guess_results):
            wordle_util.print_result_and_scores(print_type, i, result)

    def __str__(self):
        return f"[{', '.join(r.entry for r in self.guess_results)}]({self.guess})[{', '.join(self.possible_solutions)}]"


class WordleGame:
    def __init__(self, result_strings, guess):
        entry_pool = None
        guess_results = []
        for result_str in result_strings:
            guess_result = GuessResult(result_str=result_str)
            entry_pool = wordle_util.get_remaining_entries(guess_result, entry_pool)
            for earlier_result in guess_results:
                if not earlier_result.is_possible(guess_result.entry):
                    print(f'WARNING: the guess "{guess_result.entry}" is inconsistent with guess result {earlier_result}.')
                    print()
            guess_results.append(guess_result)
        if guess not in entry_pool:
            print(f'WARNING: the guess "{guess}" is inconsistent with earlier guess results.')
            print()
        self.start_state = WordleState(guess_results, entry_pool, guess)

    def actions(self, state):
        return state.possible_solutions

    def successor(self, state, action):
        if state.get_player() == 1:
            # Adversarial Wordle: report the result of the most recent guess and reduce the list of possible solutions
            latest_guess_result = GuessResult(answer=action, guess=state.guess)
            return WordleState(
                state.guess_results + [latest_guess_result],
                wordle_util.get_remaining_entries(latest_guess_result, state.possible_solutions),
                None,
            )
        else:
            # Human player: choose the next guess
            return WordleState(state.guess_results, state.possible_solutions, action)

    def check_result(self, state):
        """ Return (is_end, score) """
        if state.guess_results[-1].is_solution():
            return True, len(state.guess_results)
        elif len(state.guess_results) == 6:
            return True, 100
        else:
            return False, None

    def utility(self, state):
        is_end, result = self.check_result(state)
        assert is_end
        return result


def alpha_beta_policy(game, state):
    def recurse(state, alpha, beta):
        """ Return (utility, action that achieves that utility) """
        is_end, result = game.check_result(state)
        if is_end:
            return result, None
        if state.get_player() == 1:
            value = -float('inf')
            best_action = None
            for action in game.actions(state):
                candidate = recurse(game.successor(state, action), alpha, beta)[0]
                if candidate > value:
                    value, best_action = candidate, action
                if value >= beta:
                    break
                alpha = max(alpha, value)  # fail-hard alpha-beta
            return value, best_action
        else:
            value = float('inf')
            best_action = None
            for action in game.actions(state):
                candidate = recurse(game.successor(state, action), alpha, beta)[0]
                if candidate < value:
                    value, best_action = candidate, action
                if value <= alpha:
                    break
                beta = min(beta, value)  # fail-hard alpha-beta
            return value, best_action

    _, action = recurse(state, -float('inf'), float('inf'))
    return action


def main(result_strings, guess, print_type):
    game = WordleGame(result_strings, guess)
    state = game.start_state
    while not game.check_result(state)[0]:
        action = alpha_beta_policy(game, state)
        state = game.successor(state, action)

    print()
    state.print_state(print_type)
    print()
    print('Final utility of this game is {}'.format(game.utility(state)))
    print()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-r', '--results', nargs='+', default=[], help='Results of previous guesses')
    parser.add_argument('-g', '--guess', help="Human player's next guess")
    parser.add_argument('--output-format', default='unicode', help="Output format ('unicode' or 'ascii')")
    args = parser.parse_args()

    if args.results is None:
        print('You must enter at least one result (preferably two or more)')
        sys.exit()
    if args.guess is None:
        print('You must enter a guess')
        sys.exit()
    if args.output_format not in ('unicode', 'ascii'):
        print("Output format must be 'unicode' or 'ascii'")
        sys.exit()

    main(args.results, args.guess, args.output_format)
