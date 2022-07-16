# local
from settings.settings import data_settings
from data.clean_data import clean_data
from data.indicators import indicators
from data.classification import target
from data.preprocess import preprocess


def main(data_name) -> None:

    # clean_data.clean_data(data_name)
    indicators.add_indicators(data_name)
    # target.add_targets(data_name)
    # preprocess.preprocess(data_name)


if __name__ == "__main__":

    main(data_settings.data_name)
