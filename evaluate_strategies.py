# Evaluate two word opening strategies

from argparse import ArgumentParser
from collections import defaultdict

import score_dictionary
import wordle_util
from dictionary_info import dictionary, default_entropy
from guess_result import GuessResult

OUTPUT_FILE = 'strategy_rankings.csv'


def get_filtered_entries(filter, number):
    filter_set = set(filter)
    entries = []
    for entry in dictionary:
        entry_set = set(entry)
        # Exclude words with repeated letters
        if len(entry_set) == 5 and not filter_set & entry_set:
            entries.append(entry)
        if len(entries) == number:
            break
    return entries


def get_strategies(number):
    strategies = []
    first_words = []
    for entry in dictionary:
        if len(set(entry)) == 5:
            first_words.append(entry)
        if len(first_words) == number:
            break
    for first_word in first_words:
        for second_word in get_filtered_entries(first_word, number):
            strategies.append((first_word, second_word))
    return strategies


def get_number_remaining(guess_results, entry_pool=dictionary):
    number_remaining = 0
    for entry in entry_pool:
        if all(r.is_possible(entry) for r in guess_results):
            number_remaining += 1
    return number_remaining


def evaluate_strategy(guesses, candidate_pool=dictionary):
    histogram = defaultdict(int)
    for answer in candidate_pool:
        guess_results = [GuessResult(answer=answer, guess=guess) for guess in guesses]
        if any(r.is_solution() for r in guess_results):
            histogram[0] += 1
        else:
            histogram[get_number_remaining(guess_results)] += 1
        # Compute the average number of candidates
        avg_candidates = sum(count * histogram[count] for count in histogram) / sum(histogram.values())
        # Compute the cumulative probability of the number of candidates being less than or equal to the number of remaining guesses
        cum_prob = sum(histogram[count] for count in range(7 - len(strategy))) / sum(histogram.values())
        first_entry_pool = wordle_util.get_remaining_entries(guess_results[0])
        second_entropy = score_dictionary.calculate_entropy(guesses[1], first_entry_pool)
    return avg_candidates, cum_prob, second_entropy


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-n', '--number', type=int, default=10)
    args = parser.parse_args()

    strategies = get_strategies(args.number)
    with open(OUTPUT_FILE, 'w') as output_file:
        output_file.write('guess1,guess2,avg_candidates,cumsum4,H0(guess1),H1(guess2),H_total\n')
        for i, strategy in enumerate(strategies):
            first_word, second_word = strategy
            print(i, first_word, second_word)
            avg_candidates, cum_prob, second_entropy = evaluate_strategy(strategy)
            total_entropy = default_entropy[first_word] + second_entropy
            output_file.write(
                f'{first_word},{second_word},{avg_candidates},{cum_prob},{default_entropy[first_word]},{second_entropy},{total_entropy}\n'
            )
