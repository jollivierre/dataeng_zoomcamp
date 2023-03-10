## Week 2 Homework

The goal of this homework is to familiarise users with workflow orchestration and observation. 


## Question 1. Load January 2020 data

Using the `etl_web_to_gcs.py` flow that loads taxi data into GCS as a guide, create a flow that loads the green taxi CSV dataset for January 2020 into GCS and run it. Look at the logs to find out how many rows the dataset has.

How many rows does that dataset have?

* 447,770
* 766,792
* 299,234
* 822,132


## Answer 1

15:35:44.264 | INFO    | Task run 'clean-b9fd7e03-0' - rows: 447770




## Question 2. Scheduling with Cron

Cron is a common scheduling specification for workflows. 

Using the flow in `etl_web_to_gcs.py`, create a deployment to run on the first of every month at 5am UTC. What’s the cron schedule for that?

- `0 5 1 * *`
- `0 0 5 1 *`
- `5 * 1 0 *`
- `* * 5 1 0`


## Answer 2

prefect deployment build  ./flows/04_homework/etl_web_to_gcs.py:etl_web_to_gcs -n "JAO Homework-etl_web_to_gcs Cron" --cron "0 5 1 * *" -a




## Question 3. Loading data to BigQuery 

Using `etl_gcs_to_bq.py` as a starting point, modify the script for extracting data from GCS and loading it into BigQuery. This new script should not fill or remove rows with missing values. (The script is really just doing the E and L parts of ETL).

The main flow should print the total number of rows processed by the script. Set the flow decorator to log the print statement.

Parametrize the entrypoint flow to accept a list of months, a year, and a taxi color. 

Make any other necessary changes to the code for it to function as required.

Create a deployment for this flow to run in a local subprocess with local flow code storage (the defaults).

Make sure you have the parquet data files for Yellow taxi data for Feb. 2019 and March 2019 loaded in GCS. Run your deployment to append this data to your BiqQuery table. How many rows did your flow code process?

- 14,851,920
- 12,282,990
- 27,235,753
- 11,338,483


## Answer 3
 prefect deployment run ParentFlow/docker-parameterized-flow --params '{"taxi_colour":"yellow", "year":2019, "months":[2,3]}'

 prefect deployment build  ./flows/04_homework/etl_gcs_to_bigquery.py:etl_parent_flow -n "JAO_Homework" -q default -a

 prefect deployment run ParentFlow_etl_gcs_to_bigquery/JAO_Homework --params '{"taxi_colour":"yellow", "year":2019, "months":[2,3]}'

18:02:52.622 | INFO    | Flow run 'idealistic-wallaby' - Rows Processed: [[14851920]]




## Question 4. Github Storage Block

Using the `web_to_gcs` script from the videos as a guide, you want to store your flow code in a GitHub repository for collaboration with your team. Prefect can look in the GitHub repo to find your flow code and read it. Create a GitHub storage block from the UI or in Python code and use that in your Deployment instead of storing your flow code locally or baking your flow code into a Docker image. 

Note that you will have to push your code to GitHub, Prefect will not push it for you.

Run your deployment in a local subprocess (the default if you don’t specify an infrastructure). Use the Green taxi data for the month of November 2020.

How many rows were processed by the script?

- 88,019
- 192,297
- 88,605
- 190,225


## Answer 4
GitHub Block URL - https://github.com/jollivierre/dataeng_zoomcamp.git

$prefect deployment build ./week_2_workflow_orchestration/week2_orchestration_jao/flows/04_homework/etl_web_to_gcs.py:etl_web_to_gcs -n JAO_Homework_GitHubBlock_ETL -sb github/jao-dataeng-github -q default -a

$prefect run etl-web-to-gcs/JAO_Homework_GitHubBlock_ETL

JAO_Notifications
APP  12:15 AM
Prefect flow run notification
Flow run etl-web-to-gcs/unique-urchin entered state Completed at 2023-02-06T00:15:38.248230+00:00.
Flow ID: 6a172f70-52ad-4eba-a338-f69beb605d24
Flow run ID: f3a78ac9-7c6c-4e52-a445-825ce3a0f80e
Flow run URL: http://127.0.0.1:4200/flow-runs/flow-run/f3a78ac9-7c6c-4e52-a445-825ce3a0f80e
State message: All states completed.
Prefect Notifications | Today at 12:15 AM

23:13:44.471 | INFO    | Task run 'clean-2c6af9f6-0' - rows: 88605




## Question 5. Email or Slack notifications

Q5. It’s often helpful to be notified when something with your dataflow doesn’t work as planned. Choose one of the options below for creating email or slack notifications.

The hosted Prefect Cloud lets you avoid running your own server and has Automations that allow you to get notifications when certain events occur or don’t occur. 

Create a free forever Prefect Cloud account at app.prefect.cloud and connect your workspace to it following the steps in the UI when you sign up. 

Set up an Automation that will send yourself an email when a flow run completes. Run the deployment used in Q4 for the Green taxi data for April 2019. Check your email to see the notification.

Alternatively, use a Prefect Cloud Automation or a self-hosted Orion server Notification to get notifications in a Slack workspace via an incoming webhook. 

Join my temporary Slack workspace with [this link](https://join.slack.com/t/temp-notify/shared_invite/zt-1odklt4wh-hH~b89HN8MjMrPGEaOlxIw). 400 people can use this link and it expires in 90 days. 

In the Prefect Cloud UI create an [Automation](https://docs.prefect.io/ui/automations) or in the Prefect Orion UI create a [Notification](https://docs.prefect.io/ui/notifications/) to send a Slack message when a flow run enters a Completed state. Here is the Webhook URL to use: https://hooks.slack.com/services/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

Test the functionality.

Alternatively, you can grab the webhook URL from your own Slack workspace and Slack App that you create. 


How many rows were processed by the script?

- `125,268`
- `377,922`
- `728,390`
- `514,392`


## Answer 5

app.prefect.cloud - did not understand how to show my deployments here. more reading!!

https://api.slack.com/messaging/webhooks - followed instructions here



23:42:19.359 | INFO    | Task run 'clean-2c6af9f6-0' - rows: 514392





## Question 6. Secrets

Prefect Secret blocks provide secure, encrypted storage in the database and obfuscation in the UI. Create a secret block in the UI that stores a fake 10-digit password to connect to a third-party service. Once you’ve created your block in the UI, how many characters are shown as asterisks (*) on the next page of the UI?

- 5
- 6
- 8
- 10


## Answer 6

8



## Submitting the solutions

* Form for submitting: https://forms.gle/PY8mBEGXJ1RvmTM97
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 6 February (Monday), 22:00 CET


## Solution

We will publish the solution here
