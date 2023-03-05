from math import inf as _all
from time import sleep, perf_counter_ns

import pandas

import libs
from libs import data

START = 0
END = _all
BATCH_SIZE = 250


def _format_ns(ns: int) -> str:
    s = ns / (10 ** 9)
    s = round(s, 3)
    return f"{s} seconds"


def main():
    global END

    t0 = perf_counter_ns()
    print("Initializing...")
    libs.init()
    print("Initialized.")

    dataset = data.load_dataset()
    print("Loaded Dataset.")
    dataset = dataset.where(pandas.notna(dataset), None)
    dataset = [_.to_dict() for _ in dataset.iloc]

    END = min(len(dataset), END)

    print(f"Dataset finished processing. {len(dataset)} entries found.")

    for i in range(START, END, BATCH_SIZE):
        _END = min(END, i + BATCH_SIZE)
        t1 = perf_counter_ns()
        print(f"Inserting `{i + 1}` to `{_END}`")
        libs.upsert_articles(dataset[i: _END])
        t2 = perf_counter_ns()
        print(f"Inserted `{i + 1}` to `{_END}.")
        print(f"Took {_format_ns(t2 - t1)}.`")
        print(f"{_format_ns(t2 - t0)} since start has elapsed.`")
        sleep(5)

    print("Tearing down...")
    libs.teardwn()
    print("Teardown finished.\n\n")
    tf = perf_counter_ns()
    print(f"Took {_format_ns(tf - t0)} to insert {END - START} records.")


if __name__ == '__main__':
    main()
