# run the following comands to set up mongo
# $ sudo systemctl start mongod
# $ mongo

# when finished running then run the following comands
# exit (in mongo shell)
# sudo systemctl stop mongo

import pymongo
import json
import random

def create_database(myclient):

    # load in books dataset
    with open('books.json') as f:
        books_data = json.load(f)

    # load in students data
    with open('students.json') as f:
        students_data = json.load(f)

    # creating database
    mydb = myclient['books-db']

    # print the collections
    print(mydb.list_collection_names())

    # creating the books collection
    books_collection = mydb['books']
    books_inserted_documents = books_collection.insert_many(books_data['books'])

    # creating the students collection
    students_collection = mydb['students']
    students_inserted_documents = students_collection.insert_many(students_data['students'])

    # print the collections
    print("The books-db collections: ",mydb.list_collection_names())

    # prints a list of databases
    print("The following databases have been created: ",myclient.list_database_names())


def main():

    # setting up the mongodb client
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    # check if the database has been created in mongodb if not create it
    dblist = myclient.database_names()
    if "books-db" in dblist:
        print("books-db has already been created")
    else:
        create_database(myclient)

    # get the database from mongodb
    mydb = myclient['books-db']

    # get the book collection from the db
    books_collection = mydb['books']

    # get the students collection from db
    students_collection = mydb['students']

    # performing some actions here
    print(books_collection.find_one())
    print(students_collection.find_one())


    # clean up client resources and disconnect from mongoDB
    myclient.close()
    
    

if __name__ == "__main__":
    main()

    







