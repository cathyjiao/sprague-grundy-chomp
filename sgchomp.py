"""
Calculate Sprague-Grundy values for Chomp. Input is tuple representing rows of the board with the first tuple
entry being the bottom row of the board, and the last tuple as the first row.

Author: Cathy Jiao
"""


def chomp(A):
    """
    Calculates Sprague-Grundy value for a Chomp board.

    :param A: (tuple) rows of the board
    :return: (int) Sprague-Grundy value
    """

    if sum(A) == 0:
        return 0

    # create terminal position of chomp board (one bad chocolate piece left)
    zero_tuple = tuple([1] + ([0] * (len(A) - 1)))

    # initialize memoization map
    sg_map = {zero_tuple: 0}

    # recursively calculate sg value
    sg, sg_map = chomp_helper(A, sg_map)

    return sg


def chomp_helper(A, sg_map):
    """
    Recursively calculates the sg value of a chomp board.

    :param A: (tuple) rows of the board.
    :param sg_map: (dict) memoization map
    :return: (int) sg value of A
    """

    # return sg value if it has already been calculated
    if A in sg_map:
        return sg_map[A], sg_map

    # keep track of sg value of followers from current position
    sg_values = set([])

    # get followers of current position
    followers = get_followers(A)

    # find sg values of followers
    for f in followers:
        sg, sg_map = chomp_helper(f, sg_map)
        sg_values.add(sg)

    # find minimal excluded value from sg values of followers
    sg = get_mex(list(sg_values))

    # add sg value of current position to memoization map
    sg_map[A] = sg

    return sg, sg_map


def get_mex(numbers):
    """
    Find minimal excluded value from a list of numbers.

    :param numbers: list of int
    :return: (int) mex value
    """

    # sort the numbers in ascending order
    numbers.sort()

    if numbers[0] > 0:
        return 0
    else:
        # find gap in the numbers
        for i, v in enumerate(numbers[:-1]):
            v_next = numbers[i + 1]
            if v + 1 != v_next:
                return v + 1

        # return 1 + last number in list
        return numbers[-1] + 1


def get_followers(A):
    """
    Return all direct followers of A

    :param A: (tuple) rows of the board
    :return: list of tuples that are the followers
    """

    followers = []

    # begin eating chocolate from top right corner of board
    for i in reversed(range(len(A))):
        chips = A[i]
        for j in reversed(range(chips)):
            follower = eat(A, i, j)
            followers.append(follower)

    # remove the 0 tuple
    followers.remove(tuple([0] * len(A)))

    return list(followers)


def eat(A, row, col):
    """
    Eat chocolate from a position in Chomp board.

    :param A: (tuple) rows of the board
    :param row: (int) y-coordinate of position
    :param col: (int) x-coordinate of position
    :return: (tuple) new chomp board
    """

    A_new = list(A)

    # eat chocolate from rows above
    for i in range(row, len(A)):
        pile = A[i]
        if col <= pile:
            A_new[i] = col

    return tuple(A_new)


def test(A, sg):
    """
    Tests if chomp function produces correct sg value.

    :param A: (tuple) rows of the board
    :param sg: (int) desired sg value
    """
    predicted_sg = chomp(A)
    if sg == predicted_sg:
        print('Passed')
    else:
        print('Failed')


def run_tests():
    """
    Run test suite.
    """
    test(tuple([1]), 0)
    test(tuple([0]), 0)
    test((2, 1), 0)
    test((3, 2), 0)
    test((1, 1), 1)
    test(tuple([2]), 1)
    test(tuple([3]), 2)
    test((2, 2), 2)
    test((3, 1), 3)
    test((3, 3), 4)
    test((5, 5, 5, 5, 5), 6)


# Main function
if __name__ == "__main__":
    run_tests()

