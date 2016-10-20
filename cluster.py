__author__ = "Priya"
from pattern.en import sentiment
import mysql.connector
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from MySQLdb import OperationalError #Detect "the MySQL server has gone away" error
API_TIME_LIMIT = 15 #Time limit on API for each key
import numpy as np
    
def connect_to_database():
    global dbCursor
    global db
    db = MySQLdb.connect(host="CSI531ProjectX.db.6936824.hostedresource.com", user="CSI531ProjectX", passwd="Csi531!!",db="CSI531ProjectX")
    #Database cursor
    dbCursor = db.cursor() 

def collect_tweets():#function to collect tweets
    successful = False
    while not successful:
        try:
            cnx = mysql.connector.connect(user='CSI531ProjectX', password='Csi531!!', host='CSI531ProjectX.db.6936824.hostedresource.com', database='CSI531ProjectX')
            cursor = cnx.cursor()
            query = ("SELECT `tweet_id`, `username`, 'loc_id',`text` FROM `tweets`")
            cursor.execute(query)
        
            tweets=[]
        
            for (tweet_id, username, loc_id, text) in cursor:
                tweets.append(text)
                successful = True
        except OperationalError as e:
            print "Reconnecting to DB..."
            connect_to_database()
    cnx.close()
    return tweets
    
def symptom_vocab():# define symptoms here
    symptom={u'nosebleed': 0, u'flu': 1, u'hangover': 2, u'headache': 3}
    # Extract the vocabulary of keywords
    return symptom

def sentiment_score():#computing sentiment score for each tweets
    tweets=collect_tweets()    
    sentiment_score=[0]*len(tweets)   
    i=0    
    while i<len(tweets):
        sentiment_score.append(sentiment(tweets[i]))
        i=i+1
    sentiment_score=sentiment_score[len(tweets):-1]
    return sentiment_score

def generate_symptom_clusters(): # generatin clusters based on symptoms using k means
    # Generate X
    X = []
    tweets=collect_tweets()
    vocab=symptom_vocab()
    sentiment_score1=sentiment_score()
    for text in tweets:
        x = [0] * len(vocab)
        terms = [tweet_term for tweet_term in text.split() if len(tweet_term) > 2]
        for tweet_term in terms:
            if vocab.has_key(tweet_term):
                x[vocab[tweet_term]] += 1
        X.append(x)
    # K-means clustering
    km = KMeans(n_clusters = 4, n_init = 100) # try 100 different initial centroids
    km.fit(X)
#    for i in range(len(sentiment_score1)):
#        print [km.labels_.tolist()[i],sentiment_score1[i]]
#    print km.labels_.tolist()

    symptom_clusters=[]
    for i in range(len(vocab)):        
        for idx, cls in enumerate(km.labels_):
            cluster=[]
            if cls == i:
                cluster.append([tweets[idx],cls])
        symptom_clusters.append(cluster)
    symptom_clusters=np.asarray(symptom_clusters)

    k_means_cluster_centers = km.cluster_centers_

    fig = plt.figure(figsize=(8, 8))
    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.05, top=0.9)
    colors = ['red', 'blue', 'green','pink']
    ax = fig.add_subplot(1, 1, 1)
    result=[]
    print zip(*k_means_cluster_centers)

    for i in range(len(X)):
        if X[i][0]==1:
            result.append([k_means_cluster_centers[0][0]+sentiment_score1[i][0]+k_means_cluster_centers[3][2],k_means_cluster_centers[0][1]+sentiment_score1[i][1]+k_means_cluster_centers[3][2],0])
        elif X[i][1]==1:
            result.append([k_means_cluster_centers[1][0]+sentiment_score1[i][0]+k_means_cluster_centers[0][2],k_means_cluster_centers[1][1]+sentiment_score1[i][1]+k_means_cluster_centers[0][3],1])
        elif X[i][2]==1:
            result.append([k_means_cluster_centers[2][0]+sentiment_score1[i][0]+k_means_cluster_centers[1][2],k_means_cluster_centers[2][1]+sentiment_score1[i][1]+k_means_cluster_centers[1][3],2])
        elif X[i][3]==1:
            result.append([k_means_cluster_centers[3][0]+sentiment_score1[i][0]+k_means_cluster_centers[2][2],k_means_cluster_centers[3][1]+sentiment_score1[i][1]+k_means_cluster_centers[2][3],3])
        else:
            result.append([0,0,0])
        
    for i in range(len(result)):
        if result[i][2]==0:
            ax.plot(result[i][0],result[i][1],'w', markerfacecolor=colors[0], marker='.')
        elif result[i][2]==1:
            ax.plot(result[i][0],result[i][1],'w', markerfacecolor=colors[1], marker='.')
        elif result[i][2]==2:
            ax.plot(result[i][0],result[i][1],'w', markerfacecolor=colors[2], marker='.')
        elif result[i][2]==3:
            ax.plot(result[i][0],result[i][1],'w', markerfacecolor=colors[3], marker='.')
        
    ax.plot(k_means_cluster_centers[0][0]+k_means_cluster_centers[3][2]-1, k_means_cluster_centers[0][1]+k_means_cluster_centers[3][3]+1, 'o', markerfacecolor=colors[0], markeredgecolor='k', markersize=6)
    ax.plot(k_means_cluster_centers[1][0]+k_means_cluster_centers[0][2]+1, k_means_cluster_centers[1][1]+k_means_cluster_centers[0][3]-1, 'o', markerfacecolor=colors[1], markeredgecolor='k', markersize=6)
    ax.plot(k_means_cluster_centers[2][0]+k_means_cluster_centers[1][2]-1, k_means_cluster_centers[2][1]+k_means_cluster_centers[1][3]+1, 'o', markerfacecolor=colors[2], markeredgecolor='k', markersize=6)
    ax.plot(k_means_cluster_centers[3][0]+k_means_cluster_centers[2][2]+1, k_means_cluster_centers[3][1]+k_means_cluster_centers[2][3]-1, 'o', markerfacecolor=colors[3], markeredgecolor='k', markersize=6)
    ax.set_title('KMeans')
    ax.set_xticks(())
    ax.set_yticks(())
    
generate_symptom_clusters()
