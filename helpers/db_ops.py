
def get_db():
    from pymongo import MongoClient as mc
    import pymongo
    from dotenv import load_dotenv
    import os

    load_dotenv()

    db_name = os.getenv('dbname')
    db_pass = os.getenv('mongodb_password')
    db_uri = 'mongodb+srv://ice:{}@cluster0.hpfbnjd.mongodb.net/{}?retryWrites=true&w=majority'.format(db_pass, db_name)

    cluster = mc(db_uri)
    # print(cluster)

    db = cluster['API']
    # collection = db['books']
    return db


# print(get_db()['books'])
if __name__ == '__main__':
    database_name = get_db()
