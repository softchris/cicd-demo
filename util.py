"""Utility functions for the cicd-demo project."""


def add(a, b):
    """Return the sum of a and b."""
    return a + b


def subtract(a, b):
    """Return the difference of a and b."""
    return a - b


def multiply(a, b):
    """Return the product of a and b."""
    return a * b


def divide(a, b):
    """Return the quotient of a divided by b.

    Raises:
        ValueError: If b is zero.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def is_even(n):
    """Return True if n is even, False otherwise."""
    return n % 2 == 0


def factorial(n):
    """Return the factorial of a non-negative integer n.

    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0:
        return 1
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def reverse_string(s):
    """Return the reverse of string s."""
    return s[::-1]


def is_palindrome(s):
    """Return True if string s is a palindrome (case-insensitive), False otherwise."""
    cleaned = s.lower().replace(" ", "")
    return cleaned == cleaned[::-1]


def flatten(nested_list):
    """Flatten a nested list one level deep and return a flat list."""
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(item)
        else:
            result.append(item)
    return result
