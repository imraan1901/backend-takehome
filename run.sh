# Start the containers detached
docker compose up --build -d
sleep 1

# Send the ETL execute command and get the results
curl  http://127.0.0.1:8080/data -X POST
curl  http://127.0.0.1:8080/data -X GET

# Kill the containers
API_ID=$(docker ps -aqf "name=processor-rest-api")
DB_ID=$(docker ps -aqf "name=postgres_db")
docker kill $API_ID $DB_ID

