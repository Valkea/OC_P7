#! /usr/bin/env python3
# coding: utf-8

import pandas as pd
import numpy as np
import logging as lg
import cProfile
import pstats

import time

from utils import ProgressBar, get_args

progress_monitor = ProgressBar()

lg.basicConfig(filename="algo.log", filemode="w", level=lg.DEBUG)
lg.disable(lg.DEBUG)

PRINT_STATS = False


def main(file_name):

    start_t = time.time()

    # --- LOAD data ---

    col_names = ["Shares", "Cost(Euro/share)", "Profit(% post 2 years)"]
    data = pd.read_csv(file_name)  # nrows=20
    df = pd.DataFrame(data, columns=col_names)

    # --- CLEAN data ---

    df = df.replace([np.inf, -np.inf], np.nan).dropna(axis=0)

    # --- ADD computed data ---

    # df["ratio"] = df[col_names[2]] / df[col_names[1]]
    df["gain"] = df[col_names[1]] / 100.0 * df[col_names[2]]

    # --- SORT data ---

    df = pd.DataFrame(
        df.sort_values(by=[col_names[2], col_names[1]], ascending=False).to_numpy(),
        index=df.index,
        columns=df.columns,
    )

    lg.debug(df)

    # --- PREPARE data for the algorithm ---

    names = [x for x in df[col_names[0]]]
    costs = [x for x in df[col_names[1]]]
    profits = [x for x in df["gain"]]
    capacity = 500
    max_results = 1

    # --- CALL the algorithm ----

    if PRINT_STATS:
        profile = cProfile.Profile()
        profile.enable()

    selected = search(costs, profits, names, capacity)

    if PRINT_STATS:
        profile.disable()
        ps = pstats.Stats(profile)

    # --- PARSE the returned values ---

    if selected is not None:

        sort_sequences = []
        for i, r in enumerate(selected):
            profit = int(sum([profits[x] * 100.0 for x in r])) / 100
            sort_sequences.append((profit, r))

        sorted_sequences = sorted(sort_sequences, reverse=True)
        for i, result in enumerate(sorted_sequences):
            print(
                "\n",
                f" TOP {i+1} ".center(50, "*"),
                sep="",
                end="\n\n",
            )
            profit = result[0]
            shares = result[1]

            results = {}
            for share_index in shares:
                results[names[share_index]] = (
                    shares.count(share_index),
                    costs[share_index],
                )

            print(
                f"The maximum profit is {profit:.2f}€ \n\nwith the following shares:\n"
            )
            print(*[f"- {k} [{v[1]}€] x {v[0]}" for k, v in results.items()], sep="\n")

            total = sum([v[0] * v[1] for k, v in results.items()])
            print(f"\nTotal: {total:.2f}€")

            if i == max_results - 1:
                break

    # --- CLOSE ---

    end_t = time.time()
    print("", "*" * 50, f"\nTime: {end_t-start_t} seconds", sep="\n", end="\n" * 2)

    if PRINT_STATS:
        ps.sort_stats("cumtime", "ncalls")
        ps.print_stats()


def search(costs, profits, names, capacity):
    """ TODO """

    # costs = [5, 2, 1]  # DEBUG data
    # profits = [10, 2, 1]

    selected = set()
    # explored = set()

    spend = recursive_search(
        costs,
        profits,
        capacity,
        # explored=explored,
        selected=selected,
        num_selection=15000,
    )
    progress_monitor.update(len(selected), len(selected), "Finished BRUT search")

    if spend != capacity:
        print("\nNO MATCH FOUND")
        return None, None

    print("\n" * 2)
    return selected  # , explored


def recursive_search(
    costs,
    profits,
    capacity,
    total=0,
    path=[],
    # explored=set(),
    selected=set(),
    num_selection=10,
):
    """ TODO """

    # explored.add(tuple(path))

    if total == capacity:
        selected.add(tuple(path))
        progress_monitor.update(len(selected), num_selection, "")
        return total
    elif total > capacity:
        return 0

    for i, p in enumerate(profits):
        new_path = path[:]
        new_path.append(i)
        # new_path = sorted(new_path)

        # if tuple(new_path) in explored:
        #     continue
        # else:
        x = recursive_search(
            costs,
            profits,
            capacity,
            total + costs[i],
            new_path,
            # explored,
            selected,
            num_selection,
        )
        if x > 0 and len(selected) >= num_selection:
            return x
    return 0


if __name__ == "__main__":
    print("\n")
    lg.info("RUN BRUT FORCE algorithm")

    filepath, profile = get_args()

    if profile:
        PRINT_STATS = True

    main(filepath)
