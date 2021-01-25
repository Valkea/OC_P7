#! /usr/bin/env python3
# coding: utf-8

from math import ceil

import pandas as pd
import numpy as np


def pd_parse(file_name):
    col_names = ["Shares", "Cost(Euro/share)", "Profit(% post 2 years)"]
    data = pd.read_csv(file_name)  # nrows=20
    df = pd.DataFrame(data, columns=col_names)

    # df["ratio"] = df[col_names[1]] / df[col_names[0]]
    # df = df.replace([np.inf, -np.inf], np.nan).dropna(axis=0)
    # df = df.sort_values(by=["ratio", col_names[1], col_names[0]], ascending=False)

    print(df)

    names = [x for x in df[col_names[0]]]
    costs = [x for x in df[col_names[1]]]
    profits = [x for x in df[col_names[2]]]
    capacity = 500

    names = ["Water", "Book", "Food", "Jacket", "Camera"]
    costs = [3, 1, 2, 2, 1]
    profits = [10, 3, 9, 5, 6]
    capacity = 6

    profit, share_indexes = knapsack_dynamic_programming(costs, profits, capacity)

    print(
        f"The maximum profit is: {profit} with the following shares: {[names[x] for x in share_indexes]}"
    )
    # search(costs, profits)


def knapsack_dynamic_programming(costs, profits, capacity):

    step = min(costs)
    rows = len(costs)
    columns = ceil(capacity / step)
    print("STEP:", step, rows, columns)

    grid_values = np.zeros([rows, columns])
    # grid_shares = [[None]*columns]*rows
    grid_shares = [[None for x in range(columns)] for y in range(rows)]
    print("GRID:", grid_values)
    print("GRID:", grid_shares)

    for i in range(len(costs)):
        for j in range(0, capacity, step):

            print("COST COND:", j + 1, ">=", costs[i])

            # if current sub-sack can hold at least one share
            if j + 1 >= costs[i]:
                print("OK")

                prev_max = (
                    grid_values[i - 1][j] if i > 0 else 0
                )  # Get the previous max profit for this sub-capacity

                current_value = profits[i]  # Get the current Share profit
                filling_index = (
                    j - costs[i]
                )  # Search for the previous max of the remaining capacity

                if filling_index > -1:
                    current_max = current_value + grid_values[i - 1][filling_index]
                else:
                    current_max = current_value

                print(prev_max, current_value, filling_index, current_max)
                new_max = max(prev_max, current_max)
                grid_values[i][j] = new_max

                if new_max == prev_max:
                    grid_shares[i][j] = grid_shares[i - 1][j]
                else:
                    grid_shares[i][j] = [i]
                    if filling_index > -1:
                        if grid_shares[i - 1][filling_index]:
                            grid_shares[i][j].extend(grid_shares[i - 1][filling_index])

                print(grid_values)
                print(np.array(grid_shares))

            else:
                print("PAS OK")
                grid_values[i][j] = grid_values[i - 1][j] if i > 0 else 0

            print(i, j, costs[i])
    return grid_values[i][j], grid_shares[i][j]


# def search(costs, profits):
#
#     start_t = time.time()
#
#     # costs = [5, 2, 1]  # TODO tmp
#     # profits = [10, 2, 1]
#
#     capacity = 500
#     selected = set()
#     explored = set()
#     # recursive_call_3(costs, 0, depth, 0, selected=selected, explored=explored)
#     spend = recursive_call_4i(
#         costs, profits, capacity, explored=explored, selected=selected, num_selection=3
#     )
#     if spend == capacity:
#         print("\nMATCH FOUND\n")
#     else:
#         print("\nNO MATCH FOUND\n")
#         return
#
#     # for r in explored:
#     #    print(f"EXP==>[{r}]")
#     # print(len(explored))
#
#     sort_sequences = []
#     for r in selected:
#         cost = sum([costs[x] for x in r])
#         profit = sum([profits[x] for x in r])
#         sort_sequences.append((profit, [costs[x] for x in r], cost))
#         print(f"SEL==>[{r}] {cost} {profit}")
#
#     print()
#
#     sort_sequences = sorted(sort_sequences)
#     for r in sort_sequences:
#         print(f"SOR==>{r}")
#
#     best = sort_sequences[-1:]
#     print("\nBEST:", best)
#
#     print(len(selected))
#
#     end_t = time.time()
#
#     print(f"Time: {end_t-start_t} seconds")


if __name__ == "__main__":
    pd_parse("dataFinance-sample.csv")
    # pd_parse("dataFinance.csv")
