import json
from flask import request
from bson import ObjectId
import os
from flask import Flask, request
import pymongo
from werkzeug.utils import secure_filename
from datetime import datetime
import glob
from dotenv import load_dotenv
from cloudStorage import upload_blob, delete_blob
load_dotenv()

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "./src/images"

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

DB_PROJECT_NAME = os.environ.get('DB_PROJECT_NAME')
DB_NAME = os.environ.get("DB_NAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
BUCKET_NAME = os.environ.get('BUCKET_NAME')

client = pymongo.MongoClient(
    f"mongodb+srv://{DB_PROJECT_NAME}:{DB_PASSWORD}@cluster0.y0meq.mongodb.net/{DB_NAME}?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
db = client['ccp2-capstone']
mediaCollection = db['media']
locationsCollection = db['locations']
usersCollection = db['users']
photoCollection = db["photos"]


@app.route('/')
def index():
    return 'You reached backend server for ccp2-capstone'


@app.route('/api/media')
def getMedia():
    result = []
    for tv in mediaCollection.find({"media_type": "tv"}, {"id": True, "name": True, "_id": False, "poster_path": True}):
        print(tv)
        result.append(tv)
    for movie in mediaCollection.find({"media_type": "movie"}, {"id": True, "name": "$title", "_id": False, "poster_path": True}):
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
    return json.dumps(result)


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


@app.route("/api/user/<userId>/location/<locationId>/photo", methods=["POST"])
def postPhotoByUserId(userId, locationId):
    if "file" not in request.files:
        return "No file was attached in request"

    uploadedFile = request.files["file"]
    try:
        filename = secure_filename(uploadedFile.filename)
        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"], filename)
        uploadedFile.save(filepath)

        # filename stored in the Cloud Storage
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        destinationBlobName = f"{userId}+{locationId}+{timestamp}"

        url = upload_blob(BUCKET_NAME, filepath, destinationBlobName)

        cloudStorageData = {
            "url": url,
            "user_id": userId,
            "location_id": locationId,
            "blob_name": destinationBlobName
        }
        photoCollection.insert_one(cloudStorageData)

    except Exception as e:
        return repr(e)

    finally:
        files = glob.glob(app.config['UPLOAD_FOLDER'] + "/*")
        for file in files:
            os.remove(file)

    cloudStorageData["_id"] = str(cloudStorageData["_id"])
    return cloudStorageData


@app.route("/api/photo/<id>", methods=["DELETE"])
def deletePhotoByObjectId(id):
    photoToDelete = photoCollection.find_one({"_id": ObjectId(id)})
    try:
        delete_blob(BUCKET_NAME, photoToDelete["blob_name"])
        photoCollection.delete_one({"_id": ObjectId(id)})
    except Exception as e:
        return repr(e)
    return id


@app.route("/api/user/<id>/photo")
def getPhotoByUserId(id):
    photos = []
    for photo in photoCollection.find({"user_id": id}):
        photos.append(photo)
        photo["_id"] = str(photo["_id"])
    return json.dumps(photos)


@app.route("/api/location/<id>/photo")
def getPhotoByLocationId(id):
    photos = []
    for photo in photoCollection.find({"location_id": id}):
        photos.append(photo)
        photo["_id"] = str(photo["_id"])
    return json.dumps(photos)


@app.route('/api/user/<id>')
def getUserById(id):
    result = []
    print(type(id))
    for user in usersCollection.find({"_id": id}):
        print(user)
        user['_id'] = str(user['_id'])
        result.append(user)
    return json.dumps(result)


@app.route('/api/user/<id>/bookmarks', methods=['PATCH', 'GET', 'DELETE'])
def userBookmarks(id):
    if request.method == 'PATCH':
        newUserBookmark = request.get_json()
        if newUserBookmark != None:
            addedB = usersCollection.update_one(
                {"_id": id}, {"$push":  {"bookmarks":  newUserBookmark}})
            return "Bookmark Added"
        else:
            return "Error! There is no json body in the request."
    elif request.method == 'GET':
        result = []
        userBookmarks = usersCollection.find_one(
            {"_id": id}, {"_id": False, "bookmarks": True})
        result.append(userBookmarks)
        return json.dumps(result)
    elif request.method == 'DELETE':
        deleteBookmark = request.get_json()
        if deleteBookmark != None:
            deletedB = usersCollection.update_one(
                {"_id": id}, {"$pull": {"bookmarks":  deleteBookmark}})
            return "Bookmark Deleted"
        else:
            return "Error! There is no json body in the request."


@app.route('/api/user/<id>/profile', methods=["PATCH", "GET"])
def userProfile(id):
    if request.method == 'PATCH':
        editProfile = request.get_json()

        if editProfile != None:
            for key, value in editProfile.items():
                user = usersCollection.update_one(
                    {"_id": id}, {"$set":  {key: value}})
            return "Profile edited"
        else:
            return "Error! There is no json body in the request."
    else:
        result = []
        profile = usersCollection.find_one(
            {"_id": id}, {"_id": False, "username": True, "email": True, "bio": True, "avatar": True})
        result.append(profile)
        return json.dumps(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
