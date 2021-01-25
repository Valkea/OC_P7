#! /usr/bin/env python3
# coding: utf-8

import pandas as pd


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

    names = ["Water", "Book", "Food", "Jacket", "Camera"]
    costs = [3, 1, 2, 2, 1]
    profits = [10, 3, 9, 5, 6]

    knapsack_dynamic_programming(costs, profits)
    # search(costs, profits)


def knapsack_dynamic_programming(costs, profits):
    pass


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
