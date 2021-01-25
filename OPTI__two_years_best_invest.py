#! /usr/bin/env python3
# coding: utf-8

from math import ceil
import time

import pandas as pd
import numpy as np


def pd_parse(file_name):
    col_names = ["Shares", "Cost(Euro/share)", "Profit(% post 2 years)"]
    data = pd.read_csv(file_name)  # nrows=20
    df = pd.DataFrame(data, columns=col_names)

    # df["ratio"] = df[col_names[1]] / df[col_names[0]]
    df = df.replace([np.inf, -np.inf, 0.0], np.nan).dropna(axis=0)
    # df = df.sort_values(by=["ratio", col_names[1], col_names[0]], ascending=False)

    print(df)

    names = [x for x in df[col_names[0]]]
    costs = [x for x in df[col_names[1]]]
    profits = [x for x in df[col_names[2]]]
    capacity = 500
    unbounded = True

    # names = ["Water", "Book", "Food", "Jacket", "Camera"]
    # costs = [3, 1, 2, 2, 1]
    # profits = [10, 3, 9, 5, 6]
    # capacity = 6
    # unbounded = False

    # names = ["WA", "GT", "NG", "BM", "SPC"]
    # costs = [.5, .5, 1, 2, .5]
    # profits = [7, 6, 9, 9, 8]
    # capacity = 2.0
    # unbounded = False

    # names = ["Guitar", "Stereo", "Laptop", "IPhone"]
    # costs = [1, 4, 3, 1]
    # profits = [1500, 3000, 2000, 2000]
    # capacity = 4
    # unbounded = True

    start_t = time.time()
    profit, share_indexes = knapsack_dynamic_programming(
        costs, profits, capacity, names, unbounded
    )

    results = {}
    for share_index in share_indexes:
        results[names[share_index]] = share_indexes.count(share_index)

    print("\n\n\n\n")

    print(f"The maximum profit is {profit} \n\nwith the following shares:\n")
    for k, v in results.items():
        print(f"- {k} x {v}")

    end_t = time.time()
    print(f"\nTime: {end_t-start_t} seconds")


def knapsack_dynamic_programming(costs, profits, capacity, names=[], unbounded=False):

    step = min(costs)
    # print("STEP:", step)

    if step < 1:
        step = 1

    rows = len(costs)
    columns = ceil(capacity / step)
    # print("STEP:", step, rows, columns)

    grid_values = np.zeros([rows, columns])
    # grid_shares = [[None]*columns]*rows
    grid_shares = [[None for x in range(columns)] for y in range(rows)]
    # print("GRID:", grid_values)
    # print("GRID:", grid_shares)

    # print("GO!")

    for i in range(rows):
        # print(f"row: {i} / {rows}")

        ref_row = i - 1
        if unbounded:
            ref_row = i

        for j in range(columns):

            # print("COST COND:", j + 1, ">=", costs[i])

            step_value = (j + 1) * step
            # print("STEP VALUE:", step_value)

            # if current sub-sack can hold at least one share
            if step_value >= costs[i]:
                # print("OK")

                # Get the previous max profit for this sub-capacity
                prev_max = grid_values[i - 1][j] if i > 0 else 0

                # Get the current Share profit
                current_value = profits[i]

                # Search for the previous max of the remaining capacity
                filling_index = j - int(costs[i] // step)

                # Get the current max profit for this sub-capacity
                current_max = current_value
                # print("DEBUG:", i-1, filling_index)
                current_max += (
                    grid_values[ref_row][filling_index] if filling_index > -1 else 0
                )

                # print(prev_max, current_value, filling_index, current_max)

                # Set the new max profit
                new_max = max(prev_max, current_max)
                grid_values[i][j] = new_max

                if new_max == prev_max:
                    grid_shares[i][j] = grid_shares[i - 1][j]
                else:
                    grid_shares[i][j] = [i]
                    if filling_index > -1:
                        if grid_shares[ref_row][filling_index]:
                            grid_shares[i][j].extend(
                                grid_shares[ref_row][filling_index]
                            )

                # print(grid_values)
                # print(np.array(grid_shares))

            else:
                # print("PAS OK")
                grid_values[i][j] = grid_values[i - 1][j] if i > 0 else 0
                grid_shares[i][j] = grid_shares[i - 1][j] if i > 0 else None

            # print(i, j, costs[i])
    return grid_values[i][j], grid_shares[i][j]


if __name__ == "__main__":
    print("\n\n\n")
    pd_parse("dataFinance-sample.csv")
    # pd_parse("dataFinance.csv")
