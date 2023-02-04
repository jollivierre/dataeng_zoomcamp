#image to be based on
FROM prefecthq/prefect:2.7.7-python3.9

#copy requirements file in.  a copy was made of the manual requirements.txt and apps remvoed already installed on docker image
COPY docker_requirements.txt .

#install packages inside container and create new image
RUN pip install -r docker_requirements.txt --trusted-host pypi.python.org --no-cache-dir


#copy file into directory (source/destination) (same name in this case)
COPY flows /opt/prefect/flows
COPY data /opt/prefect/data

#no entrypoint???/
#ENTRYPOINT [ "python", "etl_web_to_gcs_parameterized.py" ]
