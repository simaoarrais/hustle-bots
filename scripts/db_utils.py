import pymongo

def get_db(host, port, db_name):
    port = int(port)
    db_name = str(db_name)
    client = pymongo.MongoClient(host, port)
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

def update_post_status_insta(collection, post):
    result = collection.update_one(
        {"id": post['id']},    # Filter: find the document with the given post ID
        {"$set": {"status_insta": True}}  # Update: set status_insta to True
    )
    return result

def reject_post(collection, post):
    result = collection.find_one_and_delete(
        {"id": post['id']}  # Filter: find the document with the given post ID
    )
    return result

def get_next_post_x(collection):
    result = collection.find_one(
        { "status_x": False },  # Filter where status_x is False
        sort=[("score", pymongo.DESCENDING)]  # Sort by score in descending order
    )
    return result

def get_next_post_insta(collection):
    result = collection.find_one(
        { "status_insta": False },  # Filter where status_x is False
        sort=[("score", pymongo.DESCENDING)]  # Sort by score in descending order
    )
    return result