# The Wordle Programming Challenge #

[Wordle](https://www.nytimes.com/games/wordle/index.html) is a popular word game developed by Josh Wardle and now owned by the New York Times. The goal of the game is to guess a five letter word with just six guesses. After each guess, the letters of the guess are labeled by color--green for a correct letter, yellow for a correct letter in the wrong location, and gray otherwise. The website ***3Blue1Brown*** has an [excellent introduction to Wordle](https://www.3blue1brown.com/lessons/wordle) that explains the use of [information theory](https://en.wikipedia.org/wiki/Information_theory) to solve Wordle puzzles.

This repository contains several Python programs that solve different aspects of the game. These programs can be a little slow, so I may rewrite them in a faster language.

## Get Next Wordle Guess ##

The program [get_next_wordle_guess.py](get_next_wordle_guess.py) takes the results of previous guesses and produces two lists of suggestions for the next guess. Results are entered as the word followed by a comma and five characters representing the colors, with "2" for green, "1" for yellow, and any other character for gray. For example, "crate,211--" indicates that "c" is green, "r" and "a" are yellow, and "t" and "e" are gray. 

The first list of suggestions are called ***rescue suggestions*** because they have a high entropy relative to the remaining possible solutions but are not themselves consistent with the current guess results. The second list of ***candidates*** are possible remaining solutions. The three numbers shown for each suggestion are the entropy of the word, scored against the pool of remaining candidates, an indicator variable (either 0 or 1) that indicates whether the suggested word is a candidate or not, and the entropy of the word with respect to the entire list of 12,972 allowed guesses (assumed to be equally likely). Candidates and rescue suggestions are sorted by these values.

Here is an example:

![Get Next Wordle Guess Example](https://github.com/tedlf/wordle-utils/blob/main/images/get_next.png)

## Play Wordle ##

The program [play_wordle.py](play_wordle.py) plays against either an answer entered by the user or one chosen randomly from the list of 2,315 original solutions. (Note: it is possible that the New York Times has changed this list.) The user can enter more than one starting guess. The program chooses the best rescue guess or candidate as described above for the first five guesses, and the best candidate after that. Unlike the official website, this program keeps guessing until it has the solution. It can also play in hard mode, where guesses are only chosen from candidates.

Here are several examples, the last one illustrating how much more difficult the game is in hard mode.

![Play Wordle Examples](https://github.com/tedlf/wordle-utils/blob/main/images/play.png)

## Evaluating Strategies ##

When I first started writing these programs, my goal was to analyze the effectiveness of different ***strategies*** of two initial guesses containing 10 unique letters. Here are histograms (the "Guess Distribution" shown on the website) created by [get_strategy_histogram.py](get_strategy_histogram.py) for three strategies, evaluated for the 2,315 original solutions. These strategies are ***complete***, defined here as strategies that find all of the original answers in six guesses or less.

![Two Word Strategies](https://github.com/tedlf/wordle-utils/blob/main/images/strategies2.png)

Straining the limits of this Python implementation, here are three more strategies consisting of just one initial guess. The first one, "tares" is the word with the highest entropy relative to the entire list of allowed guesses. The second one, "crane" is the word which the 3Blue1Brown video linked above claims is the best opening guess. To be fair, that analysis incorporated word frequency data and searched two levels deep, and my programs have neither of those optimizations. The first two of these strategies have one Achilles' heel, a word which takes seven guesses. For "tares" this Achilles' heel is "jolly," and for "crane" it is "viper." The third opening guess, "slant," is complete. The average number of guesses for these three strategies are remarkably close.

![One Word Strategies](https://github.com/tedlf/wordle-utils/blob/main/images/strategies1.png)

## Adversarial Wordle ##

Ranking guesses by entropy is effective, but it becomes computationally difficult to conduct a deep search. Another approach implemented in the program [adversarial_wordle.py](adversarial_wordle.py) is to model Wordle as an adversarial game between a human player who tries to minimize the number of guesses to arrive at the solution and an Adversarial Wordle program that attempts to maximize that number by continually changing the answer (choosing among valid candidates, of course). If the human is playing in hard mode, this is computationally tractable using the [alpha beta pruning](https://en.wikipedia.org/wiki/Alpha–beta_pruning) implementation of the minimax algorithm. The result of this game can be considered the worst case that the human player can expect, given the available evidence.

Here is an example where the human player is playing in hard mode and has 20 candidates to choose from. The best candidate by entropy is "gurly", but the Adversarial Wordle program wins with that choice. In fact, only one of the 20 choices will guarantee a solution within 6 guesses. Surprisingly, that choice is "durum," which is near the bottom of the list in terms of entropy.

![Play Wordle Examples](https://github.com/tedlf/wordle-utils/blob/main/images/adversarial_setup.png)

![Play Wordle Examples](https://github.com/tedlf/wordle-utils/blob/main/images/adversarial_solution.png)

## Additional Options ##

There are a few additional options for each of these programs, which can be found by using the "-h" flag, for example `python get_next_wordle_guess.py -h`. 
