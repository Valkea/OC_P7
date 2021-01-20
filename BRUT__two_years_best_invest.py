#! /usr/bin/env python3
# coding: utf-8

import pandas as pd
import numpy as np

import time


def pd_parse(file_name):
    col_names = ["Cost(Euro/share)", "Profit(% post 2 years)"]
    data = pd.read_csv(file_name)  # nrows=20
    df = pd.DataFrame(data, columns=col_names)
    # print(df)

    df["ratio"] = df[col_names[1]] / df[col_names[0]]
    df = df.replace([np.inf, -np.inf], np.nan).dropna(axis=0)

    df = df.sort_values(by=["ratio", col_names[1], col_names[0]], ascending=False)
    print(df)

    costs = [x for x in df[col_names[0]]]
    profits = [x for x in df[col_names[1]]]

    search(costs, profits)


def search(costs, profits):

    start_t = time.time()

    # costs = [5, 2, 1]  # TODO tmp
    # profits = [10, 2, 1]

    capacity = 500
    selected = set()
    explored = set()
    # recursive_call_3(costs, 0, depth, 0, selected=selected, explored=explored)
    spend = recursive_call_4(
        costs, profits, capacity, explored=explored, selected=selected, num_selection=3
    )
    if spend == capacity:
        print("\nMATCH FOUND\n")
    else:
        print("\nNO MATCH FOUND\n")
        return

    # for r in explored:
    #    print(f"EXP==>[{r}]")
    # print(len(explored))

    sort_sequences = []
    for r in selected:
        cost = sum([costs[x] for x in r])
        profit = sum([profits[x] for x in r])
        sort_sequences.append((profit, [costs[x] for x in r], cost))
        print(f"SEL==>[{r}] {cost} {profit}")

    print()

    sort_sequences = sorted(sort_sequences)
    for r in sort_sequences:
        print(f"SOR==>{r}")

    best = sort_sequences[-1:]
    print("\nBEST:", best)

    print(len(selected))

    end_t = time.time()

    print(f"Time: {end_t-start_t} seconds")


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
            if x > 0 and len(selected) > num_selection:
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
    # load_file("dataFinance-sample.csv")
    pd_parse("dataFinance-sample.csv")
    # pd_parse("dataFinance.csv")
