import json
from flask import request
from bson import ObjectId
import os
from flask import Flask, request
import pymongo
from google.cloud import storage
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import glob
load_dotenv()

app = Flask(__name__)

UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

DB_PROJECT_NAME = os.environ.get('DB_PROJECT_NAME')
DB_NAME = os.environ.get("DB_NAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

client = pymongo.MongoClient(
    f"mongodb+srv://{DB_PROJECT_NAME}:{DB_PASSWORD}@cluster0.y0meq.mongodb.net/{DB_NAME}?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
db = client['ccp2-capstone']
mediaCollection = db['media']
locationsCollection = db['locations']
usersCollection = db['users']


@app.route('/')
def index():
    return 'Hello World from Python'


@app.route('/test')
def test():
    return 'test'


@app.route('/api/media')
def getMedia():
    result = []
    for tv in mediaCollection.find({"media_type": "tv"}, {"id": True, "name": True, "_id": False}):
        print(tv)
        result.append(tv)
    for movie in mediaCollection.find({"media_type": "movie"}, {"id": True, "name": "$title", "_id": False}):
        print(movie)
        result.append(movie)
    return json.dumps(result)


@app.route('/api/locations')
def getLocations():
    result = []
    for location in locationsCollection.find({}, {"plus_code": True, "name": True, "media_id": True, "_id": 1}):
        print(location)
        location['_id'] = str(location['_id'])
        result.append(location)
    return json.dumps(result)


@app.route('/api/locations/<id>')
def getLocation(id):
    result = []
    print(type(id))
    for location in locationsCollection.find({"_id": ObjectId(id)}):
        print(location)
        location['_id'] = str(location['_id'])
        result.append(location)
    return json.dumps(result[0])


@app.route('/api/media/<id>')
def getMediaById(id):
    media = mediaCollection.find_one({"id": int(id)})
    media['_id'] = str(media['_id'])
    return json.dumps(media)


@app.route("/api/media/<id>/locations")
def getMediaLocationById(id):
    result = []
    for location in locationsCollection.find({"media_id": {"$all": [id]}}):
        location['_id'] = str(location['_id'])
        result.append(location)
    return json.dumps(result)


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )


@app.route("/api/user/<id>/photo", methods=["POST"])
def postPhotoByUserId(id):
    uploaded_file = request.files["file"]
    if uploaded_file.filename != "":
        try:
            filename = secure_filename(uploaded_file.filename)
            uploaded_file.save(os.path.join(
                app.config["UPLOAD_FOLDER"], filename))

            BUCKET_NAME = os.environ.get('BUCKET_NAME')
            source_file_name = f"./images/{filename}"
            destination_blob_name = f"postTest{id}"
            upload_blob(BUCKET_NAME, source_file_name, destination_blob_name)
        except(e):
            return e

        finally:
            files = glob.glob("./images/*")
            for file in files:
                os.remove(file)
    return f"Uploaded {source_file_name} as {destination_blob_name}"


@app.route('/api/user/<id>')
def getUserById(id):
    result = []
    print(type(id))
    for user in usersCollection.find({"_id": ObjectId(id)}):
        print(user)
        user['_id'] = str(user['_id'])
        result.append(user)
    return json.dumps(result[0])


@app.route('/api/user/<id>/bookmarks', methods=['POST', 'GET', 'DELETE'])
def userBookmarks(id):
    if request.method == 'POST':
        newUserBookmark = request.get_json()
        addedB = usersCollection.update_one(
            {"_id": ObjectId(id)}, {"$push":  {"bookmarks":  newUserBookmark}})
        return "Bookmark Added"
    elif request.method == 'GET':
        userBookmarks = usersCollection.find_one(
            {"_id": ObjectId(id)}, {"_id": False, "bookmarks": True})
        print(userBookmarks)
        return userBookmarks
    elif request.method == 'DELETE':
        deleteBookmark = request.get_json()
        deletedB = usersCollection.update_one(
            {"_id": ObjectId(id)}, {"$pull": {"bookmarks":  deleteBookmark}})
        return "Bookmark Deleted"


@app.route('/api/user/add')
def addUser():
    newUser = request.get_json()
    user = usersCollection.insert_one(newUser)
    return "User Added"

# @app.route('/api/user/addcontent')
# def addContent():
#     #post json doc
#     userContent = usersCollection.insert()
#     return json.dumps(userContent)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
