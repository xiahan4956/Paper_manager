import re
import pandas as pd
import requests
import os
import sys
sys.path.append(os.getcwd())

from utils.claude import ask_claude
from utils.gpt import ask_gpt

import dotenv
dotenv.load_dotenv()
MODEL = os.getenv("MODEL")


def add_meta_data(df,i):
    '''
    Add the doi,abstract,year,publisher to the paper by the title.
    '''
    while True:
        try:    
            res = requests.get(f"https://api.scite.ai/search?term={df.loc[i,'title']}")
            break
        except Exception as e:
            print("scite.ai search fail")
            print(e)

    res = res.json()["hits"][0]


    #  To ensure the accuracy of the match,cheak doi actually mapping title.
    idea = cheak_mapping_title(df, i, res)  
    try:
        if "False" in idea:
            return df
    except Exception as e:  
        print(e)
        print("claude return error")

     
    df.loc[i,"doi"] = res["doi"]
    df.loc[i,"journal"] = res["journal"]
    df.loc[i,"abstract"] = res["abstract"]
    df.loc[i,"publish_year"] = res["year"]
    df.loc[i,"publisher"] = res["publisher"]


    return df

def cheak_mapping_title(df, i, res):
    mapping_title = res["title"]
    pmt = '''
    Background:
    I am matching papers based on their titles.
    <title> is the original paper title.
    <mapping title> is the matched paper title.
    To ensure the accuracy of the match,please verify if they are the same paper.
    If the paper is the same,You return True,else return False.

    You should think in <think></think> xml tag first

    <title>
    {title}
    <title>
    
    <mapping title>
    {mapping_title}
    </mapping title>


    RETURN
    res: <bool>
    
    '''.format(title = df.loc[i,'title'],mapping_title = mapping_title)
    
    if "claude" in MODEL:
        idea = ask_claude(pmt)
    if "gpt" in MODEL:
        idea = ask_gpt(pmt)
    return idea



def add_citations(df:pd.DataFrame):
    '''Add the citations to the paper by the doi'''
    dois = df["doi"].astype("str").unique().tolist()

    d_list = []
    for i in range(0,len(dois),500):
        dois_500 = dois[i:i+500]
        while True:
            try:
                res = requests.post("https://api.scite.ai/tallies", json=dois_500)
                break
            except Exception as e:
                print("citation data match fail")
                print(e)
        res = res.json()["tallies"]
        
        for k,v in res.items():
            d_list.append({**v, "doi": k})

    df_meta = pd.DataFrame(d_list)
    df_meta = df_meta[["doi","total"]]
    df_meta.rename(columns={"total":"citations"},inplace=True)
    df = df.merge(df_meta, left_on="doi", right_on = "doi",how="left")

    return df



def add_if_factor(df_t,i):
    '''Add the if factor to the paper by the journal'''
    publication = str(df_t.loc[i,"journal"])
    print("publication:",publication)
    
    
    url= "https://www.easyscholar.cc/open/getPublicationRank?secretKey=40e361fdc5b843fe8db1c4850b13a19f&publicationName="    
    # get the if factor result    
    while  True:
        try:
            res = requests.get(url = url+publication,timeout=3).json()
            break
        except Exception as e:
            print(e)

    try:
        sci	 = res["data"]["officialRank"]["all"].get("sci","") 
        sciif = res["data"]["officialRank"]["all"].get("sciif","")
       
    except:
        sci = ""
        sciif = ""

    df_t.loc[i,"sci"] = sci
    df_t.loc[i,"sciif"] = sciif


    print("sci:",sci,"sciif:",sciif)

    return df_t

        

    
        
        

