import sys
from pymongo import MongoClient

HOST = '127.0.0.1'
PORT = '27017'

def parse_string(string):
    return {key: value if len(value.split(',')) == 1 else value.split(',')
            for key, value in (pair.split('=') for pair in string.split('.'))}

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Command format: <parser script> <string to parse>")
        sys.exit(0)

    unparsed_document = sys.argv[1]

    client = MongoClient("mongodb://{host}:{port}".format(host=HOST, port=PORT))
    db = client.test
    collection = db['parse-objects-collection']

    collection.insert_one(parse_string(unparsed_document))
