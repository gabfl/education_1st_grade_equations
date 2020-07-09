import random
import sys
import os

import cowsay

import equations

max_number_addition = 12
max_number_subtraction = 6

foods = [
    'sandwiches',
    'pizzas',
    'hamburgers',
    'hot dogs',
    'chicken nuggets',
    'grilled cheese sandwiches',
    'tacos',
    'fries',
    'chocolate bars',
    'pickles'
]

kids = ['Zachary', 'Grant', 'Jack', 'Nolan', 'Bennet', 'Charlie',
        'Molly', 'Logan', 'Elliot', 'Johan', 'Maddie']

verbs = ['ate', 'devoured', 'had']

places = ['fridge', 'pantry', 'cupboard']

operation_types = ['addition', 'subtraction']


def pick_one(list_, not_this_ones=[]):
    choice = None
    while not choice or choice in not_this_ones:
        choice = random.choice(list_)

    return choice


def sentence_maker():
    operation_type = pick_one(operation_types)

    numbers_in_equation = equations.get_rand(3, 2)
    food = pick_one(foods)
    kid1 = pick_one(kids)
    kid2 = pick_one(kids, [kid1])
    kid3 = pick_one(kids, [kid1, kid2])
    place = pick_one(places)

    if operation_type == 'addition':
        n1 = equations.get_rand(max_number_addition)
        n2 = equations.get_rand(max_number_addition)
        n3 = equations.get_rand(max_number_addition)

        if numbers_in_equation == 2:
            result = n1 + n2
            sentence = ('%s %s %d %s and %s %s %d more. How many %s have been eaten?' % (
                kid1, pick_one(verbs), n1, food, kid2, pick_one(verbs), n2, food))
        else:
            result = n1 + n2 + n3
            sentence = ('%s %s %d %s, %s %s %d and %s %s %d more. How many %s have been eaten?' % (
                kid1, pick_one(verbs), n1, food, kid2, pick_one(verbs), n2, kid3, pick_one(verbs), n3, food))
    elif operation_type == 'subtraction':
        n1 = equations.get_rand(max_number_subtraction)
        n2 = equations.get_rand(max_number_subtraction)
        n3 = equations.get_rand(max_number_subtraction)

        if numbers_in_equation == 2:
            total = n1 + n2
            result = total - n1
            sentence = ('There are %d %s in %s\'s %s. %s %s %d. How many are left?' % (
                total, food, kid1, place, kid2, pick_one(verbs), n1))
        else:
            total = n1 + n2 + n3
            result = total - n1 - n2
            sentence = ('There are %d %s in %s\'s %s. %s %s %d and %s %s %d more. How many are left?' % (
                total, food, kid1, place, kid2, pick_one(verbs), n1, kid3, pick_one(verbs), n2))
    else:
        raise RuntimeError('Invalid operation type')

    return (result, sentence)


def solve(result, answer):
    """ Validate user answer """

    try:
        return result == int(answer)
    except ValueError:
        return False


if __name__ == '__main__':
    equations.instructions()

    while True:
        # Questions counter
        equations.total_questions += 1
        print('~' * 30)
        print(('~ Question %d' % equations.total_questions).ljust(29, ' ') + '~')
        print('~' * 30)
        print()

        # Generate a word problem
        result, sentence = sentence_maker()

        # Read user answer
        answer = equations.read_answer(sentence)

        # Clear screen
        os.system('clear')

        if answer.lower() == 'q':  # User quits
            # Remove non-answered question from counter
            equations.total_questions -= 1

            equations.get_score()

            sys.exit()
            print('quit')
        else:  # Check user answer
            print('You replied: %s' % (answer))
            is_correct = solve(result, answer)

            if is_correct:  # Correct answer
                character = equations.pick_character()
                equations.characters[character]('Good job!')
                print()
                equations.total_points += 1
            else:  # Wrong answer
                print('Try again!')
                print()
