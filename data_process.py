# local
from settings.settings import data_settings
from data.clean_data import clean_data
from data.indicators import indicators
from data.classification import target
from data.preprocess import preprocess


def main(data_name) -> None:

    clean_data.clean_data(data_name)
    indicators.add_indicators(data_name)
    target.add_targets(data_name)
    # preprocess.preprocess(data_name)


if __name__ == "__main__":

    # csv_s = [
    #     "EURUSD_H1_201701020000_202206241400",
    #     "EURUSD_H1_201801020000_202206210600",
    #     "EURUSD_H1_201901020600_202206241500",
    #     "EURUSD_M15_201701020000_202206241445",
    #     "EURUSD_M15_201801020000_202206211100",
    #     "EURUSD_M15_201901020600_202206241500"
    # ]
    # for csv in csv_s:
    #     main(csv)

    main(data_settings.data_name)
