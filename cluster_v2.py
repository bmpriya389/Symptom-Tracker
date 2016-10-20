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
    
def location_dict():# define colors for each location cluster here
    d = {}
    with open('uniqueLocations.txt', 'rU') as input:
        reader = csv.reader(input)
        for row in reader:
            key = row[0]
            val = np.random.rand(3,1).tolist()       
            d[int(key)] = val
    return d

def locations_latlon():# define colors for each location cluster here
    d = {}
    with open('uniqueLocations.txt', 'rU') as input:
        reader = csv.reader(input)
        for row in reader:
            key = row[0]
            val = str(row[1]+','+row[2])
            d[int(key)] = val
    return d

def generate_symptom_clusters(): # generating clusters based on symptoms using k means
    # Generate X
    latlon=np.asarray(collect_loc())
    vocab=location_dict()
    latlondict=locations_latlon()

    fig = plt.figure(figsize=(8, 8))
    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.05, top=0.9)
    ax = Axes3D(fig)
    result=zip(*latlon)  

    count=[]
    i=1
    
    for i in vocab.keys():
        count.append([i,result[0].count(str(i))])
    count=np.asarray(count)
    
    for i in range(len(result[0])):
        if i in vocab.keys():
            ax.scatter(float(latlon[i][0]),float(latlon[i][1]),float(latlon[i][2]),c=vocab.get(i),edgecolors='none', marker='o')
    ax.set_xlabel('Location ID')
    ax.set_ylabel('Latitude')
    ax.set_zlabel('Longitude')
    fig.savefig('location_clusters.png')
    
    with open('location_clusters_latlonpair.txt', 'w') as writer:    
        for i in range(len(count)):
            if latlondict.has_key(count[i][0]) and count[i][1]!=0:
                for j in range(count[i][1]):
                    if j==(count[i][1]-1):
                        writer.write(str(latlondict.get(count[i][0])))
                    else:
                        writer.write(str(latlondict.get(count[i][0])) + ',')
                writer.write('\n')
                
generate_symptom_clusters()