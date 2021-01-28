#! /usr/bin/env python3
# coding: utf-8

import time
import logging as lg
import cProfile
import pstats

import pandas as pd
import numpy as np
import psutil

# import psutils

from utils import ProgressBar

progress_monitor = ProgressBar()

lg.basicConfig(filename="algo.log", filemode="w", level=lg.DEBUG)
# lg.disable(lg.DEBUG)


def main(file_name):
    """This function parse the given file, format the data and feed the algorithm function .

    Paramaters
    ----------
    file_name : str
        The 'path+filename' to the file to load
    """

    start_t = time.time()

    capacity = 500
    unbounded = True

    # --- LOAD data ---

    col_names = ["Shares", "Cost(Euro/share)", "Profit(% post 2 years)"]
    data = pd.read_csv(file_name)  # nrows=20
    df = pd.DataFrame(data, columns=col_names)

    # --- CLEAN data ---

    # remove invalid data
    df = df.replace([np.inf, -np.inf, 0.0], np.nan).dropna(axis=0)

    # remove SHARES whos value is greater than the capacity
    df = df[df[col_names[1]] <= capacity]

    # remove extra entries with the very same cost and profit
    df.drop_duplicates(subset=[col_names[1], col_names[2]], keep="last", inplace=True)

    # df2 = df[df[col_names[1]] == 16.5]
    # lg.debug(f"DF2: {df2}")

    # --- ADD computed data ---

    # df["ratio"] = df[col_names[2]] / df[col_names[1]]
    df["gain"] = df[col_names[1]] / 100.0 * df[col_names[2]]

    lg.debug(df)

    # --- PREPARE data for the algorithm ---

    names = [x for x in df[col_names[0]]]
    costs = [x for x in df[col_names[1]]]
    profits = [x for x in df["gain"]]

    # --- CALL the algorithm ----
    profile = cProfile.Profile()
    profile.enable()
 
    profit, share_indexes = search(costs, profits, capacity, names, unbounded)

    profile.disable()
    ps = pstats.Stats(profile)

    # --- PARSE the returned values ---

    if share_indexes:

        results = {}
        for share_index in share_indexes:
            results[names[share_index]] = (
                share_indexes.count(share_index),
                costs[share_index],
            )

        print("\n" * 4, " TOP 1 ".center(50, "*"), sep="", end="\n\n")

        print(f"The maximum profit is {profit:.2f}€ \n\nwith the following shares:\n")
        for k, v in results.items():
            print(f"- {k} [{v[1]}€] x {v[0]}")

        total = sum([v[0] * v[1] for k, v in results.items()])
        print(f"\nTotal: {total:.2f}€")
    else:
        print("\nNO MATCH FOUND")

    # --- CLOSE ---

    end_t = time.time()
    print("", "*" * 50, f"\nTime: {end_t-start_t} seconds", sep="\n", end="\n" * 2)

    ps.sort_stats('cumtime', 'ncalls')
    ps.print_stats(10)


def search(costs, profits, capacity, names=[], unbounded=False):
    """This function search for the optimal combination of the provided data.

    This implementation of the 'unlimited knapsack problem' tries to find
    the combination that best maximize the combined profits.

    In order to reach an O(n) temporal complexity, this version is implemented
    using a dynamic programming approach.

    Parameters
    ----------
    costs: list[Number]
        A list containing the cost of the actions to select
    profits: list[Number]
        A list containing the profit of the actions to select
    capacity: int
        The target value to reach with the combined costs of the selected actions
    names: list[str]
        The names of the provided actions
    unbounded: bool
        Define if the provided actions can be re-used (unbound) or not (bound)

    Returns
    -------
    int
        The optimal profit for the given actions and capacity
    list[int]
        The list of the indexes of the actions selected to reach the optimal profit
    """

    step_size = 0.1
    precision_scale = 100

    # --- INITIALIZE the grids / matrix ---

    rows = len(costs)
    columns = round(capacity / step_size)
    lg.debug(f"step_size:{step_size}, rows:{rows}, columns:{columns}")

    # grid_costs = np.zeros([rows, columns])
    grid_values = np.zeros([rows, columns])
    grid_shares = [[None for x in range(columns)] for y in range(rows)]

    # --- RUN the algorithm ---
    lg.info(f"PSUTIL BEFORE: {psutil.virtual_memory()}")

    # for each provided action
    for i in range(rows):

        progress_monitor.update(i, rows, names[i])

        ref_row = i - 1
        if unbounded:
            ref_row = i

        # for each sub-sack in the grid
        for j in range(columns):

            step_value = (j + 1) * step_size
            # lg.debug(f"step_value:{step_value}")

            # if current sub-sack can hold at least one share
            if step_value >= costs[i]:
                # lg.debug(f"STEP_VALUE({step_value}) >= COSTS[{i}]({costs[i]}) ==> profit:{profits[i]*precision_scale}")

                # Get the previous max profit for this sub-capacity
                prev_max = grid_values[i - 1][j] if i > 0 else 0

                # Get the current max profit for this sub-capacity
                current_value = profits[i] * precision_scale
                current_max = current_value

                unused = step_value - costs[i]
                # lg.debug(f'UNUSED: {unused}')
                filling_index = round(unused / step_size) - 1
                # lg.debug(f'FILLING INDEX: {filling_index}')
                current_max += (
                    grid_values[ref_row][filling_index] if filling_index > -1 else 0
                )

                # lg.debug(f"prev_max:{prev_max}")
                # lg.debug(
                #      f"curr_max:{current_max}, current_value:{current_value}, filling_index:{filling_index}"
                # )

                # Save the new max profit
                new_max = max(prev_max, current_max)
                grid_values[i][j] = new_max
                # lg.debug(f"GRID VALUES: \n{grid_values}")

                # Save the corresponding shares & costs
                if new_max == prev_max:
                    grid_shares[i][j] = grid_shares[i - 1][j]
                else:
                    grid_shares[i][j] = [i]
                    if filling_index > -1:
                        if grid_shares[ref_row][filling_index]:
                            grid_shares[i][j].extend(
                                grid_shares[ref_row][filling_index]
                            )
                # lg.debug(f"GRID SHARES: {grid_shares}")

            # if current sub-sack CAN'T hold at least one share
            else:
                # lg.debug(f"STEP_VALUE({step_value}) < COSTS[{i}]({costs[i]})")
                grid_values[i][j] = grid_values[i - 1][j] if i > 0 else 0
                grid_shares[i][j] = grid_shares[i - 1][j] if i > 0 else None

            # lg.info(f"PSUTIL IN LOOP J: {psutil.virtual_memory()}")

    # --- RETURN values ---
    # for row in grid_values:
    #     lg.debug(f"GRID ROW VALUES: {row}")
    lg.info(f"PSUTIL AFTER: {psutil.virtual_memory()}")

    progress_monitor.update(i + 1, rows, "Finished OPTIMIZED search")
    return grid_values[i][j] / precision_scale, grid_shares[i][j]


if __name__ == "__main__":
    print("\n")
    lg.info("RUN OPTIMIZED algorithm")

    # profile = cProfile.Profile()
    # profile.runcall(main, "dataFinance-sample.csv")
    # ps = pstats.Stats(profile)
    # ps.print_stats()

    main("dataFinance-sample.csv")
    # main("dataFinance.csv")
