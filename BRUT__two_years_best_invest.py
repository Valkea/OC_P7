#! /usr/bin/env python3
# coding: utf-8

import pandas as pd

import time


def pd_parse(file_name):
    col_names = ["Cost(Euro/share)", "Profit(% post 2 years)"]
    data = pd.read_csv(file_name)
    df = pd.DataFrame(data, columns=col_names)
    print(df)

    costs = [x for x in df[col_names[0]]]
    profits = [x for x in df[col_names[1]]]

    search(costs, profits)


def search(costs, profits):

    start_t = time.time()

    costs = [1, 2, 10]  # TODO tmp
    profits = [1, 2, 5]

    # costs = ["A", "B", "C"]
    depth = 500

    selected = set()
    explored = set()
    recursive_call_3(costs, 0, depth, 0, selected=selected, explored=explored)

    # for r in explored:
    #    print(f"EXP==>[{r}]")
    # print(len(explored))

    for r in selected:
        print(f"SEL==>[{r}]")

    print(len(selected))

    end_t = time.time()

    print(f"Time: {end_t-start_t} seconds")


maxValue = 15


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

    for c in costs:

        new_path = path[:]
        new_path.append(c)
        new_path = sorted(new_path)
        if tuple(new_path) in explored:
            continue
        else:
            print(f"OPEN {tuple(new_path)}")
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
