
from prefect.deployments import Deployment
from prefect.infrastructure.docker import DockerGitHub
from etl_web_to_gcs import etl_web_to_gcs


docker_block = DockerGitHub.load("jao-dataeng-github")

# make an instance
docker_deploys = Deployment.build_from_flow(
    flow=etl_web_to_gcs, 
    name="docker-etl_web_to_gcs-github-flow",
    infrastructure=docker_block
)


# apply instance.   deployment will appear in UI
#main method
if __name__ == '__main__':
    docker_deploys.apply()



# run on command line using $python <path_to>/docker_deploy.py


#prefect deployment build ./flows/03_parameterization/etl_web_to_gcs_parameterized.py:etl_parent_flow -n "JAO Parameterized ETL Cron and Params" --cron "0 0 * * *"  --params='{"taxi_colour": "yellow", "year": 2021, "months": [1,2,3]}' -a
