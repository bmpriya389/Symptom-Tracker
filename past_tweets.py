# -*- coding: utf-8 -*-
"""
Created on Wed Feb 25 05:54:34 2015

@author: Priya's
"""

import twitter, sys, json
import datetime

reload(sys)
sys.setdefaultencoding("utf-8")
myApi=twitter.Api(consumer_key='w3LC2qxR7uGwN26xumjCsp61q', \
                  consumer_secret='twKecYAretoInz3ii3NfyPgKyRIEaCBmB2JtAdUO53AXapHL9A', \
                  access_token_key='2642530542-Ti6nrJ8QwmcKBq7bxrFvFwP5yhQAtKjWQrhDjql', \
                  access_token_secret='vQdEWEN8ZuyNymmASQ6BWMUwjUOk1bsepe9auuR1Free1')

def query_flu_outbreaks(from_date):
    query = "flu"
    geo = ('40.7127', '-74.0059', '30mi') # City of New York
    max_id = None
    flu_tweets=[]
    n=1
    for it in range(5):
        tweets=[json.loads(str(raw_tweet)) for raw_tweet \
                in myApi.GetSearch(query, geo, count=100,max_id= max_id, result_type='recent')]
        
        if tweets:
            max_id=tweets[-1]['id']
            max_date=tweets[-1]['created_at']   
            print max_date
            print max_id, len(tweets)
            if max_date!=from_date:
                n=n+1
        flu_tweets=(flu_tweets+tweets)

    flu_tweets=[i for j, i in enumerate(flu_tweets) if i not in flu_tweets[j + 1:]] #removing duplicate tweets

        
    print len(flu_tweets)
    writer=open('tweet_flu.txt','w')
    flu_tweet=[]
    for raw_tweet in flu_tweets:
        flu_tweet.append(raw_tweet)
        writer.write(json.dumps(raw_tweet)+'\n')

        
def main():
    print datetime.date.today()
    query_flu_outbreaks(2015-04-23)

if __name__ == '__main__':
    main()
