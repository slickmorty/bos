import ta
import pandas as pd
from settings.settings import data_settings
import numpy as np


def add_indicators(data_name: str):

    csv_path = data_settings.csv_path
    cleaed_data_path = csv_path + "/cleaned_mt_data/" + data_name + ".csv"

    df = pd.read_csv(cleaed_data_path)

    high_r = df["High"]
    low_r = df["Low"]
    close_r = df["Close"]
    volume_r = df["TickVol"]

    windows = tuple(data_settings.moving_average_windows)

    indicators_c = {
        # close_r
        "PPO": ta.momentum.ppo,
        "HIST": ta.momentum.ppo_hist,
        "PPO_SIGNAL": ta.momentum.ppo_signal,
        "ROC": ta.momentum.roc,
        "RSI": ta.momentum.rsi,
        "STOCHRSI": ta.momentum.stochrsi,
        "STOCHRSI_D": ta.momentum.stochrsi_d,
        "STOCHRSI_K": ta.momentum.stochrsi_k,
        "TSI": ta.momentum.tsi,
        "BOLLINGER_HBAND": ta.volatility.bollinger_hband,
        "BOLLINGER_HBAND_INDICATOR": ta.volatility.bollinger_hband_indicator,
        "BOLLINGER_LBAND": ta.volatility.bollinger_lband,
        "BOLLINGER_LBAND_INDICATOR": ta.volatility.bollinger_lband_indicator,
        "BOLLINGER_MAVG": ta.volatility.bollinger_mavg,
        "BOLLINGER_PBAND": ta.volatility.bollinger_pband,
        "BOLLINGER_WBAND": ta.volatility.bollinger_wband,
        "ULCER_INDEX": ta.volatility.ulcer_index,
        "DPO": ta.trend.dpo,
        "KST": ta.trend.kst,
        "KST_SIG": ta.trend.kst_sig,
        "MACD": ta.trend.macd,
        "MACD_DIFF": ta.trend.macd_diff,
        "MACD_SIGNAL": ta.trend.macd_signal,
        "STC": ta.trend.stc,
        "TRIX": ta.trend.trix,
        "CUMULATIVE_RETURN": ta.others.cumulative_return,
        "DAILY_LOG_RETURN": ta.others.daily_log_return,
        "DAILY_RETURN": ta.others.daily_return,
    }
    indicators_v = {
        # df["TickVol"]
        "PVO": ta.momentum.pvo,
        "PVO_HIST": ta.momentum.pvo_hist,
        "PVO_SIGNAL": ta.momentum.pvo_signal,
    }
    indicators_hlc = {
        # high_r,low_r,close_r
        "CCI": ta.trend.cci,
        "STOCH": ta.momentum.stoch,
        "STOCH_SIGNAL": ta.momentum.stoch_signal,
        "ULTIMATE_OSCILLATOR": ta.momentum.ultimate_oscillator,
        "WILLIAMS_R": ta.momentum.williams_r,
        "AVERAGE_TRUE_RANGE": ta.volatility.average_true_range,
        "DONCHIAN_CHANNEL_HBAND": ta.volatility.donchian_channel_hband,
        "DONCHIAN_CHANNEL_LBAND": ta.volatility.donchian_channel_lband,
        "DONCHIAN_CHANNEL_MBAND": ta.volatility.donchian_channel_mband,
        "DONCHIAN_CHANNEL_PBAND": ta.volatility.donchian_channel_pband,
        "DONCHIAN_CHANNEL_WBAND": ta.volatility.donchian_channel_wband,
        "KELTNER_CHANNEL_HBAND": ta.volatility.keltner_channel_hband,
        "KELTNER_CHANNEL_HBAND_INDICATOR": ta.volatility.keltner_channel_hband_indicator,
        "KELTNER_CHANNEL_LBAND": ta.volatility.keltner_channel_lband,
        "KELTNER_CHANNEL_LBAND_INDICATOR": ta.volatility.keltner_channel_lband_indicator,
        "KELTNER_CHANNEL_MBAND": ta.volatility.keltner_channel_mband,
        "KELTNER_CHANNEL_PBAND": ta.volatility.keltner_channel_pband,
        "KELTNER_CHANNEL_WBAND": ta.volatility.keltner_channel_wband,
        "ADX": ta.trend.adx,
        "ADX_NEG": ta.trend.adx_neg,
        "ADX_POS": ta.trend.adx_pos,
        "PSAR_DOWN": ta.trend.psar_down,
        "PSAR_DOWN_INDICATOR": ta.trend.psar_down_indicator,
        "PSAR_UP": ta.trend.psar_up,
        "PSAR_UP_INDICATOR": ta.trend.psar_up_indicator,
        "VORTEX_INDICATOR_NEG": ta.trend.vortex_indicator_neg,
        "VORTEX_INDICATOR_POS": ta.trend.vortex_indicator_pos,
    }
    indicators_hlv = {
        # high_r,low_r,df["TickVol"]
        "EASE_OF_MOVEMENT": ta.volume.ease_of_movement,
        "SMA_EASE_OF_MOVEMENT": ta.volume.sma_ease_of_movement,
    }
    indicators_hlcv = {
        # high_r,low_r,close_r,df["TickVol"]
        "ACC_DIST_INDEX": ta.volume.acc_dist_index,
        "CHAIKIN_MONEY_FLOW": ta.volume.chaikin_money_flow,
        "MONEY_FLOW_INDEX": ta.volume.money_flow_index,
        "VOLUME_WEIGHTED_AVERAGE_PRICE": ta.volume.volume_weighted_average_price,
    }
    indicators_cv = {
        # close_r,df["TickVol"]
        "FORCE_INDEX": ta.volume.force_index,
        "NEGATIVE_VOLUME_INDEX": ta.volume.negative_volume_index,
        "ON_BALANCE_VOLUME": ta.volume.on_balance_volume,
        "VOLUME_PRICE_TREND": ta.volume.volume_price_trend,
    }
    indicators_hl = {
        # high_r,low_r
        "AWESOME_OSCILLATOR": ta.momentum.awesome_oscillator,
        "ICHIMOKU_A": ta.trend.ichimoku_a,
        "ICHIMOKU_B": ta.trend.ichimoku_b,
        "ICHIMOKU_BASE_LINE": ta.trend.ichimoku_base_line,
        "ICHIMOKU_CONVERSION_LINE": ta.trend.ichimoku_conversion_line,
        "MASS_INDEX": ta.trend.mass_index,
    }
    indicators_aroon = {
        # aroon
        "AROON_DOWN": ta.trend.aroon_down,
        "AROON_INDICATOR": ta.trend.AroonIndicator(close_r).aroon_indicator,
        "AROON_UP": ta.trend.aroon_up,
    }

    indicators_ema = {
        f"EMA_INDICATOR_{i:03}": ta.trend.ema_indicator for i in windows
    }
    indicators_sma = {
        f"SMA_INDICATOR_{i:03}": ta.trend.ema_indicator for i in windows
    }

    for name, indicator in indicators_c.items():
        print(name)
        df[name] = indicator(close_r)

    for name, indicator in indicators_v.items():
        print(name)
        df[name] = indicator(volume_r)

    for name, indicator in indicators_hlc.items():
        print(name)
        df[name] = indicator(high_r, low_r, close_r, fillna=True)

    for name, indicator in indicators_hlv.items():
        print(name)
        df[name] = indicator(high_r, low_r, volume_r)

    for name, indicator in indicators_hlcv.items():
        print(name)
        df[name] = indicator(high_r, low_r, close_r, volume_r)

    for name, indicator in indicators_cv.items():
        print(name)
        df[name] = indicator(close_r, volume_r)

    for name, indicator in indicators_hl.items():
        print(name)
        df[name] = indicator(high_r, low_r)

    for name, indicator in indicators_aroon.items():
        print(name)
        if name == "AROON_INDICATOR":
            df[name] = indicator()
        else:
            df[name] = indicator(close_r)

    for name, indicator in indicators_ema.items():
        print(name)
        for window in windows:
            if f"{window:03}" in name:
                df[name] = indicator(close_r, window=window)
                break

    for name, indicator in indicators_sma.items():
        print(name)
        for window in windows:
            if f"{window:03}" in name:
                df[name] = indicator(close_r, window=window)
                break

    date_time = pd.to_datetime(
        df.pop("DateTime"), format=data_settings.date_time_format)
    timestamps = date_time.map(pd.Timestamp.timestamp)
    # TODO, it is slow use concat or some other shit
    day = 24  # hours
    year = (365.2425)*day

    day_sin = pd.Series(np.sin(timestamps * (2 * np.pi / day)))
    day_sin.name = "Day_sin"
    day_cos = pd.Series(np.cos(timestamps * (2 * np.pi / day)))
    day_cos.name = "Day_cos"
    one_year_sin = pd.Series(np.sin(timestamps * (2 * np.pi / year)))
    one_year_sin.name = "One_Year_sin"
    one_year_cos = pd.Series(np.cos(timestamps * (2 * np.pi / year)))
    one_year_cos.name = "One_Year_cos"
    two_year_sin = pd.Series(np.sin(timestamps * (2 * np.pi / (year*2))))
    two_year_sin.name = "Two_Year_sin"
    two_year_cos = pd.Series(np.cos(timestamps * (2 * np.pi / (year*2))))
    two_year_cos.name = "Two_Year_cos"
    three_year_sin = pd.Series(np.sin(timestamps * (2 * np.pi / (year*3))))
    three_year_sin.name = "Three_Year_sin"
    three_year_cos = pd.Series(np.cos(timestamps * (2 * np.pi / (year*3))))
    three_year_cos.name = "Three_Year_cos"
    four_year_sin = pd.Series(np.sin(timestamps * (2 * np.pi / (year*4))))
    four_year_sin.name = "Four_Year_sin"
    four_year_cos = pd.Series(np.cos(timestamps * (2 * np.pi / (year*4))))
    four_year_cos.name = "Four_Year_cos"
    five_year_sin = pd.Series(np.sin(timestamps * (2 * np.pi / (year*5))))
    five_year_sin.name = "Five_Year_sin"
    five_year_cos = pd.Series(np.cos(timestamps * (2 * np.pi / (year*5))))
    five_year_cos.name = "Five_Year_cos"

    df = pd.concat([df,
                    day_sin,
                    day_cos,
                    one_year_sin,
                    one_year_cos,
                    two_year_sin,
                    two_year_cos,
                    three_year_sin,
                    three_year_cos,
                    four_year_sin,
                    four_year_cos,
                    five_year_sin,
                    five_year_cos,
                    ], axis="columns")
    df["DateTime"] = date_time

    data_indicator_path = csv_path+"/with_indicator/" + data_name + ".csv"
    df.to_csv(data_indicator_path, index=False)


if __name__ == "__main__":
    pass
