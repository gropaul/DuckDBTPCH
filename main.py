import duckdb
import json

SCALE_FACTOR = 30

def main():
    con = duckdb.connect(':memory:')

    # install TPCH extension
    con.execute(f"INSTALL tpch;LOAD tpch;CALL dbgen(sf = {SCALE_FACTOR});")

    # set up profiling
    con.execute("PRAGMA enable_profiling = 'json';")
    con.execute("PRAGMA profiling_output = 'profile.json';")

    results = {}

    print("Running queries...")

    # run query 1 to 22
    for i in range(1, 23):
        con.execute(f"PRAGMA tpch({i});")
        latency = con.execute("SELECT latency FROM 'profile.json';").fetchall()[0][0]
        results[i] = latency


    # save result as json
    with open('results.json', 'w') as f:
        json.dump(results, f, indent=4)


if __name__ == "__main__":
    main()