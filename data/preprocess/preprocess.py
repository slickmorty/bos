import pandas as pd
import numpy as np
from settings.settings import data_settings
import pathlib
from datetime import datetime

"""
def preprocess(data_name: str):

    csv_path = data_settings.csv_path
    data_path = csv_path + "/with_class/" + \
        f"{data_name}_slatr_{data_settings.sl_to_atr:02}" + ".csv"

    df = pd.read_csv(data_path)

    # TODO: change to fillna(0,inplace=True)
    df = df.dropna().reset_index(drop=True)

    buy = df[f"buy_{data_settings.tp_to_sl}"].copy()
    df["Buy"] = buy
    sell = df[f"sell_{data_settings.tp_to_sl}"].copy()
    df["Sell"] = sell

    tp_to_sl_s = data_settings.tp_to_sl_s
    for i in tp_to_sl_s:
        df.pop(f"buy_{i}")
        df.pop(f"sell_{i}")

    df.pop(df.windowsizes.name)
    df.pop(df.do_nothing.name)

    do_nothings = []
    for i in range(len(df)):
        if(buy.iloc[i] == 0 and sell.iloc[i] == 0):
            do_nothings.append(1)
        else:
            do_nothings.append(0)

    df["do_nothing"] = do_nothings
    for column in data_settings.relative_columns:
        df[f"{column}_C"] = (df[column] / df.Close)*100

    # ------------------------------------------------------
    # Saving all file + train and test dataframes

    path = csv_path + "/preprocessed/" + \
        f"{data_name}_slatr_{data_settings.sl_to_atr:02}"
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

    df.to_csv(
        path + f"/{data_name}_{data_settings.tp_to_sl:02}_slatr_{data_settings.sl_to_atr}.csv", index=False)

    df["DateTime"] = pd.to_datetime(
        df.pop("DateTime"), format=data_settings.date_time_format)
    train_df = df.loc[df.DateTime < datetime(
        data_settings.split_year, data_settings.split_month, data_settings.split_day)].reset_index(drop=True)
    test_df = df.loc[df.DateTime >= datetime(
        data_settings.split_year, data_settings.split_month, data_settings.split_day)].reset_index(drop=True)

    # n = df.shape[0]
    # train_df = df[:int((0.85)*n)].reset_index(drop=True)
    # test_df = df[int((0.85)*n):].reset_index(drop=True)

    train_df.to_csv(
        path + f"/train_{data_settings.tp_to_sl:02}.csv", index=False)
    test_df.to_csv(
        path + f"/test_{data_settings.tp_to_sl:02}.csv", index=False)

"""


def preprocess():

    # Loading data and making it ready

    df = pd.read_csv(
        f"{data_settings.csv_path}/with_class/{data_settings.data_name}.csv")

    train_starting_date = datetime(data_settings.train_split_year,
                                   data_settings.train_split_month,
                                   data_settings.train_split_day)

    df["DateTime"] = pd.to_datetime(
        df.pop("DateTime"), format=data_settings.date_time_format)
    df = df.loc[df.DateTime > train_starting_date].reset_index(drop=True)

    print("Number of rows with na values:", df.shape[0] - df.dropna().shape[0])
    df = df.dropna().reset_index(drop=True)

    date_time = df.pop("DateTime")
    df.pop(df.windowsizes.name)
    df.pop(df.do_nothing.name)

    for column in data_settings.relative_columns:
        if column in df.columns:
            new_column = df[column].div(df.Close).mul(100)
            new_column.name = f"{column}_C"
            df = pd.concat([df, new_column], axis=1)

    moving_averages = [column for column in data_settings.relative_columns if (
        "SMA" in column) or ("EMA" in column)]

    for column in moving_averages[:]:
        moving_averages.remove(column)
        for i in moving_averages[:]:
            new_column = df[f"{column}"].div(df[f"{i}"])
            new_column.name = f"{column}/{i}"
            df = pd.concat([df, new_column], axis=1)

    #TODO: Check
    print("Number of rows with na values:", df.shape[0] - df.dropna().shape[0])
    df.fillna(0, inplace=True)
    df.replace(np.inf, 1e15, inplace=True)

    df["DateTime"] = pd.to_datetime(
        date_time, format=data_settings.date_time_format)

    df.to_csv(data_settings.csv_path + f"/{data_name}.csv", index=False)


if __name__ == "__main__":
    data_name = data_settings.data_name
    preprocess(data_name)
