### Start with python ###

- cd services 
- cd flask
- pip install -r requirements.txt
- Start gunicorn server main:app

smoke test - 
curl --location 'http://localhost:8000/message' \
--header 'accept: application/json' \
--header 'Content-Type: application/json' \
--data '{
    "message":"ping"
}'


### Start with Docker ###

- download docker
- docker compose up --build

smoke test -
curl --location 'http://localhost:8000/message' \
--header 'accept: application/json' \
--header 'Content-Type: application/json' \
--data '{
    "message":"ping"
}'

### ENV FILE ###
OPENAI_API_KEY = enter openai key
MYSQL_HOST = mysql host
MYSQL_USER = user
MYSQL_PASSWORD = password
MYSQL_ROOT_PASSWORD= password
MYSQL_DB = database name

