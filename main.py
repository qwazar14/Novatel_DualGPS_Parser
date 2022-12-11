import datetime
import sys
import time

import pandas
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from matplotlib import ticker


class DataParser:
    def __init__(self, filename="6.csv"):
        self.filename = filename
        self.data = self.read_data_csv()

    def read_data_csv(self):
        try:
            df = pandas.read_csv(self.filename, header=None)
            return df
        except FileNotFoundError:
            print(f"ERROR: File {self.filename} not found. Exit...")
            sys.exit(-1)

    def get_data_from_column(self, column: int):
        data = self.data
        data_list = []
        for row in range(0, len(data.values)):
            data_list.append(float(data.values[row][column]))
        return np.array(data_list)


def visualise(time_array, head_array, pitch_array, divider=0):
    plt.rcParams["figure.dpi"] = 800
    plt.rcParams["font.size"] = 5

    def display_time(seconds):
        return time.strftime("%H:%M:%S", time.gmtime(seconds))

    def convert_seconds(array):
        time_list = []
        for sec in array:
            time_list.append(display_time(sec))
        return np.array(time_list)

    def split_array(array, n):
        return np.split(array, np.arange(n, len(array), n))

    def find_average(array):
        return [np.mean(arr) for arr in array]

    if divider != 0:
        timestamp_array = convert_seconds(
            find_average(split_array(time_array, divider))
        )
        head_array = find_average(split_array(head_array, divider))
        pitch_array = find_average(split_array(pitch_array, divider))
    else:
        timestamp_array = convert_seconds(time_array)

    try:
        _, axis = plt.subplots(2)
        axis[0].plot(timestamp_array, head_array, linewidth=0.3)
        axis[0].set_title("head/time")

        axis[1].plot(timestamp_array, pitch_array, "tab:red", linewidth=0.3)
        axis[1].set_title("pitch/time")

        axis[0].tick_params(labelrotation=45)
        axis[1].tick_params(labelrotation=45)
        # axis[1].tick_params(labelrotation=45)

        plt.tight_layout()

        plt.show()
    except ValueError:
        print(
            f"ERROR: log file has only {len(time_array)} seconds. You typed {divider}"
        )


def run(divider=100, filename="6.csv"):
    dp = DataParser(filename)

    time_array = dp.get_data_from_column(6)
    head_array = dp.get_data_from_column(12)
    pitch_array = dp.get_data_from_column(13)

    print("Average head: ", round(np.average(head_array), 3))
    print("Average pitch: ", round(np.average(pitch_array), 3))

    std_head = np.std(head_array)
    std_pitch = np.std(pitch_array)

    print("Std head: ", std_head)
    print("Std pitch: ", std_pitch)

    print("Std max head: ", std_head.max())
    print("Std max pitch: ", std_pitch.max())

    visualise(time_array, head_array, pitch_array, divider)


if __name__ == "__main__":
    start_time = time.time()
    run(0)
    print("--- %s seconds ---" % (time.time() - start_time))
