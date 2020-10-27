import pandas as pd
import glob
import re

filenames = glob.glob("CTE News articles/*.txt")
months = {'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12}

df = pd.DataFrame(data={"filename":filenames,"date":filenames, "body":filenames})

for i,filename in enumerate(filenames):
    file = open(filename,'r',encoding='utf-8')
    body=""
    date=""
    timeout=0
    max_length=0

    while True:
        line = file.readline()

        if line=="ENDFILE\n" or timeout>20:
            break
        
        if line and line[0]=='[':
            date_to_list = line.strip().replace(" ","").replace("'","").replace("[","").replace("]","").split(",")
            
            if date_to_list[0] in months.keys():
                for j in range(1,len(date_to_list)): 
                    date_to_list[j] = re.sub('\D', '', date_to_list[j])
                
                date="/".join([str(months[date_to_list[0]])] + date_to_list[1:])
                    
                
        if len(line)>max_length:
            max_length=len(line)
            body=line[:-1]
            
    df.date[i]=date
    df.body[i]=body
    
    if i%1000==0:
        print(i,'/',len(filenames))

    file.close()

# Remove duplicate values
#df.drop_duplicates(subset='body', keep='first', inplace=True)
#df.reset_index(drop=True,inplace=True)

# Remove outliers
irregular = sorted(df.index,reverse=True,key=lambda x: len(df.iloc[x,2]))
df.drop(irregular[:50], inplace=True)
df.reset_index(drop=True,inplace=True)

# Export to csv
df.to_csv("cte_news_articles_RAW.csv",index=False)

# %% debug
'''
a = [len(x) for x in df.body]

irregular = sorted(a,reverse=True)

for i in range(len(df)):
    if len(df.iloc[i,2]) in irregular[:10]:
        print(df.iloc[i,0])

# import matplotlib.pyplot as plt


plt.plot(irregular[:1000])
'''
