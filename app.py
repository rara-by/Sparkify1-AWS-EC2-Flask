import pymongo 
from bson.son import SON
from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)
@app.route("/")
def home():
    # mongoDB hosted on an AWS EC2 instance (public IP: 54.173.225.16)
    myclient = pymongo.MongoClient("mongodb://54.173.225.16:27017/")

    mydb = myclient["mydatabase"] #create database
    
    #display data headers
    print(myclient.list_database_names())
    print(mydb.list_collection_names())

    # weeks = ["week1", "week2", "week3", "week4", "week5"]

    def aggregate_function(week, mydb=mydb):
        collection = mydb[week]
        print("Week: ", week)

        # the aggregate pipeline here counts song frequencies,
        # sorts based on those frequencies,
        # and eliminates null values 
        # note: the bson package is by default installed with pymongo
        aggregated = collection.aggregate([{"$unwind": "$_id"},
                                    {"$match": {"artist": {"$ne": None}}},
                                    {"$group": {"_id": ["$song", "$artist"], "num_played": {"$sum":1}}},
                                    {"$sort": SON([("num_played", -1), ("_id", -1)])},
                                    { "$limit": 10 }])
        
        # separate the items to display: song and artist
        aggregated_list = list(aggregated)
        top_ten = {}
        # pprint.pprint(aggregated_list)
        for idx, item in enumerate(aggregated_list):
            # print(item['_id'][0])
            top_ten[idx] = {"Song": item['_id'][0], "Artist": item['_id'][1]}

        return top_ten
    
    # a template folder is necessary for flask.render_template()
    path = "templates"
    # Check whether the templates path exists in the directory
    isExist = os.path.exists(path)

    if not isExist:
        os.makedirs(path)

    # for week in weeks:
    # aggregated_dict[week] = aggregate_function(week)

    # html tables
    df1 = pd.DataFrame.from_dict(aggregate_function('week1'))
    df2 = pd.DataFrame.from_dict(aggregate_function('week2'))
    df3 = pd.DataFrame.from_dict(aggregate_function('week3'))
    df4 = pd.DataFrame.from_dict(aggregate_function('week4'))
    df5 = pd.DataFrame.from_dict(aggregate_function('week5'))

    os.chdir("./templates/")

    with open("top.html", "w", encoding="utf-8") as file:
        # create HTML table to display query results
        file.write("<html>\n<head>\n <h1>Top 10 Songs and Artists Each Week</h1></head>" + \
                "<body>\n\n\n Week 1" + "\n\n\n" + \
                df1.to_html() + "\n\n\n" + \
                "Week 2" + "\n\n\n" + \
                df2.to_html() + "\n\n\n" + \
                "Week 3" + "\n\n\n" + \
                df3.to_html() + "\n\n\n" + \
                "Week 4" + "\n\n\n" + \
                df4.to_html() + "\n\n\n" + \
                "Week 5" + "\n\n\n" + \
                df5.to_html() +
                "</body></html>")
        

    # pprint.pprint(aggregated_dict)

    return render_template("top.html")
    # return 'Hello, Flask'

if __name__ == '__main__':
    app.run()




