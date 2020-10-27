import pandas as pd
from textblob import TextBlob
import nltk
from nltk.corpus import words
import re

# %% Read data

df = pd.read_csv("cte_news_articles_RAW.csv")
df["date"] = pd.to_datetime(df["date"])

# %% Preprocess data. Remove junk from text

# Remove URLs, emails

df["body"] = df["body"].apply(lambda x: re.sub(r'http\S+'," ", x))

print("Removed URLs")

df["body"] = df["body"].apply(lambda x: re.sub('\S*@\S*\s?'," ", x))

print("Removed emails")

# Remove bad punctuations (allow ,!?')

df["body"] = df["body"].apply(lambda x: re.sub("[^A-Za-z0-9!?,']+"," ", x))

print("Removed Bad chars")

# Remove garbage words
words = set(words.words())

def text_filter(my_text):
    return " ".join(w for w in nltk.wordpunct_tokenize(my_text) if w.lower() in words or not w.isalpha())

df["body"] = df["body"].apply(text_filter)

print("Removed garbage words")

# Remove empty rows
empty_rows = [i for i in range(len(df)) if len(df.iloc[i,2])==0]
df.drop(empty_rows, inplace=True)
df.reset_index(drop=True,inplace=True)

print("Removed empty rows")

# Export cleaned data
df.to_csv("cte_news_articles_CLEANED.csv",index=False)

# %% Function to return sentiment type

positive_threshold = 0.1
negative_threshold = -0.1

def get_senti_type(senti_score):
    if senti_score >= positive_threshold:
        return 1
    elif senti_score<=positive_threshold:
        return -1
    else:
        return 0
    
# %% Perform Sentiment analysis

df["senti_score"] = [TextBlob(text).sentiment.polarity for text in df["body"]]
df["senti_type"] = [get_senti_type(text) for text in df["senti_score"]]

df["positive"] = df["senti_type"]==1
df["negative"] = df["senti_type"]==-1
#df["neutral"] = df["senti_type"]==0

df = df.drop(columns = ["senti_type"])
df["count"] = [1 for _ in range(len(df))]
df = df.set_index(df["date"])

print("Sentiment done")

# %% Group by month

sentiment_by_month = df.iloc[:,[1,3,4,5,6]].groupby(pd.Grouper(freq="M"))
sentiment_by_month = sentiment_by_month.sum()
sentiment_by_month['Month'] = [str(date.year)+"-"+str(date.month) for date in sentiment_by_month.index]
sentiment_by_month['mean_senti_score'] = sentiment_by_month['senti_score']/sentiment_by_month['count']

cols = list(sentiment_by_month.columns)
sentiment_by_month = sentiment_by_month[[cols[-2]]+[cols[0]]+[cols[-1]]+cols[1:4]]

print("Grouping done")

# %% Export analysis
sentiment_by_month.to_csv('cte_news_senti_by_month.csv',index = False)
    
