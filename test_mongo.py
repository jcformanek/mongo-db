#### Run the following comands in your shell ####

#### Setup the mongo db in a docker container ####
# docker pull mongo
# docker run -d -p 27017:27017/tcp --name my-mongo mongo:latest

#### To use the Mongo CLI ####
# docker exec -it my-mongo bash
# mongo


import pymongo # pip install pymongo
import json

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["books-db"]

books_col = mydb["books"]

with open('books.json') as f:
    file_data = json.load(f)

books_col.insert_many(file_data["books"])

myclient.close()
