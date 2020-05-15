import pymongo
import json

def get_client():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    return client

def close_client(client):
    client.close()

def create_database(client):
    dblist = client.database_names()

    # If books-db exists, drop it and create a new one. This is to keep
    # the version of the DB the program starts on consistent.
    if "books-db" in dblist:
        print("Droping old version of DB")
        client.drop_database('books-db')

    print("Creating books-db database")

    # load in books dataset
    with open('books.json') as f:
        books_data = json.load(f)

    # load in students data
    with open('students.json') as f:
        students_data = json.load(f)

    # creating database
    mydb = client['books-db']

    # creating the books collection
    books_collection = mydb['books']
    books_inserted_documents = books_collection.insert_many(books_data['books'])

    # creating the students collection
    students_collection = mydb['students']
    students_inserted_documents = students_collection.insert_many(students_data['students'])

    # print the collections
    print("The books-db collections: ",mydb.list_collection_names())

    # prints a list of databases
    print("The following databases have been created: ",client.list_database_names())

# Claude's Operation
def claude_operation(client):
    print("### Start of Claude's Operation ###")
    books = client.get_database("books-db").get_collection("books")

    # Get the list of student id's on the Android in action book
    book = books.find_one({'title':'Android in Action, Second Edition'}, 
                        {"title":1, "_id":0, "students":1})
    print("Before update:", book)

    # Add student with id 5 to the list of students on the book
    books.update_one({'title':'Android in Action, Second Edition'},
                        {"$push":{'students':5}})

    # Show that the update was successful
    book = books.find_one({'title':'Android in Action, Second Edition'}, 
                        {"title":1, "_id":0, "students":1})
    print("After update:", book)

    print("### End of Claude's Operation ###")

# Matts's Operation
def matt_operation(client):
    pass

# Emil's Operation
def emil_operation(client):
    pass

# Justin's Operation
def justin_operation(client):
    print("### Start of Justin's Operation ###")
    students = client.get_database("books-db").get_collection("students")

    student = students.find_one({'_id':200, 'name':'Justin Dorman'})

    print("Before insert, search for Justin Dorman:", student )

    newstudent = {"_id": 200, "name": "Justin Dorman", "scores": [ { "score": 85.21,"type": "exam" }, { "score": 73.88, "type": "quiz" }, { "score": 95.33, "type": "homework"}] }

    students.insert_one(newstudent)

    print("Operation: Insert student, Justin Dorman with relevant details")

    #show that insert was successful
    student = students.find_one({'_id':200, 'name':'Justin Dorman'})
    print('After insert, search for Justin Dorman', student)

    print("### End of Justin's Operation ###")



def main():
    client = get_client()

    create_database(client)

    claude_operation(client)

    emil_operation(client)

    matt_operation(client)

    justin_operation(client)

    close_client(client)

if __name__ == "__main__":
    main()