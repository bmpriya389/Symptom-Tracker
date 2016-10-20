# Sam Pellino
# UA ID: 001175569
# Net ID: sp492873
# CSI 531, Data Mining, Spring 2015

#yum install mysql
#yum install mysql-devel
#yum install MySQL-python

import datetime #Used to create timestamps for data/JSON filenames
import sys #Used for setting the default encoding
import time #Used to make python wait (sleep) before executing the query again
import tweepy #Twitter API library wrapper
import MySQLdb #Used to connect to the MySQL database
from django.utils.html import escape

CALL_EVERY_N_MINS = 10 #Query all locations every N minutes

#Query to obtain tweets about users having the flu
FLU_QRY = "(' I ' OR 'I\'m' OR 'Im' OR 'I\'ve' OR 'I have' OR 'sick' OR 'down' OR 'got' OR 'caught' OR 'get' OR 'have' OR 'catch') AND ('flu') -RT"

reload(sys)
sys.setdefaultencoding("utf-8") #Set encoding for output

access_token_key = "1621903950-eEeHg0oFZistLmfblxNX03Gknsi7ZVJRdkL7o5J"; #Access token key
access_token_secret = "wFO0HvPmaziFiRpAEuyVPsvfnEHbx0rkKMcAhSjx1ljlu"; #Access token secret
consumer_key = "UA5lDJnNeTBLhl6wICOOBvoMF" #Consumer key
consumer_secret = "im95QUS2y8pVlLkfSwQB1OabO3NHJHvXW9YEeNhZS1pLUKbpuG" #Consumer secret
OAuth = tweepy.OAuthHandler(consumer_key, consumer_secret) #Twitter OAuth object
OAuth.set_access_token(access_token_key, access_token_secret) #Set access tokens in the OAuth object
api = tweepy.API(OAuth) #Generate twitter API object
db = None
dbCursor = None #Database cursor

DATA_FOLDER_PATH = "data" #Folder where all data will be housed
USR_SPEC_FOLDER = "usr_specific" #Folder where all user-specific tweets will be stored

#This function returns a tweet's useful information
def get_useful_tweet_info(tweet, locationStr):
    return [tweet.id,locationStr,tweet.created_at,tweet.user.screen_name,tweet.text]

#This function simply executes the query through the REST API
def rest_query_ex(qry,geo):
    return api.search(q=qry, geocode=geo, result_type="recent") #Execute the REST query and return the result
    
def connect_to_database():
    global dbCursor
    global db
    db = MySQLdb.connect(host="CSI531ProjectX.db.6936824.hostedresource.com", user="CSI531ProjectX", passwd="Csi531!!",db="CSI531ProjectX")
    #Database cursor
    dbCursor = db.cursor() 

def insert_tweets_into_db(tweets, locationID):
    for tweet in tweets:
        tweet.user.screen_name = escape(tweet.user.screen_name)
        tweet.text = escape(tweet.text)
        dbQuery = "INSERT IGNORE INTO `tweets` (`tweetID`,`username`,`text`,`location`,`created_at`) VALUES ('"+str(tweet.id)+"','"+str(tweet.user.screen_name)+"','"+str(tweet.text)+"','"+str(locationID)+"','"+str(tweet.created_at)+"')"
        dbCursor.execute(dbQuery)

def insert_runtime_into_db(runBegin):
    dbQuery = "INSERT INTO `run_times` (`run_begin`,`run_end`) VALUES ('"+str(runBegin)+"','"+str(datetime.datetime.utcnow())+"'); "
    dbCursor.execute(dbQuery)
    
def get_locations_from_db():
    locationsList = []
    dbQuery = "SELECT * FROM `locations`"
    dbCursor.execute(dbQuery)
    for loc in dbCursor.fetchall():
        locationsList.append({"loc_id":loc[0], "city":loc[1], "state":loc[2], "geocode": "%s,%s,%smi" % (str(loc[3]),str(loc[4]),str(loc[5])) })
    return locationsList

def main():
    
    while True: #Loop forever
        connect_to_database() #Connect to database
        runBegin = datetime.datetime.utcnow()
        
        locationsList = get_locations_from_db()
        
        for location in locationsList: #For each location in the locations list
            tweets = rest_query_ex(FLU_QRY,location['geocode']) #Execute REST query at that geolocation
            insert_tweets_into_db(tweets, location['loc_id']) #Insert the tweets collected into the database
        
        insert_runtime_into_db(runBegin)
        db.close()
        
        #Let the user know when the next query execution will be
        print "********************************************************************************"
        print "Next execution time: " + str(datetime.datetime.utcnow() + datetime.timedelta(minutes=CALL_EVERY_N_MINS))
        print "********************************************************************************"
        time.sleep(60 * CALL_EVERY_N_MINS) #Sleep for N minutes before executing the query again
        
if __name__ == '__main__':
    main() #Call main