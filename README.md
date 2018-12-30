# orlando-shuttle-api

RESTful API created with the goal to unify all major shuttle data in the Orlando area into one centralized web service.

## Root URL
All API calls start with the root URL:

https://orlando-shuttle-api.herokuapp.com/

#### Output Format

All output will be returned in JSON format.

### GET all shuttle information
send a GET request to

```
https://orlando-shuttle-api.herokuapp.com/api/shuttle/
```

### GET shuttle by name
send a GET request to

```
http://localhost:8080/api/shuttle/name/(name here)
```

*example:*
```
http://localhost:8080/api/shuttle/name/route13
```

### GET shuttle by id
send a GET request to

```
http://localhost:8080/api/shuttle/id/(id here)
```

*example:*
```
http://localhost:8080/api/shuttle/id/1
```