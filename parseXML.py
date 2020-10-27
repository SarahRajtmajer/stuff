# Import libraries

import pandas as pd 
import xml.etree.ElementTree as et 
    
# %% Parse XML

xtree = et.parse("pubmed_result.xml")
xroot = xtree.getroot() 

# %% Get date and text
    
i=0
my_text=[]
my_dates=[]
missing_ids=[]

for node in xroot:
    text=""
    date=""
    
    try:
        for AbstractText in node.iter("AbstractText"):
            text+=AbstractText.text+" "
            
        my_text.append(text)
        
    except:
        my_text.append('')
    
    for PubDate in node.iter("PubDate"):
        try:
            my_dates.append(PubDate.find("Year").text+"-"+PubDate.find("Month").text)
        except:
            my_dates.append(None)        

    if my_dates[i] is None:
        for ArticleDate in node.iter("ArticleDate"):
            try:
                my_dates[i]= ArticleDate.find("Year").text+"-"+ArticleDate.find("Month").text
            except:
                pass
 
    if my_dates[i] is None:
        for DateRevised in node.iter("DateRevised"):
            
            try:
                my_dates[i]= DateRevised.find("Year").text+"-"+DateRevised.find("Month").text
            except:
                pass
    
    if my_dates[i] is None:
        my_dates[i] = my_dates[i-1]
        
    i+=1


# %% Create dataframe

df = pd.DataFrame(data={"created_on":my_dates , "text":my_text})

df["created_on"] = pd.to_datetime(df["created_on"])

# %% Export to csv

df.to_csv("pubmed_abstracts.csv",index=False)
