#!/usr/bin/env python3

import os
import time
import random
from multiprocessing.pool import Pool, ThreadPool

import pandas as pd
import hiplot as hip

from savvy import BusinessModel


def run_one(iteration, param1, param2):
    savvy_possibility = BusinessModel(
        param1=param1,
        param2=param2,
    )
    savvy_possibility.run()
    return savvy_possibility

def prepare_tasks():
    tasks = []
    for iteration in range(0, 20):
        for starting_deposits in range(0, 50, 5):
            for growth_pct in range(0, 10, 2):
                this_task = [
                    iteration,
                    starting_deposits, # 1_000_000, 1_500_000, 2_500_000, 5_000_000
                    growth_pct, # 2%-15%, 1% increments
                    average_user_yield, # 5%-20, 1% increments
                    starting_pol, # 0, 250_000, 500_000, 1_000_000, 2_000_000, 5_000_000
                    average_protocol_yield, # 10%-30%, 5% increments
                    protocol_fee_pct, # 5%-25%, 5% increments
                    buyback_rate_pct, # 10%-60%, 10% increments
                    expected_apr, # 4%-20%
                ]
                tasks.append(this_task)
    return tasks

def run_all(tasks):
    results_accumulator = []

    print("Starting simulation")
    start_time = time.time()

    with Pool(processes=7) as pool:
        results = pool.starmap(run_one, tasks)
        for savvy_possibility, param in zip(results, tasks):
            result = {
                **dict(zip(["iteration", "param1", "param2"], param)),
                "score": savvy_possibility.score,
            }

            results_accumulator.append(result)

    end_time = time.time()
    print(f"Finished in {end_time - start_time} seconds")

    return results_accumulator

def convert_to_dataframe(results_accumulator):
    df_values = [r.values() for r in results_accumulator]
    df_columns = results_accumulator[0].keys()
    df = pd.DataFrame(df_values, columns=df_columns)
    return df

def save(df, filename):
    print(f"Writing results to {filename}")
    df.to_csv(filename, index=False)
    print("Done")

def load(filename):
    df = pd.read_csv(filename)
    del df['iteration']
    return df

def plot(df, filename):
    h = hip.Experiment.from_dataframe(df)
    h.parameters_definition["score"].type = hip.ValueType.NUMERIC_LOG
    h.to_html(filename)

def main():
    tasks = prepare_tasks()
    results_accumulator = run_all(tasks)
    df = convert_to_dataframe(results_accumulator)

    path = os.path.abspath('.')
    save(df, filename=os.path.join(path, "var/results.csv.gz"))
    plot(df, filename=os.path.join(path, "docs/parameters.html"))

if __name__ == "__main__":
    main()
