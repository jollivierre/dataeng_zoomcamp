#image to be based on
FROM python:3.9

#wget
RUN apt-get install wget

#install packages inside container and create new image
RUN pip install pandas sqlalchemy psycopg2-binary

#specifying a directory to copy file.  *directory will be created and navigated to same.
WORKDIR /app

#copy file into directory (source/destination) (same name in this case)
COPY ingest_csv_data_to_postgres.py ingest_csv_data_to_postgres.py		

#start docker image with bash prompt
ENTRYPOINT [ "python", "ingest_csv_data_to_postgres.py" ]
