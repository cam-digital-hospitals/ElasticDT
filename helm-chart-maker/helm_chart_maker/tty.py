"""Functions for formatting console output."""

import sys
from textwrap import dedent, wrap

from colorama import Fore


def instruction(s: str):
    """Unident and print a Python string/docstring."""
    for x in wrap(' '.join(dedent(s).split('\n')), 100):
        print(f"{Fore.GREEN}{x}{Fore.RESET}")


def prompt(s: str, default=''):
    """Prompt the user for input."""
    try:
        ret = input(f"{Fore.YELLOW}{s}{Fore.RESET}")
    except EOFError:
        ret = ''

    # Makes piped input appear as if it were typed in
    if not sys.stdin.isatty():
        print(ret)

    if ret is None or ret == '':
        ret = default

    return ret


def error(s: str):
    """Display an error message."""
    for x in wrap(' '.join(dedent(s).split('\n')), 100):
        print(f"{Fore.RED}{x}{Fore.RESET}")

    # Prevent infinite "Try again" loop:
    if not sys.stdin.isatty():
        exit(1)


def raw_error(s: str):
    """Display an error message, without re-wrapping."""
    print(f"{Fore.RED}{s}{Fore.RESET}")

    # Prevent infinite "Try again" loop:
    if not sys.stdin.isatty():
        exit(1)
