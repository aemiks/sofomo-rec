'api/token/', 
'api/token/refresh/'
'api/get_user_geolocation_data'
'api/geolocations'   


## Sofomo-rec
This is an API that requires JWT authentication. The application is able to store 
geolocation data in a database based on the IP address(data retrieved using ipstack.com). The IP address can be provided
via the POST method or retrieved from the user at a specific endpoint.  

API is avaiable online:  [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html)

```
to test API online authorization values: 
username= testuser 
password= user12345
```

## Table of contents
* [Getting Started](#getting-started)
* [Default Endpoints](#default-endpoints)  
* [JWT Authorization](#jwt-authorization)


## Getting Started 

To start project locally

clone respiratory from github:
```
$ git clone https://github.com/aemiks/sofomo-rec.git

```
When the cloning is successful, I recommend using ```virtualenv```
```
$ cd sofomo-rec

$ python -m venv venv

for unix users:
$ source venv/bin/activate

for windows users:
$ source venv/Scripts/activate

$ pip install -r requirements.txt

```

To launch project:
```
$ python manage.py migrate
$ python manage.py runserver
```
To create super user:
```
$ python manage.py createsuperuser
```
## Default Endpoints
```
To retrive JWT token
    localhost:8000/api/token/   

To refresh JWT token
    localhost:8000/api/token/refresh/ 

Use GET retrieve gelocation data from your ip
    localhost:8000/api/get_user_geolocation_data

ViewSet that allow to list, create and destroy data 
    localhost:8000/api/geolocations
    to add new object:
        -X POST \
        -H "Authorization: Bearer xxxxx.yyyyy.zzzzz" \
        -b {'ip':'127.0.0.1'} \ 
```

## JWT Authorization

I have chosen SimpleJWT package for JWT authorization

You can find documentation here:  [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html)

Usage: 
```
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "user12345"}' \
  http://localhost:8000/api/token/
...
You will receive:
{
  "access":"xxxxx.yyyyy.zzzzz",
  "refresh":"aaaaa.bbbbb.ccccc"
}
```
You can use the returned access token to prove authentication for a protected view:
```
curl \
  -H "Authorization: Bearer xxxxx.yyyyy.zzzzz" \
  http://localhost:8000/api/geolocations/
```


enjoy.