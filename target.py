from concurrent.futures import ProcessPoolExecutor
from settings.settings import data_settings
import pandas as pd


def make_target(df: pd.DataFrame, target_path: str):

    stop_loss_to_atr_ratio = data_settings.stop_loss_to_atr_ratio

    # 0 --> sell 1      5 --> buy 1
    # 1 --> sell 2      6 --> buy 2
    # 2 --> sell 4      7 --> buy 4
    # 3 --> sell 8      8 --> buy 8
    # 4 --> sell 16     9 --> buy 16

    buy_1 = []
    buy_2 = []
    buy_4 = []
    buy_8 = []
    buy_16 = []

    sell_1 = []
    sell_2 = []
    sell_4 = []
    sell_8 = []
    sell_16 = []

    do_nothing = []

    windowsizes = []

    for i in range(len(df)):

        sl = df.ATR.iloc[i] * stop_loss_to_atr_ratio

        do_nothing_found: int = 0

        buy_sl: int = 0
        buy_1_found: int = 0
        buy_2_found: int = 0
        buy_4_found: int = 0
        buy_8_found: int = 0
        buy_16_found: int = 0

        sell_sl: int = 0
        sell_1_found: int = 0
        sell_2_found: int = 0
        sell_4_found: int = 0
        sell_8_found: int = 0
        sell_16_found: int = 0

        buy = False
        sell = False
        for w in range(i+1, min(i+289, len(df))):

            if(not buy_sl and df.Low.iloc[w] <= df.Close.iloc[i] - sl):
                buy_sl = 1

            elif(not buy_16_found and not sell and df.High.iloc[w] >= df.Close.iloc[i] + 16*sl):
                buy_16_found = 1
                buy_8_found = 1
                buy_4_found = 1
                buy_2_found = 1
                buy_1_found = 1
                buy = True

            elif(not buy_8_found and not sell and df.High.iloc[w] >= df.Close.iloc[i] + 8*sl):
                buy_8_found = 1
                buy_4_found = 1
                buy_2_found = 1
                buy_1_found = 1
                buy = True

            elif(not buy_4_found and not sell and df.High.iloc[w] >= df.Close.iloc[i] + 4*sl):
                buy_4_found = 1
                buy_2_found = 1
                buy_1_found = 1
                buy = True

            elif(not buy_2_found and not sell and df.High.iloc[w] >= df.Close.iloc[i] + 2*sl):
                buy_2_found = 1
                buy_1_found = 1
                buy = True

            elif(not buy_1_found and not sell and df.High.iloc[w] >= df.Close.iloc[i] + 1*sl):
                buy_1_found = 1
                buy = True

            if(not sell_sl and df.High.iloc[w] >= df.Close.iloc[i] + sl):
                sell_sl = 1

            elif(not sell_16_found and not buy and df.Low.iloc[w] <= df.Close.iloc[i] - 16*sl):
                sell_16_found = 1
                sell_8_found = 1
                sell_4_found = 1
                sell_2_found = 1
                sell_1_found = 1
                sell = True

            elif(not sell_8_found and not buy and df.Low.iloc[w] <= df.Close.iloc[i] - 8*sl):
                sell_8_found = 1
                sell_4_found = 1
                sell_2_found = 1
                sell_1_found = 1
                sell = True

            elif(not sell_4_found and not buy and df.Low.iloc[w] <= df.Close.iloc[i] - 4*sl):
                sell_4_found = 1
                sell_2_found = 1
                sell_1_found = 1
                sell = True

            elif(not sell_2_found and not buy and df.Low.iloc[w] <= df.Close.iloc[i] - 2*sl):
                sell_2_found = 1
                sell_1_found = 1
                sell = True

            elif(not sell_1_found and not buy and df.Low.iloc[w] <= df.Close.iloc[i] - 1*sl):
                sell_1_found = 1
                sell = True

            if((buy_sl and buy) or (sell_sl and sell) or (buy_16_found or sell_16_found)):
                break

        if(not buy and not sell):
            do_nothing_found = 1

        buy_1.append(buy_1_found)
        buy_2.append(buy_2_found)
        buy_4.append(buy_4_found)
        buy_8.append(buy_8_found)
        buy_16.append(buy_16_found)

        sell_1.append(sell_1_found)
        sell_2.append(sell_2_found)
        sell_4.append(sell_4_found)
        sell_8.append(sell_8_found)
        sell_16.append(sell_16_found)

        do_nothing.append(do_nothing_found)
        windowsizes.append(w-i)

        print(f"{i=}", "window size:", w-i)

    df["buy_1"] = buy_1
    df["buy_2"] = buy_2
    df["buy_4"] = buy_4
    df["buy_8"] = buy_8
    df["buy_16"] = buy_16

    df["sell_1"] = sell_1
    df["sell_2"] = sell_2
    df["sell_4"] = sell_4
    df["sell_8"] = sell_8
    df["sell_16"] = buy_16

    df["do_nothing"] = do_nothing
    df["windowsizes"] = windowsizes
    df.to_csv(target_path, index=False)


def main():
    target_paths = data_settings.data_with_targets_parts_paths
    dfs = [pd.read_csv(path)
           for path in data_settings.data_without_targets_parts_paths]
    with ProcessPoolExecutor() as executor:
        executor.map(make_target, dfs, target_paths)


if __name__ == "__main__":

    main()
