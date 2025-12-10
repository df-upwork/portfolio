# How to setup a data pipeline in Microsoft Azure Data Factory v2?
## Step 1
Create «**Linked Services**» for the data source and the sink («**Manage**» → «**Linked Services**»).
## Step 2
Specify the **authentication method** (e.g., Managed Identity, Service Principal, SQL Authentication, etc.).
## Step 3
If your data source or sink is **on-premises** or behind a **firewall**, it is necessary to:
3.1) Install and configure the **Self-Hosted Integration Runtime** (**SHIR**).
3.2) Configure **network rules** or additional certificates to ensure a secure connection.
## Step 4
Create **datasets** for each source and sink.
I recommend configuring these as **parameterised** (to specify file paths, table names, and other variables in a flexible way).
## Step 5
Create a pipeline («**Author**» → «**+**» → «**Pipeline**»).
## Step 6
Add «**Activities**» such as «**Copy Data**» or «**Mapping Data Flow**» to the pipeline (if transformation is required).
To use «Mapping Data Flow», it is necessary to enable Data Flow support in the Integration Runtime («Manage» → «Integration runtimes»).
## Step 7
Configure the **input** and **output** **dataset** for the pipeline, specifying:
7.1) The source (e.g., Azure SQL Database Dataset, REST API, Amazon S3, or an on-premises database via SHIR).
7.2) The sink (e.g., Azure Blob Storage Dataset, Data Lake Storage, or any other of the 90+ supported connections).
## Step 8
In the «**Settings**» section for «**Copy Data**», specify the copy parameters (method, parallelism, behavior on errors).
## Step 9
If necessary, add other «Activities» (e.g., «**Lookup**», «**Stored Procedure**», «**Script**», «**Databricks Notebook**», «**Web Activity**», «**Execute Pipeline**», «**ForEach**», etc.), according to the needs of the project.
## Step 10
When working with recurring copy or transformation templates, or when it is necessary to flexibly change table names and file paths, **pipeline parameters**, **dataset parameters** and **dynamic content expressions** can be used.
## Step 11
Test the pipeline:
11.1) Click on «**Debug**» at the top of the screen to run the pipeline in debug mode.
11.2) Check the execution log in «**Output**» or go to «**Monitor**» → «**Pipeline runs**».
## Step 12
Add «*Triggers*» for automatic execution.
## Step 13
Connect a **Git repository** (Azure DevOps or GitHub) for version control and collaborative development (if not already done).
This will make it easier for your developer (when he recovers) to track changes made to ADF during his illness, and will also allow the use of CI/CD processes when moving pipelines between environments.
## Step 14
**Publish** all changes.
If it is planned to move solutions between multiple environments (Dev, Test, Prod) or to parameterise ADF objects on a large scale, it is recommended to use an **automated deployment approach** (**ARM templates** or **Bicep**) together with **CI/CD** (e.g., **Azure DevOps** or **GitHub Actions**).
This will simplify the transfer and update of your pipeline, datasets, and linked services across different environments without manual duplication.
## Step 15
Configure monitoring and alerts.
In the «**Monitor**» section, it is possible to use built-in alert rules and metrics (via **Azure Monitor**) to automatically track the state of pipelines and receive notifications (via email, SMS, etc.) in the event of failures or deviations from normal operation.