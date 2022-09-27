import gridfs
import base64
from pymongo import MongoClient

pdf_name = "not_defined"

def get_database():

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://abyaav:Y6srlzv7NukT4IYM@cluster0.xl4rlg0.mongodb.net/myFirstDatabase"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['pdf_store']


def mongo_pdf(encoded_string, name):
    # Get the database

    dbname = get_database()
    # path = 'Trial1.pdf'
    # db = client.storagearea
    fs = gridfs.GridFS(dbname)
    # Note, open with the "rb" flag for "read bytes"
    # with open(path, "rb") as f:
    #     encoded_string = base64.b64encode(f.read())
    with fs.new_file(chunkSize=800000, filename=name) as fp:
        fp.write(encoded_string)


def download(name_of_pdf):
    
    global data_pdf
     
    db = get_database()

    cursor = db.fs.files.find({'filename': name_of_pdf})

    for i in cursor:
        dict = i

    chunks_cursor = db.fs.chunks.find({'files_id': dict['_id']})

    for j in chunks_cursor:
        dict1 = j

    # print(dict1['data'])

    k = dict1['data'].decode('utf-8')

    data_pdf = k.split(",")[1]
    
    # delete(name_of_pdf)

    # decode = open("Copy - Copy.pdf", 'wb')
    
    return base64.b64decode(data_pdf)
   
    


def delete(name_of_pdf):
    db = get_database()
    
    cursor = db.fs.files.find({'filename': name_of_pdf})

    for i in cursor:
        dict = i

    db.fs.chunks.delete_one({'files_id': dict['_id']})
    db.fs.files.delete_one({'filename': dict['_id']})


    # cursor = db.fs.files.find({'filename': name_of_pdf})

    # for i in cursor:
    #     dict = i

    # chunks_cursor = db.fs.chunks.find({'files_id': dict['_id']})
    
    # for j in chunks_cursor:
    #     dict1 = j

    
    # db.fs.files.delete_one({'files_id': dict['_id']})
    
    

