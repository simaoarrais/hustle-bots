from pymongo import MongoClient, errors

def get_db(host, port, db_name):
    port = int(port)
    db_name = str(db_name)
    client = MongoClient(host, port)
    return client[db_name]

def get_collection(db, collection):
    return db[collection]

def insert_document(collection, post):
    if collection.find_one({"id": post["id"]}):
        print(f'ID - {post["id"]} already exists')
        return False
    
    collection.insert_one(post)
    print("Document inserted successfully")
    return True

    # except errors.DuplicateKeyError:
    #     print(f'Duplicate key error: Document with ID {post["_id"]} already exists')
    #     return False
    # except Exception as e:
    #     print("An error occurred:", e)
    #     return False