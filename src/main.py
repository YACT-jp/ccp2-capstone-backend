from flask_cors import CORS
from functools import wraps
from flask_bcrypt import Bcrypt
import jwt
import json
from bson import ObjectId
import bson
import os
from flask import Flask, request, jsonify
import pymongo
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import glob
from dotenv import load_dotenv
from cloudStorage import upload_blob, delete_blob
load_dotenv()

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "./src/images"
CORS(app, resources={r"/*": {"origins": "*"}})
bcrypt = Bcrypt(app)
secret = os.environ.get('SUPER_DUPER_SECRET')

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


def tokenReq(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].replace("Bearer ", "")
            try:
                jwt.decode(token, secret, algorithms=["HS256"])
            except Exception as e:
                return repr(e)
            return f(*args, **kwargs)
        else:
            return jsonify({"status": "fail", "message": "unauthorized"}), 401
    return decorated


@app.route('/api/auth', methods=['POST'])
def auth():
    message = ""
    res_data = {}
    code = 500
    status = "fail"
    try:
        data = request.get_json()
        user = db['users'].find_one({"email": f'{data["email"]}'})

        if user:
            time = datetime.utcnow() + timedelta(hours=744)
            token = jwt.encode({
                "user": {
                    "email": f"{user['email']}",
                    "id": f"{user['_id']}",
                },
                "exp": time
            }, secret, 'HS256').decode('utf-8')

            message = f"user authenticated"
            code = 200
            status = "successful"
            res_data['token'] = token
            res_data['user'] = user
        else:
            message = "invalid login details"
            code = 401
            status = "fail"

    except Exception as ex:
        message = f"{ex}"
        code = 500
        status = "fail"
    return jsonify({'status': status, "data": res_data, "message": message}), code


@app.route('/')
def index():
    return 'You reached backend server for E-Mina'


@app.route('/authtest')
@tokenReq
def index2():
    return 'Auth Successful'


@app.route('/api/media')
@tokenReq
def getMedia():
    result = []
    for tv in mediaCollection.find({"media_type": "tv"}, {"id": True, "name": True, "_id": False, "poster_path": True, "overview": True}):
        result.append(tv)
    for movie in mediaCollection.find({"media_type": "movie"}, {"id": True, "name": "$title", "_id": False, "poster_path": True, "overview": True}):
        result.append(movie)
    return json.dumps(result)


@app.route('/api/locations')
@tokenReq
def getLocations():
    result = []
    for location in locationsCollection.find({}):
        location['_id'] = str(location['_id'])
        result.append(location)
    return json.dumps(result)


@app.route('/api/locations/<id>')
@tokenReq
def getLocation(id):
    try:
        location = locationsCollection.find_one({"_id": ObjectId(id)})
    except bson.errors.InvalidId as e:
        return jsonify({"status": 400, "message": "Invalid ID Format"}), 400
    if location is None:
        return jsonify({"status": 404, "message": "Not Found"}), 404
    location['_id'] = str(location['_id'])
    return json.dumps(location)


@app.route('/api/media/<id>')
@tokenReq
def getMediaById(id):
    media = mediaCollection.find_one({"id": int(id)})
    if media is None:
        return jsonify({"status": 404, "message": "Not Found"}), 404
    media['_id'] = str(media['_id'])
    return json.dumps(media)


@app.route("/api/media/<id>/locations")
@tokenReq
def getMediaLocationById(id):
    result = []
    for location in locationsCollection.find({"media_id": {"$all": [id]}}):
        location['_id'] = str(location['_id'])
        result.append(location)
    return json.dumps(result)


