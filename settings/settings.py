import json


class Settings:
    def __init__(self, settings_path: str) -> None:

        self.settings_path = settings_path

        with open(self.settings_path, "r") as f:
            self.data: dict = json.load(f)

        for key, value in self.data.items():
            setattr(self, key, value)


data_settings = Settings("./settings/data_settings.json")
model_settings = Settings("./settings/model_settings.json")
