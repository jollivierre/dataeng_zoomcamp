prefect deployment 

use a prefect deployment used to trigger and schedule flow runs to stop running manually

a deployment in prefect is a server side concept that encaapsulates a flow allowing it to be scheduled and trigger via the API


--build a deployment -- flow_name used especially if more than one flow defined
prefect deployment build {path/file_name}:{flow_name} -n "Deployment Name"

e.g.

$prefect deployment build  ./flows/03_parameterization/etl_web_to_gcs_parameterized.py:etl_parent_flow -n "JAO Parameterized ETL"


parameters was empty, so added in  yaml file (etl_parent_flow-deployment.yaml created after deployment command) from main method

parameters: {"taxi_colour": "yellow", "year": 2021, "months": [1,2,3]}


then need to apply deployment using yaml file.  this will send metadata over to API
$prefect deployment apply etl_parent_flow-deployment.yaml      #should have created in current folder


/**** message returned
Successfully loaded 'JAO Parameterized ETL'
Deployment 'ParentFlow/JAO Parameterized ETL' successfully created with id '8014ea93-bda7-41ac-9204-8c97dd130696'.
View Deployment in UI: http://127.0.0.1:4200/deployments/deployment/8014ea93-bda7-41ac-9204-8c97dd130696

To execute flow runs from this deployment, start an agent that pulls work from the 'default' work queue:
$ prefect agent start -q 'default'
*****/


**In API
Quick Run - uses the set parameters
Custom Run - user can set parameters for each run


*** message above "prefect agent start -q 'default'"
for a prefect deployment to run it needs an agent from workqueue to run.
an agent is a lightweight python process in prefect that live in the execution environment
and agent is pulled from a workqueue

prefect agent start  --work-queue "default"         # command copied from API under Wokqueues and "default" agent


**the deployment that was queued should kick-off immediately



--Notifications can now be setup in UI
States - run state (Running, Failed, etc)
Tag - 
Type of hook - where tosend notification



--building deployment with cron job  (every day at 12AM) -- (the "-a" is to apply)
prefect deployment build ./flows/03_parameterization/etl_web_to_gcs_parameterized.py:etl_parent_flow -n "JAO Parameterized ETL Cron" --cron "0 0 * * *" -a



--to get help on a command.  in this case, the options that can be inccluded after "build"
prefect deployment build --help


prefect deployment build ./flows/03_parameterization/etl_web_to_gcs_parameterized.py:etl_parent_flow -n "JAO Parameterized ETL Cron and Params" --cron "0 0 * * *"  --params='{"taxi_colour": "yellow", "year": 2021, "months": [1,2,3]}' -a





------------------------------------------------------------------------------------------------
--code to be stored in a docker image on docker hub and run from there

1. create a Dockerfile
2. created a new requirements file 
3. removed prefect as it is part of image
4. completed details for Dockerfile
5. build docker image --> docker image build -t <docker_login><image_name> .

e.g.
$docker image build -t jollie/prefect_jao:dataeng_jao .

6. push image to docker hub

e.g. -- if not logeed in then run --> $docker login  ***research
$docker image push jollie/prefect_jao:dataeng_jao



*** create docker  block in prefect example
week_2_workflow_orchestration/week2_orchestration_jao/blocks/make_docker_block.py



7.  need to create deployment file.  using a file instead of command.  deployment will appear in UI


8. run $python <path_to>/docker_deploy.py


9. show profile prefect using.  default proflie comes automatically when installed
$prefect profile ls

10. ran the following to set link to IP .  seem to remember this being run alreeady
 prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api


11.  fire up an agent ("$prefect orion start" would have been kicked off )

prefect agent start -q default


12.  run deployment - -from UI or command line just for months 1 and 2
$prefect deployment run ParentFlow/docker-parameterized-flow -p "months=[1,2]"



--got an Error

ValueError: Path /home/jasono/.prefect/storage/03d58a1aa33e4247bff4c8dfc4a6efea does not exist.

removed ", cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1)" from task decorator in script


--other error 

RuntimeError: Unable to load 'dataeng-gcs-jao' of block type None due to failed validation. To load without validation, try loading again with `validate=False`.
18:50:31.209 | ERROR   | Flow run 'functional-koala' - Finished in state Failed('Flow run encountered an exception. Traceback (most recent call last):\n  File "/usr/local/lib/python3.9/site-packages/prefect/blocks/core.py", line 696, in load\n    return cls._from_block_document(block_document)\n  File "/usr/local/lib/python3.9/site-packages/prefect/blocks/core.py", line 551, in _from_block_document\n    block = block_cls.parse_obj(block_document.data)\n  File "pydantic/main.py", line 527, in pydantic.main.BaseModel.parse_obj\n  File "/usr/local/lib/python3.9/site-packages/prefect/blocks/core.py", line 183, in __init__\n    super().__init__(*args, **kwargs)\n  File "pydantic/main.py", line 342, in pydantic.main.BaseModel.__init__\npydantic.error_wrappers.ValidationError: 1 validation error for GcsBucket\ngcp_credentials -> service_account_file\n  The provided path to the service account is invalid (type=value_error)\n\nThe above exception was the direct cause of the following exception:\n\nRuntimeError: Unable to load \'dataeng-gcs-jao\' of block type None due to failed validation. To load without validation, try loading again with `validate=False`.\n')

In the the error message, almost to the end, there is a line that states " The provided path to the service account is invalid".  
When I created my "GCP Credentials" block in Prefect UI, I used the option "Service Account File" and specified the path (/home/user/.gcp/xxxx.json).
I removed this from the block and pasted the .json file into the option "Service Account Info". Flow then worked for me.




---to start
start vm on gcp
update ssh config
conda activate orchestration_jao (each app)

echo $GOOGLE_APPLICATION_CREDENTIALS
export GOOGLE_APPLICATION_CREDENTIALS=~/.gcp/ny-rides-share-jao-de-user.json
gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS

run terraform (projectid - ny-rides-share-jao)

prefect orion start
prefect agent start -q "default"
python flows/03_parameterization/docker_deploy.py       # is the flow is not deployed or to redeploy
prefect deployment run ParentFlow/docker-parameterized-flow -p "months=[1,2]"



