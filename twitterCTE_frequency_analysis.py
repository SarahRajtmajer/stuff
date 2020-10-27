import pandas as pd

# %% Read data

df = pd.read_csv("twitterCTE_complete_data_Oct-2009_to_Dec-2020.csv")
df["created_on"] = pd.to_datetime(df["created_on"])
df = df.set_index(df["created_on"])

# %% count

df["count"] = [1 for _ in range(len(df))]

# %%  Group counts, retweets, replies and quotes

df_freq = df.loc[:,["count","retweet_count","reply_count","quote_count"]].groupby(pd.Grouper(freq="M"))
df_freq = df_freq.sum()
df_freq['Month'] = [str(date.year)+"-"+str(date.month) for date in df_freq.index]

cols = list(df_freq.columns)
df_freq = df_freq[[cols[-1]]+cols[:-1]]

# %% Export

df_freq.to_csv("twitterCTE_freq_by_month.csv", index=False)