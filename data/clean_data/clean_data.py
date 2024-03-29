import pandas as pd
from settings.settings import data_settings


def clean_data(data_name: str):

    csv_path = data_settings.csv_path
    data_path = csv_path + "/mt_data/" + data_name + ".csv"
    cleaed_data_path = csv_path + "/cleaned_mt_data/" + data_name + ".csv"

    with open(cleaed_data_path, "w") as f:
        f.write("")

    with open(data_path, "r") as f:

        for _, value in enumerate(f):
            with open(cleaed_data_path, "a") as f2:
                a = value.split("\t")
                f2.write(f"{a}\n"
                         .replace("[", "")
                         .replace("]", "")
                         .replace("\\n", "")
                         .replace("\"", "")
                         .replace("\'", "")
                         .replace(" ", "")
                         .replace("<", "")
                         .replace(">", ""))

    df = pd.read_csv(cleaed_data_path)
    date = df.pop("DATE")
    time = df.pop("TIME")
    df.drop("VOL", axis="columns", inplace=True)

    df["DateTime"] = date+" "+time

    columns = ["Open", "High", "Low", "Close", "TickVol", "Spread", "DateTime"]
    df.columns = columns

    columns = ["DateTime", "Open", "High", "Low", "Close", "TickVol", "Spread"]
    df = df[columns]

    df.to_csv(cleaed_data_path, index=False)


if __name__ == "__main__":

    pass