@app.route("/api/user/<userId>/location/<locationId>/photo", methods=["POST"])
@tokenReq
def postPhotoByUserId(userId, locationId):
    if "file" not in request.files:
        return "No file was attached in request"

    uploadedFile = request.files["file"]
    description = request.form["description"]
    try:
        # Check if locationId and mediaId exist
        location = locationsCollection.find_one({"_id": ObjectId(locationId)})
        user = usersCollection.find_one({"_id": userId})

        if location is None:
            return jsonify({"status": 404, "message": "LocationID Not Found"}), 404
        if user is None:
            return jsonify({"status": 404, "message": "UserID Not Found"}), 404

        filename = secure_filename(uploadedFile.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        uploadedFile.save(filepath)

        # filename stored in the Cloud Storage
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        destinationBlobName = f"{userId}+{locationId}+{timestamp}"

        url = upload_blob(BUCKET_NAME, filepath, destinationBlobName)

        cloudStorageData = {
            "url": url,
            "user_id": userId,
            "location_id": locationId,
            "blob_name": destinationBlobName,
            "timestamp": timestamp,
            "description": description
        }
        photoCollection.insert_one(cloudStorageData)

    except bson.errors.InvalidId as e:
        return jsonify({"status": 400, "message": "Invalid ID Format"}), 400
    except Exception as e:
        return repr(e)
    finally:
        files = glob.glob(app.config['UPLOAD_FOLDER'] + "/*")
        for file in files:
            os.remove(file)

    cloudStorageData["_id"] = str(cloudStorageData["_id"])
    return cloudStorageData


@app.route("/api/photo/<id>", methods=["DELETE"])
@tokenReq
def deletePhotoByObjectId(id):
    try:
        photoToDelete = photoCollection.find_one({"_id": ObjectId(id)})

        if photoToDelete is None:
            return jsonify({"status": 404, "message": "Not Found"}), 404

        delete_blob(BUCKET_NAME, photoToDelete["blob_name"])
        photoCollection.delete_one({"_id": ObjectId(id)})
    except bson.errors.InvalidId as e:
        return jsonify({"status": 400, "message": "Invalid ID Format"}), 400
    except Exception as e:
        return repr(e), 500
    return jsonify({"status": "successfully deleted", "id": id}), 200


@app.route("/api/user/<id>/photo")
@tokenReq
def getPhotoByUserId(id):
    photos = []
    for photo in photoCollection.find({"user_id": id}):
        photos.append(photo)
        photo["_id"] = str(photo["_id"])
    return json.dumps(photos)


@app.route("/api/location/<id>/photo")
@tokenReq
def getPhotoByLocationId(id):
    photos = []
    for photo in photoCollection.find({"location_id": id}):
        photos.append(photo)
        photo["_id"] = str(photo["_id"])
    return json.dumps(photos)


@app.route('/api/user/<id>')
@tokenReq
def getUserById(id):
    user = usersCollection.find_one({"_id": id})
    if user is None:
        return jsonify({"status": 404, "message": "Not Found"}), 404
    user['_id'] = str(user['_id'])
    return json.dumps(user)


@app.route('/api/user/<id>/bookmarks', methods=['PATCH', 'GET', 'DELETE'])
@tokenReq
def userBookmarks(id):
    if request.method == 'PATCH':
        newUserBookmark = request.get_json()
        if newUserBookmark != None:
            user = usersCollection.update_one(
                {"_id": id}, {"$push":  {"bookmarks":  newUserBookmark}})
            if user.matched_count == 0:
                return jsonify({"status": 404, "message": "Not Found"}), 404
            return jsonify({"status": "success", "message": "Bookmark Added"}), 200
        else:
            return jsonify({"status": "failure", "message": "No JSON was in request body"}), 400
    elif request.method == 'GET':
        bookmarks = usersCollection.find_one(
            {"_id": id}, {"_id": False, "bookmarks": True})
        if bookmarks is None:
            return jsonify({"status": 404, "message": "Not Found"}), 404
        return json.dumps(bookmarks)
    elif request.method == 'DELETE':
        deleteBookmark = request.get_json()
        if deleteBookmark != None:
            user = usersCollection.update_one(
                {"_id": id}, {"$pull": {"bookmarks":  deleteBookmark}})
            if user.matched_count == 0:
                return jsonify({"status": 404, "message": "Not Found"}), 404
            return jsonify({"status": "success", "message": "Bookmark successfuly deleted"}), 200
        else:
            return jsonify({"status": "failure", "message": "No JSON was in request body"}), 400


@app.route('/api/user/<id>/profile', methods=["PATCH", "GET"])
@tokenReq
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
