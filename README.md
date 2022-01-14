# E-Mina Backend API Endpoints Documentation

### / - root path

Result: You reached backend server for E-Mina

Parameter: None

### POST /api/auth

Result:

Parameter:

### GET /api/media

Result: Return all media results

Parameter: None

Example:

```bash
{URL}/api/media
```

### GET /api/locations

Result: Return all location results

Parameter: None

Example:

```bash
{URL}/api/locations
```

### GET /api/locations/<id>

Result: Return detailed information about specific location

Parameter: locationId

Example:

### GET /api/media/<id>

Result: Return detailed information about specific media

Parameter: mediaId

Example:

### GET /api/media/<id>/locations

Result: Return all locations of given media

Parameter: mediaId

Example:

### POST /api/user/<userId>/location/<locationId>/photo

Result: Return all locations of given media

Parameter: mediaId and locationId

Example:

### DELETE /api/photo/<id>

Result: Delete photo information from database and Cloud storage

Parameter: id (photoId)

Example:

### GET /api/user/<id>

Result: Return user information given userId

Parameter: id (userId)

Example:

### GET /api/user/<id>/photo

Result: Return all photo information given userId

Parameter: id (photoId)

Example:

### GET /api/location/<id>/photo

Result: Return all photo of specific location given id

Parameter: id (locationId)

Example:

### GET /api/user/<id>

Result: Return all users given id

RParameter: id (userId)

Example:

### GET | PATCH | DELETE /api/user/<id>/bookmarks

GET

Result: Return all saved locations (bookmarks) of given user

Parameter: id (userID)

Example:

PATCH

Result:

Parameter: id (userID)

Example:

DELETE

Result:

Parameter: id (userID)

Example:

### GET | PATCH /api/user/<id>/profile

GET

Result:

Parameter:

PATCH

Result:

Parameter:
