#! /usr/bin/env python3
# coding: utf-8

import pandas as pd
import numpy as np
import logging as lg

import time

from utils import ProgressBar
progress_monitor = ProgressBar()

lg.basicConfig(filename="algo.log", filemode="w", level=lg.DEBUG)
lg.disable(lg.DEBUG)


def pd_parse(file_name):
    lg.info("START :: Parse data")

    col_names = ["Shares", "Cost(Euro/share)", "Profit(% post 2 years)"]
    data = pd.read_csv(file_name)  # nrows=20
    df = pd.DataFrame(data, columns=col_names)
    # print(df)

    df["ratio"] = df[col_names[2]] / df[col_names[1]]
    df = df.replace([np.inf, -np.inf], np.nan).dropna(axis=0)

    df = pd.DataFrame(
        df.sort_values(
            by=["ratio", col_names[2], col_names[1]], ascending=False
        ).to_numpy(),
        index=df.index,
        columns=df.columns,
    )

    lg.debug(df)

    names = [x for x in df[col_names[0]]]
    costs = [x for x in df[col_names[1]]]
    profits = [x for x in df[col_names[2]]]
    capacity = 500
    lg.info("CLOSE :: Parse data")

    lg.info("START :: BRUT algo")
    search(costs, profits, names, capacity)
    lg.info("CLOSE :: BRUT algo")


def search(costs, profits, names, capacity):

    start_t = time.time()

    # costs = [5, 2, 1]  # TODO tmp
    # profits = [10, 2, 1]

    selected = set()
    explored = set()

    spend = recursive_call_4(
        costs, profits, capacity, explored=explored, selected=selected, num_selection=3
    )
    progress_monitor.update(len(selected), len(selected), "Finished")

    if spend != capacity:
        print("\nNO MATCH FOUND")
        return
    else:
        print("")

    sort_sequences = []
    for i, r in enumerate(selected):
        profit = sum([profits[x] for x in r])
        sort_sequences.append((profit, r))

    sorted_sequences = sorted(sort_sequences)
    for i, result in enumerate(sorted_sequences):
        print(
            "\n", f" TOP {len(sort_sequences)-i} ".center(50, "*"), sep="", end="\n\n"
        )
        profit = result[0]
        shares = result[1]

        results = {}
        for share_index in shares:
            results[names[share_index]] = (
                shares.count(share_index),
                costs[share_index],
            )

        print(f"The maximum profit is {profit} \n\nwith the following shares:\n")
        print(*[f"- {k} [{v[1]}€] x {v[0]}" for k, v in results.items()], sep="\n")

    end_t = time.time()
    print("\n", "*" * 50, f"\nRunning time: {end_t-start_t} seconds", sep="")


def recursive_call_4(
    costs,
    profits,
    capacity,
    total=0,
    path=[],
    explored=set(),
    selected=set(),
    num_selection=10,
):

    explored.add(tuple(path))

    if total == capacity:
        selected.add(tuple(path))
        progress_monitor.update(len(selected), num_selection, "")
        return total
    elif total > capacity:
        return 0

    for i, p in enumerate(profits):
        new_path = path[:]
        new_path.append(i)
        new_path = sorted(new_path)
        if tuple(new_path) in explored:
            continue
        else:
            x = recursive_call_4(
                costs,
                profits,
                capacity,
                total + costs[i],
                new_path,
                explored,
                selected,
                num_selection,
            )
            if x > 0 and len(selected) >= num_selection:
                return x
    return 0


def recursive_call_3(
    costs,
    total_cost,
    max_depth,
    current_depth,
    path=[],
    count=[0],
    explored=set(),
    selected=set(),
):

    explored.add(tuple(path))

    if current_depth >= max_depth or total_cost > maxValue:
        return

    if total_cost == maxValue:
        count[0] += 1
        selected.add(tuple(path))
        # print(f"{path} {count}")
        return

    for i, c in enumerate(costs):

        new_path = path[:]
        new_path.append(i)
        new_path = sorted(new_path)
        if tuple(new_path) in explored:
            continue
        else:
            print(f"{len(selected)} OPEN {tuple(new_path)}")
        recursive_call_3(
            costs,
            total_cost + c,
            max_depth,
            current_depth + 1,
            new_path,
            count,
            explored,
            selected,
        )


# 10 combinaisons avec A,B,C depth 3
def recursive_call_2(
    costs, max_depth, current_depth, path=[], count=[0], explored=set()
):
    if current_depth >= max_depth:
        count[0] += 1
        explored.add(tuple(sorted(path)))
        print(f"{path} {count}")
        return True

    for c in costs:

        new_path = path[:]
        new_path.append(c)
        new_path = sorted(new_path)
        if tuple(new_path) in explored:
            continue
        else:
            print(f"OPEN {tuple(new_path)}")
        recursive_call_2(costs, max_depth, current_depth + 1, new_path, count, explored)


# 27 combinaisons avec A,B,C depth 3
def recursive_call(costs, max_depth, current_depth, path=[], count=[0]):
    if current_depth >= max_depth:
        count[0] += 1
        print(f"{path} {count}")
        return True

    for c in costs:

        new_path = path[:]
        new_path.append(c)
        recursive_call(costs, max_depth, current_depth + 1, new_path, count)


def load_file(file_name):
    with open(file_name, "r") as f:
        for line in f:
            print(line)


if __name__ == "__main__":
    print("\n")
    lg.info("RUN BRUT FORCE algorithm")

    # load_file("dataFinance-sample.csv")
    pd_parse("dataFinance-sample.csv")
    # pd_parse("dataFinance.csv")
