#! /usr/bin/env python3
# coding: utf-8

import argparse
from os import get_terminal_size


class ProgressBar:
    """The purpose of this class is to display a progress bar

    Attributes
    ----------
    _progress : dict
        current progress informations

    Methods
    -------
    update(current, total, label)
        update the current progress informations & display
    """

    def __init__(self):
        self._progress = {"current": 0, "total": 0, "label": ""}

    def update(self, current, total, label):
        self._progress = {
            "current": int(current),
            "total": int(total),
            "label": label,
        }

        self.__update_display()

    # --- PRIVATE METHODS ---

    def __update_display(self):

        try:
            terminal_size = get_terminal_size()
            bar_size = terminal_size.columns - 20
            num_lines = 2

            # Clean terminal
            print(" " * terminal_size.columns * num_lines)
            print("\033[A" * (num_lines + 1))

            rows = self._progress
            rows_bar = self.__get_progressbar(rows, bar_size)
            print(f"{rows_bar} {rows['current']}/{rows['total']} rows")
            print(f"{rows['label'].center(bar_size)[:bar_size]}", end="\r")

            # Reset cursor position in terminal
            print("\033[A" * num_lines)

        except OSError:
            pass

    def __get_progressbar(self, source, bar_size):

        todo_char = "◻"
        done_char = "◼"

        try:
            size = round(bar_size / source["total"] * source["current"])
        except ZeroDivisionError:
            size = 0

        fillchars = done_char * size
        return f"{fillchars.ljust(bar_size,todo_char)}"


def get_args():
    """Parse command arguments and return the appropriate parameters.

    Returns
    -------
    str:
        The path to the CSV file to parse.
    bool:
        Should display cProfile & pstats informations or not?
    """

    file_sample = "dataFinance-sample.csv"
    file_full = "dataFinance.csv"

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--sample",
        action="store_true",
        help=f"Use {file_sample} instead of {file_full}",
    )
    parser.add_argument(
        "-p", "--profile", action="store_true", help="Display cProfile stats"
    )

    parseargs = parser.parse_args()

    return (
        (file_sample, parseargs.profile)
        if parseargs.sample
        else (file_full, parseargs.profile)
    )
