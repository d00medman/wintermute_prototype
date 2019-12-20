from flask import Flask
from flask import request
import pandas as pd
import numpy as np
app = Flask(__name__)

# How to be reading from the kafka topic?
# Do I need an endpoint? Most barebones possible listener


if __name__ == "__main__":
    app.run()
