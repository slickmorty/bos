from concurrent.futures import ProcessPoolExecutor

from sklearn import datasets
from settings.settings import data_settings
import pandas as pd
import pathlib


def make_target(df: pd.DataFrame, target_path: str):
    """
        1- Get list of ratios from data_settings
        2- Sort them
        3- A list of buys and sells which contains a list for each ratio
        4- Start the main loop with i as variable
        5- Start the loop within the other one for doing the windowing stuff
        6- It's ez to understand no need to explain nevermind :)
    """
    window_size = data_settings.sl_window
    sl_to_atr = data_settings.sl_to_atr
    target_tp_to_sl_s = sorted(data_settings.tp_to_sl_s)

    # 0 --> sell 1          6  --> buy 1
    # 1 --> sell 1.25       7  --> buy 1.25
    # 2 --> sell 1.5        8  --> buy 1.5
    # 3 --> sell 1.75       9  --> buy 1.75
    # 4 --> sell 2          10 --> buy 2
    # 5 --> sell 4          11 --> buy 4

    buys = [[] for _ in target_tp_to_sl_s]
    sells = [[] for _ in target_tp_to_sl_s]

    do_nothing = []
    windowsizes = []

    for i in range(len(df)):

        sl = max(df.AVERAGE_TRUE_RANGE.iloc[i],
                 df.AVERAGE_TRUE_RANGE.mean()) * sl_to_atr

        do_nothing_found: int = 0

        buys_found = [0 for _ in target_tp_to_sl_s]
        buy_sl_hit: int = 0

        sells_found = [0 for _ in target_tp_to_sl_s]
        sell_sl_hit: int = 0

        bought = False
        sold = False
        n = len(target_tp_to_sl_s)
        for w in range(i+1, min(i+(window_size+1), len(df))):

            if(not buy_sl_hit and df.Low.iloc[w] <= df.Close.iloc[i] - sl):
                buy_sl_hit = 1

            else:
                for index, ratio in enumerate(target_tp_to_sl_s[::-1]):
                    if(not buys_found[-(index+1)] and not sold and df.High.iloc[w] >= df.Close.iloc[i] + ratio * sl):
                        buys_found[:(
                            n-index)] = [1 for _ in range(len(buys_found[:(n-index)]))]
                        bought = True
                        break

            if(not sell_sl_hit and df.High.iloc[w] >= df.Close.iloc[i] + sl):
                sell_sl_hit = 1

            else:
                for index, ratio in enumerate(target_tp_to_sl_s[::-1]):
                    if(not sells_found[-(index+1)] and not bought and df.Low.iloc[w] <= df.Close.iloc[i] - ratio * sl):
                        sells_found[:(
                            n-index)] = [1 for _ in range(len(sells_found[:(n-index)]))]
                        bought = True
                        break

            if((buy_sl_hit and bought) or (sell_sl_hit and sold) or (buys_found[-1] or buys_found[-1])):
                break

        if(not bought and not sold):
            do_nothing_found = 1

        for _, values in enumerate(zip(buys, buys_found)):
            values[0].append(values[1])

        for _, values in enumerate(zip(sells, sells_found)):
            values[0].append(values[1])

        do_nothing.append(do_nothing_found)
        windowsizes.append(w-i)

        print(f"{i=}", "window size:", w-i)

    for _, values in enumerate(zip(buys, target_tp_to_sl_s)):
        df[f"buy_{values[1]}"] = values[0]

    for _, values in enumerate(zip(sells, target_tp_to_sl_s)):
        df[f"sell_{values[1]}"] = values[0]

    df["do_nothing"] = do_nothing
    df["windowsizes"] = windowsizes
    df.to_csv(target_path, index=False)
    return


def add_targets(data_name: str):

    window_size = data_settings.sl_window
    parts = 8

    csv_path = data_settings.csv_path
    cleaed_data_path = csv_path + "/with_indicator/" + data_name + ".csv"
    df = pd.read_csv(cleaed_data_path)

    n = df.shape[0] // parts
    dfs = [df[i * n:(i+1)*n + (window_size+1)].reset_index(drop=True)
           for i in range(parts)]

    target_paths = [
        f"D:/dev/workspace/vscode/python/bos/data/csv/with_class/{data_name}_part_1.csv",
        f"D:/dev/workspace/vscode/python/bos/data/csv/with_class/{data_name}_part_2.csv",
        f"D:/dev/workspace/vscode/python/bos/data/csv/with_class/{data_name}_part_3.csv",
        f"D:/dev/workspace/vscode/python/bos/data/csv/with_class/{data_name}_part_4.csv",
        f"D:/dev/workspace/vscode/python/bos/data/csv/with_class/{data_name}_part_5.csv",
        f"D:/dev/workspace/vscode/python/bos/data/csv/with_class/{data_name}_part_6.csv",
        f"D:/dev/workspace/vscode/python/bos/data/csv/with_class/{data_name}_part_7.csv",
        f"D:/dev/workspace/vscode/python/bos/data/csv/with_class/{data_name}_part_8.csv"
    ]

    with ProcessPoolExecutor() as executor:
        executor.map(make_target, dfs, target_paths)

    dfs = [pd.read_csv(target_path) for target_path in target_paths]

    df = pd.concat([part[:-(window_size+1)]
                   for part in dfs]).reset_index(drop=True)

    with_class_data_path = csv_path + "/with_class/" + \
        f"{data_name}_slatr_{data_settings.sl_to_atr:02}" + ".csv"

    df.to_csv(with_class_data_path, index=False)

    for path in target_paths:
        pathlib.Path(path).unlink(missing_ok=True)


if __name__ == "__main__":
    pass
