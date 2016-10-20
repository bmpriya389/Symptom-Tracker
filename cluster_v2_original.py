__author__ = "Priya"
import mysql.connector
import matplotlib.pyplot as plt
from MySQLdb import OperationalError #Detect "the MySQL server has gone away" error
API_TIME_LIMIT = 15 #Time limit on API for each key
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import csv

def collect_loc():#store location information
    locations=[]            
    with open('nonunique.txt', 'rU') as input:
        
        reader = csv.reader(input)
        for row in reader:
            locations.append([row[0],row[1],row[2]])
    return locations
    
def location_dict():# define symptoms here
    d = {}
    with open('uniqueLocations.txt', 'rU') as input:
        reader = csv.reader(input)
        for row in reader:
            key = row[0]
            val = np.random.rand(3,1).tolist()       
            d[int(key)] = val
    # Extract the vocabulary of keywords
    return d

def locations_latlon():# define colors for each location cluster here
    d = {}
    with open('uniqueLocations.txt', 'rU') as input:
        reader = csv.reader(input)
        for row in reader:
            key = row[0]
            val = [row[1],row[2]]  
            d[int(key)] = val
    # Extract the vocabulary of keywords
    return d

def generate_symptom_clusters(): # generating clusters based on symptoms using k means
    # Generate X
    i=0
    latlon=np.asarray(collect_loc())
    vocab=location_dict()

    fig = plt.figure(figsize=(8, 8))
    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.05, top=0.9)
    ax = Axes3D(fig)
    result=[]
        
    for i in range(len(latlon)):
        if latlon[i][0]==i:
            result.append([float(latlon[i][0]),float(latlon[i][1]),float(latlon[i][2])])       
        else:
            result.append([0,0,0])
    
    result=np.asarray(result)
    
    for i in range(len(result)):
        if i in vocab.keys():
            ax.scatter(float(latlon[i][0]),float(latlon[i][1]),float(latlon[i][2]),c=vocab.get(i),edgecolors='none', marker='o')
    ax.set_xlabel('Location ID')
    ax.set_ylabel('Latitude')
    ax.set_zlabel('Longitude')
#    Axes3D.plot(k_means_cluster_centers[0][0],k_means_cluster_centers[0][0], k_means_cluster_centers[0][0], 'o', markerfacecolor=colors[0], markeredgecolor='k', markersize=6)
#    Axes3D.set_title('KMeans')
    fig.savefig('location_clusters.png')



generate_symptom_clusters()
