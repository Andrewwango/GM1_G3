import csv
import numpy as np
from scipy.signal import find_peaks

def saveline(c, arr):
    result_book.append([c] + list(arr))

with open("ml_training/temp4.csv", mode="r", newline='') as f:
    csvreader = csv.reader(f, delimiter=',')
    series = np.array([row[0] for row in csvreader])[1:]

peaks,_ =  find_peaks(series, prominence=10)
result_book = []

for peak in peaks:
    saveline(2, series[peak-10:peak+10])

with open("ml_training/training_data2.csv", mode="a", newline='') as f:
    csvwriter = csv.writer(f, delimiter=',')
    for row in result_book:
        csvwriter.writerow(row)