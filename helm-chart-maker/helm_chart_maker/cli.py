"""Functions for formatting console output."""

import sys
from textwrap import dedent, wrap
from typing import Any

from colorama import Fore

COLUMNS = 80
EXIT_ON_ERROR = False


def instruction(s: str, hanging = 0):
    """Unident and print a Python string/docstring."""

    # Dedent, remove line breaks, then re-wrap to COLUMNS columns wide
    for x in wrap(' '.join(dedent(s).split('\n')), COLUMNS, subsequent_indent=' '*hanging):
        print(f"{Fore.GREEN}{x}{Fore.RESET}")


def prompt(s: str, /, *, default: Any = ''):
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

    # Dedent, remove line breaks, then re-wrap to COLUMNS columns wide
    for x in wrap(' '.join(dedent(s).split('\n')), COLUMNS):
        print(f"{Fore.RED}{x}{Fore.RESET}")

    # Prevent infinite "Try again" loop when stdin is not a terminal:
    if not sys.stdin.isatty():
        exit(1)


def raw_error(s: str):
    """Display an error message, without re-wrapping."""
    print(f"{Fore.RED}{s}{Fore.RESET}")

    # Prevent infinite "Try again" loop:
    if not sys.stdin.isatty():
        exit(1)
