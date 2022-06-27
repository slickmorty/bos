import pandas as pd
import numpy as np
from settings.settings import data_settings
import pathlib
from datetime import datetime


def preprocess(data_name: str):

    csv_path = data_settings.csv_path
    data_path = csv_path + "with_class/" + data_name + ".csv"
    df = pd.read_csv(data_path)

    df = df.dropna().reset_index(drop=True)

    date_time = pd.to_datetime(
        df.pop("DateTime"), format=data_settings.date_time_format)
    timestamps = date_time.map(pd.Timestamp.timestamp)

    day = 24  # hours
    year = (365.2425)*day
    five_year = 5 * year
    df["Day_sin"] = (np.sin(timestamps * (2 * np.pi / day)))  # /2
    df["Day_cos"] = (np.cos(timestamps * (2 * np.pi / day)))  # /2
    df["Year_sin"] = (np.sin(timestamps * (2 * np.pi / year)))  # /2
    df["Year_cos"] = (np.cos(timestamps * (2 * np.pi / year)))  # /2
    df["Five_Year_sin"] = (np.sin(timestamps * (2 * np.pi / year)))  # /2
    df["Five_Year_cos"] = (np.cos(timestamps * (2 * np.pi / year)))  # /2

    buy = df[f"buy_{data_settings.tp_to_sl}"].copy()
    df["Buy"] = buy
    df.pop(df.buy_1.name)
    df.pop(df.buy_2.name)
    df.pop(df.buy_4.name)
    df.pop(df.buy_8.name)
    df.pop(df.buy_16.name)

    sell = df[f"sell_{data_settings.tp_to_sl}"].copy()
    df["Sell"] = sell
    df.pop(df.sell_1.name)
    df.pop(df.sell_2.name)
    df.pop(df.sell_4.name)
    df.pop(df.sell_8.name)
    df.pop(df.sell_16.name)
    df.pop(df.windowsizes.name)
    df.pop(df.do_nothing.name)

    do_nothings = []
    for i in range(len(df)):
        if(buy.iloc[i] == 0 and sell.iloc[i] == 0):
            do_nothings.append(1)
        else:
            do_nothings.append(0)

    # df.rename(mapper={buy.name: "Buy", sell.name: "Sell"},
    #           axis="columns", inplace=True)
    df["do_nothing"] = do_nothings
    df["DateTime"] = date_time

    for column in data_settings.relative_columns:
        df[f"{column}_C"] = (df[column] / df.Close)*100

    # ------------------------------------------------------
    # Saving all file + train and test dataframes

    path = csv_path + "preprocessed/" + data_name
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

    df.to_csv(
        path + f"/{data_name}_{data_settings.tp_to_sl:02}.csv", index=False)

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


if __name__ == "__main__":
    data_name = data_settings.data_name
    preprocess(data_name)
