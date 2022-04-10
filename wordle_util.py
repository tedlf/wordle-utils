import random
import sys
from collections import defaultdict

from words import wordle_dict
from wordle_solutions import wordle_solns as original_solutions
from candidate import Candidate
from guess_result import GuessResult
from dictionary_info import dictionary, default_entropy
from score_dictionary import calculate_entropy


def print_result_and_scores(print_type, count, result, scores=None):
    if print_type == 'unicode':
        if scores is None:
            print(f'{count + 1} {result}')
        else:
            print('{} {}\t{}'.format(count + 1, result, '\t'.join(str(round(abs(s), 4)) for s in scores)))
    elif print_type == 'ascii':
        if scores is None:
            print(f'{count + 1} {repr(result)}')
        else:
            print('{} {}\t{}'.format(count + 1, repr(result), '\t'.join(str(round(abs(s), 4)) for s in scores)))


def get_remaining_entries(guess_result, entry_pool=None):
    entry_pool = dictionary if entry_pool is None else entry_pool
    return [entry for entry in entry_pool if guess_result.is_possible(entry)]


def get_scored_candidates(entry_pool, remaining_guesses, number_rescues, hard_mode=False):
    relative_entropy = dict((entry, calculate_entropy(entry, entry_pool)) for entry in wordle_dict)
    scored_candidates = sorted((Candidate(e, (relative_entropy[e], 1, default_entropy[e])) for e in entry_pool), reverse=True)
    rescue_candidates = []
    if not hard_mode and remaining_guesses > 1:
        for rescue_entry in sorted(relative_entropy, key=lambda x: (relative_entropy[x], default_entropy[x]), reverse=True):
            if relative_entropy[rescue_entry] > relative_entropy[scored_candidates[0].entry]:
                rescue_candidates.append(Candidate(rescue_entry, (relative_entropy[rescue_entry], 0, default_entropy[rescue_entry])))
            if len(rescue_candidates) == number_rescues:
                rescue_candidates = sorted(rescue_candidates, reverse=True)
                break
    return scored_candidates, rescue_candidates


def play(answer, guesses, print_type=None, hard_mode=False):
    if answer is None:
        answer = random.choice(original_solutions)
    else:
        assert answer in dictionary, f'ERROR: {answer} is not in the dictionary'
    for guess in guesses:
        assert guess in dictionary, f'ERROR: {guess} is not in the dictionary'
    if print_type is not None:
        print(f'answer = {answer}\n')
    entry_pool = None
    for count, guess in enumerate(guesses):
        if hard_mode and entry_pool is not None and guess not in entry_pool:
            print(f'\nERROR: You are playing in hard mode, and the guess "{guess}" is inconsistent with earlier guess results.\n')
            sys.exit()
        guess_result = GuessResult(answer=answer, guess=guess)
        entry_pool = get_remaining_entries(guess_result, entry_pool)
        print_result_and_scores(print_type, count, guess_result)
        if guess_result.is_solution():
            return count + 1
    while True:
        count += 1
        candidates, rescue_candidates = get_scored_candidates(entry_pool, 6 - count, 1, hard_mode)
        candidate = candidates[0] if not rescue_candidates else rescue_candidates[0]
        guess_result = GuessResult(answer=answer, guess=candidate.entry)
        entry_pool = get_remaining_entries(guess_result, entry_pool)
        print_result_and_scores(print_type, count, guess_result, candidate.scores)
        if guess_result.is_solution():
            return count + 1
