import datetime

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from legacy.email import send

plt.style.use('_mpl-gallery')


def main():
    spy = yf.Ticker('SPY')
    data = cvtDF(spy.history('5d', '1d'))

    xAxis = getXList(data)

    y1 = np.array(getYList(data, 'High'))
    y2 = np.array(getYList(data, 'Low'))

    fig, ax = plt.subplots()

    ax.fill_between(xAxis, y1, y2, alpha=.5, linewidth=0.5)
    ax.plot(xAxis, (y1 + y2)/2, linewidth=2)

    plt.show()


def cvtDF(data: pd.DataFrame) -> list:
    outList = []

    data = data.to_dict()

    for i in range(len(data['Close'])):
        tmp = {'ts': list(data['Open'])[i].to_pydatetime(),
               'Open': data['Open'][list(data['Open'])[i]],
               'Close': data['Close'][list(data['Close'])[i]],
               'High': data['High'][list(data['High'])[i]],
               'Low': data['Low'][list(data['Low'])[i]]
               }

        outList.append(tmp)

    return outList


def getXList(data: list) -> list:
    values = []

    for d in data:
        openTime = d['ts'] + datetime.timedelta(hours=8)
        midDay = openTime + datetime.timedelta(hours=4)
        closeTime = midDay + datetime.timedelta(hours=4)

        values.append(openTime)
        values.append(midDay)
        values.append(closeTime)

    return values


def getYList(data: list, highOrLow: str) -> list:
    values = []

    for d in data:
        openValue = d['Open']
        midValue = d[highOrLow]
        closeValue = d['Close']

        values.append(openValue)
        values.append(midValue)
        values.append(closeValue)

    return values


def test():

    def plot_line_with_slope_color(x, y):
        # Calculate the slope
        slope = (y[-1] - y[0]) / (x[-1] - x[0])

        # Determine the color based on the slope
        line_color = 'green' if slope > 0 else 'red'

        # Plot the line
        plt.plot(x, y, color=line_color, label=f'Slope: {slope:.2f}')

        # Add labels and legend
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.legend()

    # Example data
    x_values = np.linspace(0, 10, 100)
    y_values_pos = 2 * x_values + 5  # Positive slope
    y_values_neg = -2 * x_values + 5  # Negative slope

    # Plot lines with different slopes and colors
    plt.figure(figsize=(8, 6))
    plot_line_with_slope_color(x_values, y_values_pos)
    plot_line_with_slope_color(x_values, y_values_neg)

    # Show the plot
    plt.title('Lines with Positive and Negative Slopes')
    plt.show()


if __name__ == '__main__':
    test()
