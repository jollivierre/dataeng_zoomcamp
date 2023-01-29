services:
  pgdatabase:
    image: postgres:13
    environment:
      - POSTGRES_USER=root
      - POSTGRES_PASSWORD=root
      - POSTGRES_DB=ny_taxi
    volumes:
      - "./data/ny_taxi_postgres_data:/var/lib/postgresql/data:rw"
    ports:
      - "5432:5432"
  pgadmin:
    image: dpage/pgadmin4
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@admin.com
      - PGADMIN_DEFAULT_PASSWORD=root
    ports:
      - "8080:80"


      #create network
docker network create postgres-network

# run docker image cmd line database
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/data/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=postgres-network \
  --name postgres-database \
  postgres:13





  # run docker image web interface
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v $(pwd)/data/pgadmin_data:/var/lib/pgadmin \
  -p 8080:80 \
  --network=postgres-network \
  --name postgres-pgadmin \
  dpage/pgadmin4



URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

python ingest_csv_data_to_postgres.py \
  --username=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --database=ny_taxi \
  --tablename=yellow_taxi_data \
  --csv_url=${URL}



  docker build -t jao_taxi_data_ingest:v002 .


URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

docker run -it \
  --network=postgres-network \
  jao_taxi_data_ingest:v002 \
    --username=root \
    --password=root \
    --host=postgres-database \
    --port=5432 \
    --database=ny_taxi \
    --tablename=yellow_taxi_data \
    --csv_url=${URL}


#home work
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz"

docker run -it \
  --network=postgres-network \
  jao_taxi_data_ingest:v002 \
    --username=root \
    --password=root \
    --host=postgres-database \
    --port=5432 \
    --database=ny_taxi \
    --tablename=green_taxi_data \
    --csv_url=${URL}


  URL="https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv"
   