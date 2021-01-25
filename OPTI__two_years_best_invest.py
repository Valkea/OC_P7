#! /usr/bin/env python3
# coding: utf-8

from math import ceil
import time
import logging as lg

import pandas as pd
import numpy as np
# import psutils

from utils import ProgressBar
progress_monitor = ProgressBar()

lg.basicConfig(filename="algo.log", filemode="w", level=lg.DEBUG)
lg.disable(lg.DEBUG)


def pd_parse(file_name):
    lg.info("OPEN :: Parse data")

    col_names = ["Shares", "Cost(Euro/share)", "Profit(% post 2 years)"]
    data = pd.read_csv(file_name)  # nrows=20
    df = pd.DataFrame(data, columns=col_names)

    # df["ratio"] = df[col_names[1]] / df[col_names[0]]
    df = df.replace([np.inf, -np.inf, 0.0], np.nan).dropna(axis=0)
    # df = df.sort_values(by=["ratio", col_names[1], col_names[0]], ascending=False)

    lg.debug(df)

    names = [x for x in df[col_names[0]]]
    costs = [x for x in df[col_names[1]]]
    profits = [x for x in df[col_names[2]]]
    capacity = 500
    unbounded = True

    lg.info("CLOSE :: Parse data")

    lg.info("START :: OPTI algo")
    start_t = time.time()
    profit, share_indexes = knapsack_dynamic_programming(
        costs, profits, capacity, names, unbounded
    )
    lg.info("CLOSE :: OPTI algo")

    lg.info("START :: Display results")
    results = {}
    for share_index in share_indexes:
        results[names[share_index]] = share_indexes.count(share_index)

    print("\n\n")

    print(f"The maximum profit is {profit} \n\nwith the following shares:\n")
    for k, v in results.items():
        print(f"- {k} x {v}")

    end_t = time.time()
    print(f"\nTime: {end_t-start_t} seconds")
    lg.info("CLOSE :: Display results")


def knapsack_dynamic_programming(costs, profits, capacity, names=[], unbounded=False):

    step_size = min(costs)
    # if step_size < 1:  # TODO
    #    step_size = 1

    rows = len(costs)
    columns = ceil(capacity / step_size)
    lg.debug(f"step_size:{step_size}, rows:{rows}, columns:{columns}")

    grid_values = np.zeros([rows, columns])
    grid_shares = [[None for x in range(columns)] for y in range(rows)]

    for i in range(rows):
        # print(f"row: {i} / {rows}")

        progress_monitor.update(i, rows, names[i])

        ref_row = i - 1
        if unbounded:
            ref_row = i

        for j in range(columns):

            step_value = (j + 1) * step_size
            lg.debug(f"step_value:{step_value}")

            # if current sub-sack can hold at least one share
            if step_value >= costs[i]:
                lg.debug(f"STEP_VALUE({step_value}) >= COSTS[{i}]({costs[i]})")

                # Get the previous max profit for this sub-capacity
                prev_max = grid_values[i - 1][j] if i > 0 else 0

                # Get the current Share profit
                current_value = profits[i]

                # Search for the previous max of the remaining capacity
                filling_index = j - int(costs[i] // step_size)

                # Get the current max profit for this sub-capacity
                current_max = current_value
                current_max += (
                    grid_values[ref_row][filling_index] if filling_index > -1 else 0
                )

                lg.debug(f"prev_max:{prev_max}")
                lg.debug(f"curr_max:{current_max}, current_value:{current_value}, filling_index:{filling_index}")

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

                # lg.debug(f"GRID VALUES: {grid_values}")
                # lg.debug(f"GRID SHARES: {grid_shares}")

            else:
                lg.debug(f"STEP_VALUE({step_value}) < COSTS[{i}]({costs[i]})")
                grid_values[i][j] = grid_values[i - 1][j] if i > 0 else 0
                grid_shares[i][j] = grid_shares[i - 1][j] if i > 0 else None

    progress_monitor.update(i + 1, rows, "Finished")
    return grid_values[i][j], grid_shares[i][j]


if __name__ == "__main__":
    print("\n")
    lg.info("RUN OPTIMIZED algorithm")

    pd_parse("dataFinance-sample.csv")
    # pd_parse("dataFinance.csv")
