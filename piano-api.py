import requests, json 
import pandas as pd
from pandas import json_normalize
from config import AID, API_TOKEN 

# read, sort and merge csv files
def merge_csv(csvA,csvB):
    dfA = pd.read_csv(csvA)
    dfB = pd.read_csv(csvB)
    dfA.sort_values(by=['user_id'], inplace=True)
    dfB.sort_values(by=['user_id'], inplace=True)
    df = pd.merge(dfA, dfB)
    return df

# pick up actual team members and put them in a data frame
def team_members(aid, api_token):
    payload = {'aid' : AID, 'api_token' : API_TOKEN}
    api_url = "https://sandbox.piano.io/api/v3/publisher/team/list"
    response = requests.get(api_url, params=payload)
    json_response = response.json()
    team_members_df = json_normalize(json_response, 'team_members')
    return team_members_df

# check if users id are correct
def iter_df(df1,df2):
    for index, row in df1.iterrows():
        for index1, row1 in df2.iterrows():
            if (row['first_name'] == row1['first_name']) and (row['last_name'] == row1['last_name']) and (row['email'] == row1['email']):
                df1['user_id'][index] = df2['uid'][index1]
    return df1
            

if __name__ == '__main__':
    df = merge_csv('fa.csv', 'fb.csv')
    team_members_df = team_members(AID, API_TOKEN)
    iter_df(df,team_members_df)
    # convert dataframe to csv
    df.to_csv("checked_users.csv", index=False)
    
