#! /usr/bin/env python3
# coding: utf-8

def load_file(file_name):
    with open(file_name, 'r') as f:
        for line in f:
            print(line)

if __name__ == "__main__":
    load_file("dataFinance-sample.csv")
