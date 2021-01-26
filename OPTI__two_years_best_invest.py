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


def main(file_name):
    """This function parse the given file, format the data and feed the algorithm function .

    Paramaters
    ----------
    file_name : str
        The 'path+filename' to the file to load
    """

    start_t = time.time()

    # --- LOAD data ---

    col_names = ["Shares", "Cost(Euro/share)", "Profit(% post 2 years)"]
    data = pd.read_csv(file_name)  # nrows=20
    df = pd.DataFrame(data, columns=col_names)

    # --- CLEAN data ---

    df = df.replace([np.inf, -np.inf, 0.0], np.nan).dropna(axis=0)
    lg.debug(df)

    # --- PREPARE data for the algorithm ---

    names = [x for x in df[col_names[0]]]
    costs = [x for x in df[col_names[1]]]
    profits = [x for x in df[col_names[2]]]
    capacity = 500
    unbounded = True

    # --- CALL the algorithm ----

    profit, share_indexes = knapsack_dynamic_programming(
        costs, profits, capacity, names, unbounded
    )

    # --- PARSE the returned values ---

    results = {}
    for share_index in share_indexes:
        results[names[share_index]] = share_indexes.count(share_index)

    print("\n\n")

    print(f"The maximum profit is {profit} \n\nwith the following shares:\n")
    for k, v in results.items():
        print(f"- {k} x {v}")

    # --- CLOSE ---

    end_t = time.time()
    print(f"\nTime: {end_t-start_t} seconds")


def knapsack_dynamic_programming(costs, profits, capacity, names=[], unbounded=False):
    """This function tries to find the best combination using the provided parameters

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

    step_size = min(costs)
    # if step_size < 1:  # TODO
    #    step_size = 1

    # --- INITIALIZE the grids / matrix ---

    rows = len(costs)
    columns = ceil(capacity / step_size)
    lg.debug(f"step_size:{step_size}, rows:{rows}, columns:{columns}")

    grid_values = np.zeros([rows, columns])
    grid_shares = [[None for x in range(columns)] for y in range(rows)]

    # --- RUN the algorithm ---

    # for each provided action
    for i in range(rows):

        progress_monitor.update(i, rows, names[i])

        ref_row = i - 1
        if unbounded:
            ref_row = i

        # for each sub-sack in the grid
        for j in range(columns):

            step_value = (j + 1) * step_size
            lg.debug(f"step_value:{step_value}")

            # if current sub-sack can hold at least one share
            if step_value >= costs[i]:
                lg.debug(f"STEP_VALUE({step_value}) >= COSTS[{i}]({costs[i]})")

                # Get the previous max profit for this sub-capacity
                prev_max = grid_values[i - 1][j] if i > 0 else 0

                # Get the current max profit for this sub-capacity
                current_value = profits[i]
                current_max = current_value

                filling_index = j - int(costs[i] // step_size)
                current_max += (
                    grid_values[ref_row][filling_index] if filling_index > -1 else 0
                )

                lg.debug(f"prev_max:{prev_max}")
                lg.debug(
                    f"curr_max:{current_max}, current_value:{current_value}, filling_index:{filling_index}"
                )

                # Set the new max profit
                new_max = max(prev_max, current_max)
                grid_values[i][j] = new_max
                # lg.debug(f"GRID VALUES: {grid_values}")

                # Set the corresponding shares
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
                lg.debug(f"STEP_VALUE({step_value}) < COSTS[{i}]({costs[i]})")
                grid_values[i][j] = grid_values[i - 1][j] if i > 0 else 0
                grid_shares[i][j] = grid_shares[i - 1][j] if i > 0 else None

    # --- RETURN values ---
    progress_monitor.update(i + 1, rows, "Finished")
    return grid_values[i][j], grid_shares[i][j]


if __name__ == "__main__":
    print("\n")
    lg.info("RUN OPTIMIZED algorithm")

    main("dataFinance-sample.csv")
    # main("dataFinance.csv")
