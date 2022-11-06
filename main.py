import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import re
from config import *
#import os

# check if it conatins key words
# put in seperate dataframe
# add all cost
# repeat
# plot

# remove if found off list!
# DataFrame.fillna() ! replace nan no need for try except
# check how .loc() works in detail and iloc()

#TODO
# input what you want / weekly / monthly etc
# input what type of graph
# suggest improvements
# show increase / decrease
# save all fiels in specified locations + noremal excel files up

# open files
#path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.txt")

#with open(path) as f:
#    contents = f.read()
#print(contents)
#print(type(eval(contents)))

# variables/constants


plt.rcParams.update({'font.size': FONT})

# functions TOO SMALL wont work
def create_graphs(graph, data):
    start = 0
    for i in range(len(data["group"])):
        group, costs = list(data["cost"][i].keys()), list(data["cost"][i].values())
        graph.subplot(3, 2, (i+1))
        print(group, costs)
        graph.bar(group, costs)
        graph.xlabel("Groups")
        graph.ylabel("Cost")
        graph.title("Tax")
    graph.show()
    
def flip_date(date):
    date = date.split("/")
    date.reverse()
    date = "/".join(date)
    return date

def get_months(df): # if wanted?
    months = []
    # months inbetween
    m = START_DATE.split("/")
    for i in range(1, 13):
        m[1] = str(i).zfill(2)
        m1 = "/".join(m)
        months.append(m1)
    
    #create dataframes for each month
    df_months = []
    #print(df["date"])
    #print(months)
    for i in range(1, 12):
        mask = (df['date'] >= months[i-1]) & (df['date'] < months[i]) # ranges FALSE TRUES
        #print(mask.to_string())
        #print( months[i-1],  months[i])
        #print(mask.to_string())
        df_months.append(df.loc[mask]) # between ranges
    return df_months

def group_func(series, costs, keywords): # return total cost
    total = dict.fromkeys(keywords, 0)
    total_sum = 0
    for i in range(len(series)):
        cost = costs[i]
        sentance = series[i]
        if not isinstance(sentance,bool) and not isinstance(cost, bool):
            flag = True
            sentance = list(filter(None, re.split(r"\s|\.", sentance)))
            #print(sentance)
            # print(f"sentance {sentance} cost {type(cost)} cost {cost}")
            #print(f"sentance {list(sentance)} keyword {keywords}")
            # print(list(sentance), keywords)
            for word in sentance:
                if word.lower() in keywords:
                    total_sum += float(cost[1:])
                    total[word.lower()] += float(cost[1:])
                    break
    return total, total_sum

# SETUP EXCEL
df = pd.read_csv('Bank statement.csv') # read file return DataFrame
df = df.fillna(False)
pd.set_option('display.max_columns', 50) # max value
df = df.iloc[OFFSET:-1] # gets rid of first 4 rows
# rid of useless collums
del df["Unnamed: 0"]
del df["Unnamed: 2"]
del df["Unnamed: 3"]
del df["Unnamed: 4"]
del df["Unnamed: 6"]
del df["Unnamed: 8"]
# rename collums
df.rename(columns = {"Transactions":"date", "Unnamed: 5":"details", "Unnamed: 7":"cash in", "Unnamed: 9":"cash out"}, inplace = True)
# change index from 0
df.index = pd.RangeIndex(start=0, stop=(df.shape[0]), step = 1)
df["date"] = df["date"].apply(flip_date)
#print(df.to_string())
# VERY USEFULL df_m = get_months(df)
df_m = df
des = df_m["details"]
cost = df_m["cash out"]

#ANALYSIS
chart = {}
chart2 = {"group": [], "cost":[]}
# clubs
total, total_sum = group_func(des, cost, clubs)
chart["clubs"] = (total)
chart2["group"].append("clubs")
chart2["cost"].append(total_sum)
# deliveries
total, total_sum  = group_func(des, cost, deliveries)
chart["deliveries"] = (total)
chart2["group"].append("deliveries")
chart2["cost"].append(total_sum)
# travel
total, total_sum  = group_func(des, cost, travel)
chart["travel"] = (total)
chart2["group"].append("travel")
chart2["cost"].append(total_sum)
# stores
total, total_sum  = group_func(des, cost, stores)
chart["stores"] = (total)
chart2["group"].append("stores")
chart2["cost"].append(total_sum)
# restaurants
total, total_sum  = group_func(des, cost, restaurants)
chart["restaurants"] = (total)
chart2["group"].append("restaurants")
chart2["cost"].append(total_sum)
# commodities
total, total_sum  = group_func(des, cost, commodities)
chart["commodities"] = (total)
chart2["group"].append("commodities")
chart2["cost"].append(total_sum)
# creates plots
while True:
    ans = input("specific group or all groups? group / all groups")
    if ans == "all groups":
        plt.bar(chart2["group"], chart2["cost"])
        break
    elif ans == "group":
        ans = input("what group?")
        keys = chart[ans].keys()
        values = chart[ans].values()
        plt.bar(keys, values)
        break
    
plt.xlabel("Groups")
plt.ylabel("Cost")
plt.title("Bank ")
plt.show()
    
