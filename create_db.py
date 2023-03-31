import pymongo 
import os
import json

# mongoDB hosted on an AWS EC2 instance (public IP: 54.173.225.16)
myclient = pymongo.MongoClient("mongodb://54.173.225.16:27017/")
myclient.drop_database('mydatabase') #if database already exists
mydb = myclient["mydatabase"] #create database

path = "/home/ubuntu/sparkify1/data/log_data/2018/11/"
file_names = os.listdir(path)
# print(path+file_names[0])

#divide the dataset into weeks
week1 = file_names[0:7]
week2 = file_names[7:14]
week3 = file_names[14:21]
week4 = file_names[21:28]
week5 = file_names[28:]

weeks = {'week1': week1, 'week2': week2, 'week3': week3, 'week4': week4, 'week5': week5}

#create five collection objects in MongoDB for each week
for key, value in weeks.items():
    collection = mydb[key]
    for file_name in value:
        with open(path + file_name) as f:
            log_list = []
            for line in f:
                file_data = json.loads(line)  # load data from JSON file to dict
                # for key, value in file_data.items():  # iterate over key-value pairs
                log_list.append(file_data)
            
            x = collection.insert_many(log_list)  #collection object here

#display data headers
print(myclient.list_database_names())
print(mydb.list_collection_names())

#query into database for testing purpose
val = mydb['week1'].find_one({"artist":"Sydney Youngblood"})
print(val)
