import random
import sys
import os

import cowsay

# Maximum numbers an equation can use
max_number_multiplication = 6
max_number_addition = 12
max_number_subtraction = 10

# Maximum result of an equation
max_result_multiplication = 25
max_result_addition = 20
max_result_subtraction = 22

total_questions = 0
total_points = 0
history = []
characters = {
    'beavis': cowsay.beavis, 'cheese': cowsay.cheese, 'daemon': cowsay.daemon,
    'cow': cowsay.cow, 'dragon': cowsay.dragon, 'ghostbusters': cowsay.ghostbusters,
    'kitty': cowsay.kitty, 'meow': cowsay.meow, 'milk': cowsay.milk,
    'stegosaurus': cowsay.stegosaurus, 'stimpy': cowsay.stimpy, 'turkey': cowsay.turkey,
    'turtle': cowsay.turtle, 'tux': cowsay.tux
}


def get_rand(_max=10, _min=1):
    """ Return random int """

    return random.randint(_min, _max)


def get_equation_values(max_value, max_result=20, operator='+', _min=1):
    """ Returns a set of numbers to be used for an equation """

    a = None
    b = None
    retries = 0
    while (a is None or (a * b > max_result if operator == 'x' else a + b > max_result) or str(max(a, b)) + operator + str(min(a, b)) in history) and retries < 10:
        a = get_rand(max_value, _min)
        b = get_rand(max_value, _min)
        retries += 1

    return (a, b)


def f_addition():
    """ Generate an addition """

    r = get_rand(3)
    a, b = get_equation_values(
        max_number_addition, max_result_addition, '+')

    # Add operation to history
    history.append('%d+%d' % (max(a, b), min(a, b)))

    if r == 1:
        return ("%d + %d = ?" % (a, b))
    elif r == 2:
        return ("%d + ? = %d" % (a, (a + b)))
    else:
        return ("? + %d = %d" % (a, (a + b)))


def f_multiplication():
    """ Generate a multiplication """

    a, b = get_equation_values(
        max_number_multiplication, max_result_multiplication, 'x', 2)

    # Add operation to history
    history.append('%dx%d' % (max(a, b), min(a, b)))

    return ("%d x %d = ?" % (a, b))


def f_subtraction():
    """ Generate a subtraction """

    r = get_rand(3)
    v1, v2 = get_equation_values(
        max_number_subtraction, max_result_subtraction, '-')
    a = max(v1, v2)  # Get greater number
    b = min(v1, v2)  # Get smaller number

    # Add operation to history
    history.append('%d-%d' % (a, b))

    if r == 1:
        return ("%d - %d = ?" % (a, b))
    elif r == 2:
        return ("%d - ? = %d" % (a + b, a))
    else:
        return ("? - %d = %d" % (b, a + b))


operation_types = {
    'addition': f_addition, 'multiplication': f_multiplication, 'subtraction': f_subtraction
}


def pick_operation_type():
    """ Chose a type of operation """

    return random.choice(list(operation_types.keys()))


def pick_character():
    """ Chose a character """

    return random.choice(list(characters.keys()))


def read_answer(equation):
    """ Read user answer """

    print(equation)
    print()
    reply = input("Answer? ")

    return reply.strip() or '0'


def solve(equation, answer):
    """ Solve equation and check if user is correct or incorrect """

    splitted = equation.split('=')
    left = splitted[0].strip().replace('?', str(answer)).replace('x', '*')
    right = splitted[1].strip().replace('?', str(answer)).replace('x', '*')

    try:
        if right.isdigit():
            return eval(left) == int(right)
        else:
            return int(left) == eval(right)
    except ValueError:
        return False


def get_score():
    """ Print user score """

    pcent = round(total_points / total_questions *
                  100) if total_questions > 0 else 0

    print('~' * 50)
    print(('~ You got %d answers correct out of %d (%d%%)' %
           (total_points, total_questions, pcent)).ljust(49, ' ') + '~')
    print('~' * 50)


def instructions():
    """ Print instructions """

    print('~' * 30)
    print(('~ Type q to quit').ljust(29, ' ') + '~')
    print('~' * 30)


if __name__ == '__main__':
    instructions()

    while True:
        # Questions counter
        total_questions += 1
        print('~' * 30)
        print(('~ Question %d' % total_questions).ljust(29, ' ') + '~')
        print('~' * 30)
        print()

        # Pick a type of calculation
        operation_type = pick_operation_type()

        # Generate a random equation
        equation = operation_types[operation_type]()

        # Read user answer
        answer = read_answer(equation)

        # Clear screen
        os.system('clear')

        if answer.lower() == 'q':  # User quits
            # Remove non-answered question from counter
            total_questions -= 1

            character = pick_character()
            characters[character]('Goodbye')
            get_score()

            sys.exit()
            print('quit')
        else:  # Check user answer
            print('You replied: %s' % (answer))
            is_correct = solve(equation, answer)

            if is_correct:  # Correct answer
                character = pick_character()
                characters[character]('Good job!')
                print()
                total_points += 1
            else:  # Wrong answer
                print('Try again!')
                print()
