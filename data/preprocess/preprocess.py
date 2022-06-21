import pandas as pd
import numpy as np
from settings.settings import data_settings
import pathlib


def main(data_name: str):

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

    buy = df.buy_2
    df.pop(df.buy_1.name)
    # df.pop(df.buy_2.name)
    df.pop(df.buy_4.name)
    df.pop(df.buy_8.name)
    df.pop(df.buy_16.name)

    sell = df.sell_2
    df.pop(df.sell_1.name)
    # df.pop(df.sell_2.name)
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
    df.rename(mapper={buy.name: "Buy", sell.name: "Sell"},
              axis="columns", inplace=True)
    df["do_nothing"] = do_nothings
    df["DateTime"] = date_time

    # Make relative columns
    relative_columns = ["BOLLINGER_HBAND",
                        "BOLLINGER_LBAND",
                        "BOLLINGER_MAVG",
                        "DONCHIAN_CHANNEL_HBAND",
                        "DONCHIAN_CHANNEL_LBAND",
                        "DONCHIAN_CHANNEL_MBAND",
                        "EMA_INDICATOR_12",
                        "EMA_INDICATOR_26",
                        "EMA_INDICATOR_50",
                        "EMA_INDICATOR_100",
                        "EMA_INDICATOR_200",
                        "SMA_INDICATOR_12",
                        "SMA_INDICATOR_26",
                        "SMA_INDICATOR_50",
                        "SMA_INDICATOR_100",
                        "SMA_INDICATOR_200",
                        "Open",
                        "High",
                        "Low",
                        "ICHIMOKU_A",
                        "ICHIMOKU_B",
                        "ICHIMOKU_BASE_LINE",
                        "ICHIMOKU_CONVERSION_LINE",
                        "KELTNER_CHANNEL_HBAND",
                        "KELTNER_CHANNEL_LBAND",
                        "KELTNER_CHANNEL_MBAND",
                        "NEGATIVE_VOLUME_INDEX",
                        "VOLUME_WEIGHTED_AVERAGE_PRICE"]

    for column in relative_columns:
        df[f"{column}_C"] = (df[column] / df.Close)*100

    # ------------------------------------------------------
    # Saving all file + train and test dataframes

    data_path = csv_path + "preprocessed/" + data_name + ".csv"
    df.to_csv(data_path, index=False)

    path = csv_path + "preprocessed/" + data_name
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

    n = df.shape[0]
    train_df = df[:int((0.95)*n)].reset_index(drop=True)
    test_df = df[int((0.95)*n):].reset_index(drop=True)

    train_df.to_csv(path+"/train.csv", index=False)
    test_df.to_csv(path+"/test.csv", index=False)


if __name__ == "__main__":
    data_name = data_settings.data_name
    main(data_name)
