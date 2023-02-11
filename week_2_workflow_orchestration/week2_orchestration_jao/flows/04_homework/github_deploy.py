
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


#prefect deployment build week_2_workflow_orchestration/week2_orchestration_jao/flows/04_homework/etl_web_to_gcs.py:etl_web_to_gcs -n "JAO_Homework_GitHubBlock_ETL" -sb github/jao-dataeng-github -q default -a


#prefect deployment build -n "JAO_Homework_GitHubBlock_ETL" -sb github/jao-dataeng-github ./week_2_workflow_orchestration/week2_orchestration_jao/flows/04_homework/etl_web_to_gcs.py:etl_web_to_gcs -q default -a

#build the deployment from CLI:
#prefect deployment build -n etl_github -sb github/github-prefect-storage  ./path/to/your_flow/etl_web_to_gcs.py:etl_web_to_gcs
#so when you specify github block for storage (-sb), your path to flow is not local path but path from the root of your repo. As simple as that (e