import util
import constants

figure, axes = util.create_subplots()
figure.suptitle(constants.MSFT_FIGURE_TITLE, fontsize=18)

df = util.load_data(constants.MSFT_DATA_PATH)

util.plot_data(
    axes[0],
    df[constants.DATETIME_COLUMN],
    df[constants.CLOSE_COLUMN],
    title="Price (USD)",
)

chaikin_volatility = util.calculate_chaikin_volatility(df)
util.plot_data(
    axes[1],
    df[constants.DATETIME_COLUMN][constants.CHAIKIN_PERIOD * 2:],
    chaikin_volatility,
    title="Chaikin Volatility",
    y_line=0,
    x_lim=axes[0].get_xlim()
)

vol_rate_of_change = util.calculate_vol_rate_of_change(df)
util.plot_data(
    axes[2],
    df[constants.DATETIME_COLUMN][constants.VOL_PERIOD:],
    vol_rate_of_change,
    title="Volume Rate of Chg",
    y_line=0,
    x_lim=axes[0].get_xlim()
)

upper_band, middle_band, lower_band = util.calculate_bollinger_band(df)
util.plot_data(
    axes[0],
    df[constants.DATETIME_COLUMN],
    upper_band,
    toggle_grid=False,
    color="green",
    label="Upper Bollinger Band"
)
util.plot_data(
    axes[0],
    df[constants.DATETIME_COLUMN],
    lower_band,
    toggle_grid=False,
    color="red",
    label="Lower Bollinger Band"
)
util.plot_data(
    axes[0],
    df[constants.DATETIME_COLUMN],
    middle_band,
    toggle_grid=False,
    color="black",
    label="Middle Bollinger Band"
)
axes[0].fill_between(df[constants.DATETIME_COLUMN], upper_band, lower_band, color="paleturquoise")
axes[0].legend(loc="upper right")
