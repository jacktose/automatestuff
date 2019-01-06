#!/usr/bin/env python3

'''Project: Generating Random Quiz Files
From "Automate the Boring Stuff with Python" ch. 8
'''

import os
import random
from collections import namedtuple
from string import ascii_uppercase as alphabet

def main():
    NUM_STATES = 50
    NUM_QUESTIONS = NUM_STATES
    NUM_OPTIONS = 4
    NUM_STUDENTS = 35

    from data import capitals
    if not len(capitals) == NUM_STATES:
        print(f'Weird! You have {len(capitals)} states.')
        return 1

    states = list(capitals.keys())
    tests = []
    for i in range(NUM_STUDENTS):
        questions = []
        for j,state in enumerate(states):
            other_states = states[:j] + states[j+1:]  # exclude item at index j
            other_states = random.sample(other_states, NUM_OPTIONS-1)
            other_capitals = [capitals[state] for state in other_states]
            options = [capitals[state]] + other_capitals
            random.shuffle(options)
            answer = options.index(capitals[state])
            questions.append(Question(state, options, answer))
        random.shuffle(questions)
        tests.append(questions)

    for dir in ['tests', 'keys']:
        if not os.path.isdir(dir):
            os.mkdir(dir)
    places = len(str(len(tests) - 1))
    for i,test in enumerate(tests):
        test_num = str(i+1).zfill(places)
        with open(os.path.join('tests', f'test{test_num}.txt'), 'w') as test_file,\
             open(os.path.join('keys', f'key{test_num}.txt'), 'w') as key_file:
            test_file.write('Name:\nDate:\nPeriod:\n\n')
            test_file.write(f'State Capitals Quiz (Form {test_num})\n\n')
            for j,question in enumerate(test):
                test_file.write(f'{j+1}. What is the capital of {question.state}?\n')
                for letter, option in zip(alphabet, question.options):
                    test_file.write(f'\t{letter}. {option}\n')
                test_file.write('\n')
                key_file.write(f'{j+1}. {alphabet[question.answer]}\n')

Question = namedtuple('Question', 'state, options, answer')

if __name__ == '__main__':
    import sys
    sys.exit(main())
