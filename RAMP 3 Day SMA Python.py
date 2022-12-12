# Read Text Files with Pandas using read_csv()
  

# importing the modules
from IPython.display import display
import pandas as pd
import matplotlib.pyplot as plt


# read text file into pandas DataFrame
df = pd.read_csv('transactions.txt', sep=" ", names=["transaction_dates", "transaction_hours", "transaction_amount"])

# clean up any special characters besides a-z A-Z 0-9 and decimal point
# convert date to datetime, convert amount to float
df['transaction_dates'] = df['transaction_dates'].str.replace('[^a-zA-Z0-9]',"", regex = True)
df['transaction_dates'] = pd.to_datetime(df['transaction_dates'])
df['transaction_amount'] = df['transaction_amount'].str.replace('[^a-zA-Z0-9.]',"", regex = True).astype(float)

# sort by transaction_dates
df2 = df.sort_values(by="transaction_dates", ascending=True)

# clean out the unnecessary hours column
del df2["transaction_hours"]

# group by daily
df3 = df2.groupby(["transaction_dates"]).sum()

# saving only the transaction_amount for 3 day sma calculation
# using .to_frame() to convert df3["transaction_amount"] pandas series into dataframe
df4 = df3["transaction_amount"].to_frame()

# calculating 3 day sma with .rolling(window_size=3).mean()
df4["3_day_sma"] = df4["transaction_amount"].rolling(3).mean()

# clean up any NA or NULL values
df4.dropna(inplace=True)

display(df4)

# plot the transaction amount vs 3 day sma using .plot() method
df4[["transaction_amount","3_day_sma"]].plot(label = "transactions", figsize=(16,8))

plt.show()