from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_caching import Cache

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/ncov"

cache = Cache(config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': "redis://localhost:6123"})
cache.init_app(app)
mongo = PyMongo(app)


@app.route('/')
@cache.cached(timeout=50)
def hello_world():
    array = []
    for data in mongo.db.ncov.find({}):
        data['_id'] = str(data["_id"])
        array.append(data)

    return jsonify(array)


def insert_to_db():
    import json
    with open("nCoV.json", 'r', encoding="utf-8") as f:
        data = json.load(f)
    mongo.db.ncov.insert(data)


if __name__ == '__main__':
    app.run()
