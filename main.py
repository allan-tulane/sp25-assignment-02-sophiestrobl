"""
CMPS 2200  Assignment 2.
See assignment-02.md for details.
"""
from collections import defaultdict
import math


def parens_match_iterative(mylist):
    """
    Implement the iterative solution to the parens matching problem.

    Params:
      mylist...a list of strings
    Returns:
      True if the parenthesis are matched, False otherwise

    e.g.,
    >>> parens_match_iterative(['(', 'a', ')'])
    True
    >>> parens_match_iterative(['('])
    False
    """
    def iterate(update_fn, initial, lst):
        result = initial
        for elem in lst:
            result = update_fn(result, elem)
            if result == -float('inf'):  # Early exit if invalid
                return result
        return result

    return iterate(parens_update, 0, mylist) == 0


def parens_update(current_output, next_input):
    """
    Updates the parenthesis balance count.

    Params:
      current_output...cumulative output so far
      next_input.......next value in the input list

    Returns:
      Updated current_output value.
    """
    if current_output == -float('inf'):  # Already invalid
        return current_output
    if next_input == '(':
        return current_output + 1
    elif next_input == ')':
        if current_output <= 0:  # Closing before an open -> invalid
            return -float('inf')
        return current_output - 1
    return current_output  # Ignore non-parenthesis


#### Scan solution
def parens_match_scan(mylist):
    """
    Implement a solution using `scan`.

    Params:
      mylist...a list of strings
    Returns:
      True if the parenthesis are matched, False otherwise

    e.g.,
    >>> parens_match_scan(['(', 'a', ')'])
    True
    >>> parens_match_scan(['('])
    False
    """
    mapped_list = list(map(paren_map, mylist))

    history, last = scan(lambda x, y: x + y, 0, mapped_list)

    return last == 0 and reduce(min_f, history) >= 0

def scan(f, id_, a):
    """
    Performs an inclusive scan (prefix sum).
    """
    result = []
    running = id_
    for elem in a:
        running = f(running, elem)
        result.append(running)
    return result, running


def paren_map(x):
    """
    Maps characters to integer values:
    '(' -> 1, ')' -> -1, others -> 0.
    """
    return 1 if x == '(' else -1 if x == ')' else 0


def min_f(x, y):
    """
    Returns the minimum of x and y.
    """
    return min(x, y)


#### Divide and conquer solution
def parens_match_dc(mylist):
    """
    Calls `parens_match_dc_helper` and checks for matching result.

    Returns:
      True if (0,0) is returned (indicating matched parentheses), otherwise False.
    """
    n_unmatched_left, n_unmatched_right = parens_match_dc_helper(mylist)
    return n_unmatched_left == 0 and n_unmatched_right == 0


def parens_match_dc_helper(mylist):
    """
    Divide and conquer approach for parenthesis matching.

    Returns:
      A tuple (R, L), where:
      - R is the number of unmatched right parentheses.
      - L is the number of unmatched left parentheses.
    """
    # Base cases
    if len(mylist) == 0:
        return (0, 0)
    elif len(mylist) == 1:
        if mylist[0] == '(':
            return (0, 1)  # One unmatched '('
        elif mylist[0] == ')':
            return (1, 0)  # One unmatched ')'
        return (0, 0)  # Non-parenthesis characters

    # Recursive calls
    mid = len(mylist) // 2
    left_unmatched = parens_match_dc_helper(mylist[:mid])
    right_unmatched = parens_match_dc_helper(mylist[mid:])

    # Combine results
    left_r, left_l = left_unmatched
    right_r, right_l = right_unmatched

    # Balance mismatches
    if left_l > right_r:
        return (left_r, right_l + (left_l - right_r))
    return (left_r + (right_r - left_l), right_l)


