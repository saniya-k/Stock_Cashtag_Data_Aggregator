import tweepy
import pandas as pd
import time
from datetime import date,timedelta
from pprint import pprint

def get_authorized(consumer_key,consumer_secret,access_token,access_token_secret):
    '''    
    This function helps to establish connection to twitter api via tweepy.
    
    Parameters:
    consumer_key : api key from twitter enter by user
    consumer_secret : api secret from twitter enter by user
    access_token : access token from twitter enter by user
    access_token_secret: access token secret from twitter enter by user
    
    Returns: 
    Tweepy api object which helps in connecting to twitter
    '''
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True) #waits on rate limit (15 mins)
    return api

def get_tweets(api,tag,num_tweets=10):
    '''
    This function gets tweets related to a cashtag made in the past two days.
    
    Parameters:
    api : tweepy api object which helps in connecting to twitter
    tag : cashtag
    num_tweets : Number of tweets to be scrapped. If this exceeds 300, the API will try to get all the tweets made in the past two days.
    
    Returns: 
    A list of tweets for the corresponding cashtag.
    '''
    today = date.today()
    text_query = tag 
    try:
        if num_tweets>300:
            tweets = tweepy.Cursor(api.search,q=text_query,since=today-timedelta(days=2), until=today).items()
        else:
            tweets = tweepy.Cursor(api.search,q=text_query,since=today-timedelta(days=2), until=today).items(num_tweets)
        # Pulling information from tweets iterable object
        tweets_list = [[tweet.created_at, tweet.id, tweet.text] for tweet in tweets]
        # Creation of dataframe from tweets list
        # Add or remove columns as you remove tweet information
        tweets_df = pd.DataFrame(tweets_list)
        tweets_df.rename(columns={0: 'Timestamp',1: 'Tweet ID',2:'Tweet'}, inplace=True)
        tweets_df.insert(0, 'Hashtag', tag)
    except tweepy.TweepError as te:
        print(te.reason)
        return None 
    return tweets_df

#get from twitter after creating dev account
f=open("authentication.txt","r")
lines=f.readlines()
api_key=lines[0].strip() 
api_secret_key=lines[1].strip() 
access_token=lines[2].strip() 
access_token_secret=lines[3].strip() 
api = get_authorized(api_key,api_secret_key,access_token,access_token_secret)
f.close()

#read file containing hashtag information
hashtags=pd.read_csv("FinalList_Tech.csv",header=0) #file location
related_tweets=pd.DataFrame()
hashtags.head()
retry_later={}
print("Getting data from twitter ...")
for lab,row in hashtags.iterrows():
    #function gets 10 tweets related to cashtag in the past week
    tweets_df=get_tweets(api,'$'+row[10],2000)
    if (tweets_df is None):
        print(f"Skipped {row[3]} due to exception, will retry later")
        retry_later[row[10]]=row[3]
        continue
    if not(tweets_df.empty) :
        tweets_df.insert(0, 'Company', row[3])
        related_tweets=related_tweets.append(tweets_df, ignore_index=True)
print("Done... ")
if retry_later:
    print(f' Some of the companies are left due exception, run below code to try again: {retry_later}')
    
#Code to retry getting data for failed companies    
remove_keys=[]
num_tries=0
wait_time =180
while len(retry_later)>0:
    print("Retrying for skipped ones...")
    num_tries+=1
    if num_tries>3:
        print("Max tries exceeded, exiting... ")
        break
    for key,val in retry_later.items():
        time.sleep(wait_time) #sleep in case we reached rate limit earlier
        wait_time += 1
        tweets_df=get_tweets(api,'$'+key,300)
        if (tweets_df is None):
            print(f"Skipped {key} due to exception, will retry later")
            continue
        if not(tweets_df.empty) :
            tweets_df.insert(0, 'Company', val)
            related_tweets=related_tweets.append(tweets_df, ignore_index=True)
            remove_keys.append(key)
    
    if remove_keys:
        for k in remove_keys: del retry_later[k]
            
#Save list of tweets            
related_tweets.to_csv(f"Twitter_Tech_data_{date.today()}.csv", index=False)

#Update original tech list with number of tweets and save the file
num_tweets_per_company=related_tweets[['Company','Tweet']].groupby('Company').agg({'Tweet':'count'}).reset_index()
hashtags=pd.merge(hashtags,num_tweets_per_company,on='Company',how='left')
hashtags.to_csv(f"FinalList_Tech_{date.today()}.csv", index=False)
