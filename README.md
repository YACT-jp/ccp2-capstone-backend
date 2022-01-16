# E-Mina Backend API Endpoints Documentation

### / - root path

Parameter: None

Result: You reached backend server for E-Mina

### POST /api/auth

Parameter: JSON in request body with following format

Result: 

```json
{
	"_id":"<userId>",
	"email":"<email>"
}
```

Successful response:

```json
{
    "data": {
        "token": "<user token>",
        "user": {
            "_id": "<MongoDB ID>",
            "bio": "<Biography>",
            "bookmarks": "[array of location bookmark]",
            "email": "<user email>",
            "user_content": [],
            "user_id": "<user email>",
            "username": "<username>"
        }
    },
    "message": "user authenticated",
    "status": "successful"
}
```

Unsuccessful response:

```json
{
    "data": {},
    "message": "invalid login details",
    "status": "fail"
}
```

### GET /api/media

Parameter: None

Result: Return all media results 

Example:

```bash
{URL}/api/media
```

Successful response (Excerpt):

```json
[
   {
      "id":"<id>",
      "name":"Death Note",
      "overview":"Light Yagami is an ace student with great prospects\u2014and he\u2019s
bored out of his mind. But all that changes when he finds the Death Note, a notebook dropped by a rogue Shinigami death
god. Any human whose name is written in the notebook dies, and Light has vowed to use the power of the Death Note to rid
the world of evil. But will Light succeed in his noble goal, or will the Death Note turn him into the very thing he
fights against?",
      "poster_path":"<URL of image>"
   }
]
```

### GET /api/locations

Parameter: None

Result: Return all location results 

Example: 

```bash
{URL}/api/locations
```

Successful response (Excerpt with some example):

```json
[
   {
      "_id":"<location ID>",
      "coordinates":"{latitude: 35.6852600, longitude: 139.7299368}",
      "description":"Taki has a date with Miki and the meeting point is outside Yotsuya station.",
      "media_id":[
         "<media ID>"
      ],
      "name":"Yotsuya Station",
      "plus_code":"MPPH+4QH Shinjuku City, Tokyo",
      "address":"1 Chome Yotsuya, Shinjuku City, Tokyo 160-0004",
      "media_pic":[
         "<URL to specific scene of this location of given media>"
      ],
      "loc_pics":[
         "<URL actual picture of this lcoation>"
      ],
      "media_name":"<Name of media>",
      "location_pic":"<URL to overview picture of this location>"
   }
]
```

### GET /api/locations/<id>

Parameter: locationId

Result: Return detailed information about specific location

Example: 

### GET /api/media/<id>

Parameter: mediaId

Result: Return detailed information about specific media 

Example: 

### GET /api/media/<id>/locations

Parameter: mediaId

Result: Return all locations of given media

Example: 

### POST /api/user/<userId>/location/<locationId>/photo

Parameter: mediaId and locationId

Result: Return all locations of given media

Example: 

### DELETE /api/photo/<id>

Parameter: id (photoId)

Result: Delete photo information from database and Cloud storage

Example: 

### GET /api/user/<id>

Parameter: id (userId)

Result: Return user information given userId

Example: 

### GET /api/user/<id>/photo

Parameter: id (photoId)

Result: Return all photo information given userId

Example: 

### GET /api/location/<id>/photo

Parameter: id (locationId)

Result: Return all photo of specific location given id

Example: 

### GET /api/user/<id>

RParameter: id (userId)

Result: Return all users given id 

Example: 

### GET | PATCH | DELETE /api/user/<id>/bookmarks

GET

Parameter: id (userID)

Result: Return all saved locations (bookmarks) of given user

Example: 

PATCH

Parameter: id (userID)

Result: 

Example: 

DELETE 

Parameter: id (userID)

Result:

Example: 

### GET | PATCH /api/user/<id>/profile

GET 

Parameter:

Result:

PATCH 

Parameter:

Result:
