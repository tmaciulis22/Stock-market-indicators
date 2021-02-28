import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import constants


def load_data(path):
    df = pd.read_csv(path)
    df[constants.DATETIME_COLUMN] = df[constants.DATE_COLUMN] + " " + df[constants.TIME_COLUMN]
    df[constants.DATETIME_COLUMN] = pd.to_datetime(df[constants.DATETIME_COLUMN], format=constants.DATETIME_FORMAT)
    df[constants.TIME_COLUMN] = pd.to_datetime(df[constants.TIME_COLUMN], format=constants.TIME_FORMAT)
    df[constants.DATE_COLUMN] = pd.to_datetime(df[constants.DATE_COLUMN], format=constants.DATE_FORMAT)

    return df


def create_subplots():
    return plt.subplots(nrows=3, constrained_layout=True)


def plot_data(
    axis,
    x_values,
    y_values,
    title=None,
    x_label=None,
    y_label=None,
    y_line=None,
    x_lim=None,
    toggle_grid=True,
    color=None,
    label=None
):
    axis.set_title(title)
    if toggle_grid:
        axis.grid()
    if x_label is not None:
        axis.set_xlabel(x_label)
    if y_label is not None:
        axis.set_ylabel(y_label)
    if x_lim is not None:
        axis.set_xlim(x_lim)
    axis.plot(x_values, y_values, color=color, label=label)
    if y_line is not None:
        axis.axhline(y=y_line, linewidth=3, color="y")


def plot_data_single(x_values, y_values, title=None, x_label=None, y_label=None, y_line=None, toggle_grid=True):
    plt.title(title)
    if toggle_grid:
        plt.grid()
    if x_label is not None:
        plt.xlabel(x_label)
    if y_label is not None:
        plt.ylabel(y_label)
    plt.plot(x_values, y_values)
    if y_line is not None:
        plt.axhline(y=y_line, linewidth=3, color="y")


def calculate_chaikin_volatility(df):
    high_low_diff = np.subtract(df[constants.HIGH_COLUMN], df[constants.LOW_COLUMN])

    averages = np.round(high_low_diff.ewm(
        alpha=constants.CHAIKIN_ALPHA,
        adjust=True
    ).mean(), 2)
    previous_avg = averages[constants.CHAIKIN_PERIOD:-constants.CHAIKIN_PERIOD].reset_index(drop=True)
    current_avg = averages[constants.CHAIKIN_PERIOD * 2:].reset_index(drop=True)

    diff_of_avg = np.subtract(current_avg, previous_avg)
    division = np.divide(diff_of_avg, previous_avg)

    return np.round(np.multiply(division, [100]), 2)


def calculate_vol_rate_of_change(df):
    current_vol = np.add(
        df[constants.VOL_PERIOD:][constants.UP_COLUMN],
        df[constants.VOL_PERIOD:][constants.DOWN_COLUMN]
    ).reset_index(drop=True)
    previous_vol = np.add(
        df[0:-constants.VOL_PERIOD][constants.UP_COLUMN],
        df[0:-constants.VOL_PERIOD][constants.DOWN_COLUMN]
    )

    diff_of_vols = np.subtract(current_vol, previous_vol)
    div_of_vols = np.divide(diff_of_vols, previous_vol)

    return np.round(np.multiply(div_of_vols, [100]), 2)


def calculate_bollinger_band(df):
    moving_avg = np.round(df[constants.CLOSE_COLUMN].rolling(window=constants.BOLLINGER_PERIOD).mean(), 2)

    std = np.round(df[constants.CLOSE_COLUMN].rolling(window=constants.BOLLINGER_PERIOD).std(), 2)
    multiplied_std = np.multiply(std, constants.BOLLINGER_MULTIPLIER)

    upper_band = np.round(np.add(moving_avg, multiplied_std), 2)
    lower_band = np.round(np.subtract(moving_avg, multiplied_std), 2)

    return upper_band, moving_avg, lower_band
