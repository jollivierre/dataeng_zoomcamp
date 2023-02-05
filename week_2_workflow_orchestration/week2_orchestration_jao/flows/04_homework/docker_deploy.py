
from prefect.deployments import Deployment
from prefect.filesystems import GitHub
from etl_web_to_gcs import etl_web_to_gcs

github_block = GitHub.load("jao-dataeng-github")

# make an instance
github_deploys = Deployment.build_from_flow(
    flow=etl_web_to_gcs, 
    name="github-etl_web_to_gcs-flow",
    infrastructure=github_block
)


# apply instance.   deployment will appear in UI
#main method
if __name__ == '__main__':
    github_deploys.apply()



# run on command line using $python <path_to>/docker_deploy.py


#prefect deployment build ./flows/04_homework/etl_web_to_gcs.py:etl_web_to_gcs -n "JAO_Homework_GitHubBlock_ETL" -sb github/jao-dataeng-github -q default -a