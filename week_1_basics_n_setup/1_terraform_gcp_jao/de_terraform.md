Creating two resources in google environment (GCP):

1) Google Cloud Storage (GCS): Data Lake (as referred to in course)

2) BigQuery: Data Warehouse (classic data warehouse concepts like facts and dimensions)


--steps
1. create storage service account
2. download json and save to folder
3. export GOOGLE_APPLICATION_CREDENTIALS=~/.gcp/ny-rides-share-jao-de-user.json
4. gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
5. add roles
6. ensure APIs enabled
    - https://console.cloud.google.com/apis/library/iam.googleapis.com
    - https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com



--if folder empty
- create folder "terraform"
- add file ".terraform-version" and update with app version
- create main.tf file
    - terraform resource
    - plugins to interact with cloud providers
    - get predefined google sorage bucket



--terraform commands
# ********* Project ID: ny-rides-share-jao ******************

# Refresh service-account's auth-token for this session
export GOOGLE_APPLICATION_CREDENTIALS=~/.gcp/ny-rides-share-jao-de-user.json
gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS

# Initialize state file (.tfstate)
terraform init

# Check changes to new infra plan
terraform plan -var="project=<your-gcp-project-id>"

# Create new infra
terraform apply -var="project=<your-gcp-project-id>"

# Delete infra after your work, to avoid costs on any running services
terraform destroy

