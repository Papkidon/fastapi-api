# Simple API using FastAPI

## Stack

|  | |
| --- | --- |
| Language  | Python  |
| Framework  | FastAPI  |
| ORM | SQLAlchemy |
| Data validator | Pydantic |
| Database | PostgreSQL |
| Testing | Pytest 

## Services

* <b>download_cars_service</b>
  * is responsible for downloading data from Mockachino API.
    * localhost:8080/api/v1/download/docs/
* <b>store_cars_service</b>
  * is responsible for storing data in the database.
    * localhost:8080/api/v1/store/docs/
* <b>query_cars_service</b>
  * is responsible for sending prepared statements to the database.
    * localhost:8080/api/v1/query/docs/
* <b>combined_cars_service</b>
  * is responsible for downloading, storing data, calculating averages and storing them.
    * localhost:8080/api/v1/combined/docs/
    
## Build and create containers

`cd` into project folder and run `docker-compose up -d --build` or `docker compose up`

## Routing

Services are redirected to port 8080 via Nginx Reverse Proxy.

## Authorization

Project contains simple authorization via API Key, which is transferred in header "Authorization". Every service has its own key stored as environmental
variable. In this case every service has the same key of value `123`.

## Testing

Every service has included tests, which can be executed by running command `docker exec -it *container_name* pytest`
