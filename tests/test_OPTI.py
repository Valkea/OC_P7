#! /usr/bin/env python3
# coding: utf-8

"""
The purpose of this module is to test the OPTIMIZED version of the algorithms

>> python -m pytest (otherwise pytest won't find the script)

"""

from OPTI__two_years_best_invest import search


class TestOPTI:
    @classmethod
    def setup_class(cls):
        pass

    def setup_method(self):
        pass

    def test_bounded_01(self):
        names = ["Water", "Book", "Food", "Jacket", "Camera"]
        costs = [3, 1, 2, 2, 1]
        profits = [10, 3, 9, 5, 6]
        capacity = 6
        unbounded = False

        profit, share_indexes = search(
            costs, profits, capacity, names, unbounded
        )

        assert profit == 25
        assert len(share_indexes) == 3
        assert 0 in share_indexes  # Water
        assert 2 in share_indexes  # Food
        assert 4 in share_indexes  # Camera

    def test_bounded_02(self):
        names = ["WA", "GT", "NG", "BM", "SPC"]
        costs = [0.5, 0.5, 1, 2, 0.5]
        profits = [7, 6, 9, 9, 8]
        capacity = 2
        unbounded = False

        profit, share_indexes = search(
            costs, profits, capacity, names, unbounded
        )

        assert profit == 24
        assert len(share_indexes) == 3
        assert 0 in share_indexes  # WA
        assert 2 in share_indexes  # NG
        assert 4 in share_indexes  # SPC

    def test_bounded_03(self):
        names = ["Guitar", "Stereo", "Laptop", "IPhone"]
        costs = [1, 4, 3, 1]
        profits = [1500, 3000, 2000, 2000]
        capacity = 4
        unbounded = False

        profit, share_indexes = search(
            costs, profits, capacity, names, unbounded
        )

        assert profit == 4000
        assert len(share_indexes) == 2
        assert 2 in share_indexes  # Laptop
        assert 3 in share_indexes  # Iphone

    def test_unbounded_03(self):
        names = ["Guitar", "Stereo", "Laptop", "IPhone"]
        costs = [1, 4, 3, 1]
        profits = [1500, 3000, 2000, 2000]
        capacity = 4
        unbounded = True

        profit, share_indexes = search(
            costs, profits, capacity, names, unbounded
        )

        assert profit == 8000
        assert len(share_indexes) == 4
        assert 2 not in share_indexes  # Laptop
        assert 3 in share_indexes  # Iphone
