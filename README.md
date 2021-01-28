# AlgoInvest&Trade exercise

This project contains two Python 3 scripts trying to find the best 'share' combination from the provided data.
The goal is to select the set of shares providing the best profit given that it needs to invest exactly 500.

I identified this problem as the "Unlimited Knapsack problem", because we can reuse the same share again and again.

The first script use a recursive "brute force" approach, whereas the second one use a dynamic programming "optimized" approach.

## Installation

In order to use this script, you need to follow the steps below:

### First, 
let's duplicate the project github repository

```bash
>>> git clone https://github.com/Valkea/OC_P7.git
>>> cd OC_P7
```

### Secondly,
let's create a virtual environment and install the required Python libraries

(Linux or Mac)
```bash
>>> python3 -m venv venv
>>> source venv/bin/activate
>>> pip install -r requirements.txt
```

(Windows):
```bash
>>> py -m venv venv
>>> .\venv\Scripts\activate
>>> py -m pip install -r requirements.txt
```

## Running the scripts
we can start the algorithms using the following commands

```bash
>>> python3 BRUT__two_years_best_invest.py  # should crash because of the maximum recursion limit
>>> python3 OPTI__two_years_best_invest.py
```

But in order to run the algorithms on the sample dataset instead of the full one, we can add the -s or --sample argument

```bash
>>> python3 BRUT__two_years_best_invest.py --sample
>>> python3 OPTI__two_years_best_invest.py -s
```

And if we want to see the profiling information, we can also add the -p or --profile argument to the command line
```bash
>>> python3 BRUT__two_years_best_invest.py --profile
>>> python3 OPTI__two_years_best_invest.py -p
```

[Some combined options' examples]
```bash
>>> python3 BRUT__two_years_best_invest.py --sample --profile 
>>> python3 OPTI__two_years_best_invest.py -sp
```

## Result's display example

```bash
◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼ 20/20 rows
                              Finished OPTIMIZED search


********************* TOP 1 **********************

The maximum profit is 134.05€ 

with the following shares:

- Share-9 [17€] x 29
- Share-17 [5€] x 1
- Share-16 [2€] x 1

Total: 500.00€

**************************************************

Time: 0.33463215827941895 seconds
```


## PEP8

The scripts were developped using 'vim-Flake8' and 'black' modules to enforce the PEP8.

## Tests
You can test the modules of the script with pytest.

```bash
>>> python3 -m pytest
```
**Warning**
Don't run `pytest` directly, use `python3 -m pytest`.
Otherwise the test modules won't find some of the files.

## Ouputs

### Logs
you can find the logs in the algo.log file.
(but most logging action are currently disabled because even with the appriopriate level, it really slow down the search algorithms)

## License
[MIT](https://choosealicense.com/licenses/mit/)
