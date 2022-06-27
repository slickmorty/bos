import ta
import pandas as pd
from settings.settings import data_settings


def add_indicators(data_name: str):

    csv_path = data_settings.csv_path
    cleaed_data_path = csv_path + "/cleaned_mt_data/" + data_name + ".csv"

    df = pd.read_csv(cleaed_data_path)

    high_r = df["High"]
    low_r = df["Low"]
    close_r = df["Close"]
    volume_r = df["TickVol"]

    shorts = (8, 12, 24)
    longs = (48, 96, 192)

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
        # "PSAR_DOWN": ta.trend.psar_down,
        "PSAR_DOWN_INDICATOR": ta.trend.psar_down_indicator,
        # "PSAR_UP": ta.trend.psar_up,
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
        # "ACC_DIST_INDEX": ta.volume.acc_dist_index,
        "CHAIKIN_MONEY_FLOW": ta.volume.chaikin_money_flow,
        "MONEY_FLOW_INDEX": ta.volume.money_flow_index,
        "VOLUME_WEIGHTED_AVERAGE_PRICE": ta.volume.volume_weighted_average_price,
    }
    indicators_cv = {
        # close_r,df["TickVol"]
        # "FORCE_INDEX": ta.volume.force_index,
        "NEGATIVE_VOLUME_INDEX": ta.volume.negative_volume_index,
        # "ON_BALANCE_VOLUME": ta.volume.on_balance_volume,
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
    indicators_ma = {
        "EMA_INDICATOR_8": ta.trend.ema_indicator,
        "EMA_INDICATOR_12": ta.trend.ema_indicator,
        "EMA_INDICATOR_24": ta.trend.ema_indicator,
        "EMA_INDICATOR_48": ta.trend.ema_indicator,
        "EMA_INDICATOR_96": ta.trend.ema_indicator,
        "EMA_INDICATOR_192": ta.trend.ema_indicator,

        "SMA_INDICATOR_8": ta.trend.sma_indicator,
        "SMA_INDICATOR_12": ta.trend.sma_indicator,
        "SMA_INDICATOR_24": ta.trend.sma_indicator,
        "SMA_INDICATOR_48": ta.trend.sma_indicator,
        "SMA_INDICATOR_96": ta.trend.sma_indicator,
        "SMA_INDICATOR_192": ta.trend.sma_indicator,

    }

    for name, indicator in indicators_c.items():
        print(name)
        df[name] = indicator(close_r)

    for name, indicator in indicators_v.items():
        print(name)
        df[name] = indicator(volume_r)

    for name, indicator in indicators_hlc.items():
        print(name)
        df[name] = indicator(high_r, low_r, close_r)

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

    for name, indicator in indicators_ma.items():
        print(name)
        for _short in shorts:
            if f"{_short}" in name:
                df[name] = indicator(close_r, window=_short)
                break

        for _long in longs:
            if f"{_long}" in name:
                df[name] = indicator(close_r, window=_long)
                break

    data_indicator_path = csv_path+"/with_indicator/" + data_name + ".csv"
    df.to_csv(data_indicator_path, index=False)


if __name__ == "__main__":
    pass
