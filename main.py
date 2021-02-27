import util
import constants

figure, axes = util.create_subplots()
figure.suptitle("AAPL - 1 min NASDAQ", fontsize=18)

df = util.load_data(constants.APPL_DATA_PATH)
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
    toggle_grid=False
)
util.plot_data(
    axes[0],
    df[constants.DATETIME_COLUMN],
    lower_band,
    toggle_grid=False
)
util.plot_data(
    axes[0],
    df[constants.DATETIME_COLUMN],
    middle_band,
    toggle_grid=False
)

#plot sales and 4-day exponentially weighted moving average
# plt.plot(df['sales'], label='Sales')
# plt.plot(df['4dayEWM'], label='4-day EWM')

#add legend to plot
# plt.legend(loc=2)