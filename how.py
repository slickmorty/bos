
from backtesting import Strategy
import matplotlib.pyplot as plt
import numpy as np

steps: dict = {
    "XGBOOST": {

        "Model": [
            # "Make model more complex, depth max is 6 by default",
            # "All paraeters should be included when constructing a model",
        ],
    },
    "BackTesting": {

        "Reminders": [
            "Remember to backtest while training the model"
        ],
    },
}

# TODO: make new data with sl_to_tp=6 #TODO fuck off i did it with 5
# TODO: Change tp to sl to 1, 1.25, 1.5, 1.75 , 2 , 4 if things didn't work
# TODO: make df columns relate to each other #TODO nvm its to fucking expensive
# TODO: make important columns relative to each other
# TODO:
