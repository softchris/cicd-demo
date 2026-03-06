"""Tests for util.py using pytest."""

import pytest

from util import (
    add,
    subtract,
    multiply,
    divide,
    is_even,
    factorial,
    reverse_string,
    is_palindrome,
    flatten,
    testing
)

# testing
def test_testing():
    assert testing()

# --- add ---

def test_add_positive_numbers():
    assert add(2, 3) == 5


def test_add_negative_numbers():
    assert add(-1, -4) == -5


def test_add_zero():
    assert add(0, 5) == 5


# --- subtract ---

def test_subtract():
    assert subtract(10, 3) == 7


def test_subtract_negative_result():
    assert subtract(3, 10) == -7


# --- multiply ---

def test_multiply():
    assert multiply(4, 5) == 20


def test_multiply_by_zero():
    assert multiply(100, 0) == 0


# --- divide ---

def test_divide():
    assert divide(10, 2) == 5.0


def test_divide_non_integer_result():
    assert divide(7, 2) == 3.5


def test_divide_by_zero_raises():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(5, 0)


# --- is_even ---

def test_is_even_with_even_number():
    assert is_even(4) is True


def test_is_even_with_odd_number():
    assert is_even(7) is False


def test_is_even_with_zero():
    assert is_even(0) is True


# --- factorial ---

def test_factorial_of_zero():
    assert factorial(0) == 1


def test_factorial_of_one():
    assert factorial(1) == 1


def test_factorial_of_five():
    assert factorial(5) == 120


def test_factorial_negative_raises():
    with pytest.raises(ValueError, match="Factorial is not defined for negative numbers"):
        factorial(-1)


# --- reverse_string ---

def test_reverse_string():
    assert reverse_string("hello") == "olleh"


def test_reverse_string_empty():
    assert reverse_string("") == ""


def test_reverse_string_single_char():
    assert reverse_string("a") == "a"


# --- is_palindrome ---

def test_is_palindrome_true():
    assert is_palindrome("racecar") is True


def test_is_palindrome_false():
    assert is_palindrome("hello") is False


def test_is_palindrome_case_insensitive():
    assert is_palindrome("Racecar") is True


def test_is_palindrome_with_spaces():
    assert is_palindrome("a man a plan a canal panama") is True


# --- flatten ---

def test_flatten_nested_list():
    assert flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]


def test_flatten_mixed_list():
    assert flatten([1, [2, 3], 4]) == [1, 2, 3, 4]


def test_flatten_empty_list():
    assert flatten([]) == []


def test_flatten_already_flat():
    assert flatten([1, 2, 3]) == [1, 2, 3]
