import argparse
import matplotlib.pyplot as plt
import pandas as pd

ap = argparse.ArgumentParser()

ap.add_argument("-i", "--input", required=True, help="path to input csv file")
args = vars(ap.parse_args())

with open(args["input"], 'r') as f:
    data = pd.read_csv(f)


data.plot(x="time", y="signal")
plt.show()


