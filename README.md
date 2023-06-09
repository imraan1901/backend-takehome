# Backend Engineering Take-Home Challenge

## ---------- My Implementation ----------


## Tools
* Docker Desktop 4.20.1 or Docker Engine, Docker CLI, and Docker Compose plugin (https://docs.docker.com/compose/install/)
* Python 3.9 if running local python script (https://www.python.org/downloads/release/python-390/)

## How to run
1) Type "docker compose up --build" to start the postgres database and the api respectively.
2) Type "curl  http://127.0.0.1:8080/data -X POST" in ANOTHER terminal to trigger the ETL process.
3) Type "curl  http://127.0.0.1:8080/data -X GET" in the same terminal as step 2 to get the processed data from the database in JSON format.

## Alternatively you can run a shell script 
1) Type "chmod +x run.sh" to give the script executable permissions
2) Type "./run.sh" to run the demo

## Alternatively you can run a python script 
1) Type "python run.py" to start the database and the api respectively.


## DEMO VIDEO
[![Demo of the API](http://img.youtube.com/vi/gwuh00BkjU4/0.jpg)](https://www.youtube.com/watch?v=gwuh00BkjU4 "Backend Take-home Demo")

## ---------- End My Implementation ----------


## CHALLENGE DETAILS BELOW


### Introduction
In this challenge, you will be tasked with creating a simple ETL pipeline that can be triggered via an API call. You will be provided with a set of CSV files that you will need to process, derive some features from, and then upload into a database table.

### Requirements
- Python 3.7+
- Docker
- PostgreSQL

### Challenge
1.  Create a Dockerized application that can be started with a single `docker run` command.

2. The application should expose an API endpoint that triggers an ETL process.

3. The ETL process should:
- Load CSV files from the given data directory.
 - Process these files to derive some simple features.
 - Upload the processed data into a **postgres** table.

4.  The application should be built using Python and any tooling you like for coordinating the workflow and fronting the api server

### Data
You will find three CSV files in the `data`  directory:

- `users.csv`: Contains user data with the following columns: `user_id`, `name`, `email`,`signup_date`.

- `user_experiments.csv`: Contains experiment data with the following columns: `experiment_id`, `user_id`, `experiment_compound_ids`, `experiment_run_time`. The `experiment_compound_ids` column contains a semicolon-separated list of compound IDs.


- `compounds.csv`: Contains compound data with the following columns: `compound_id`, `compound_name`, `compound_structure`.


## Feature Derivation
From the provided CSV files, derive the following features:

1. Total experiments a user ran.
2. Average experiments amount per user.
3. User's most commonly experimented compound.

## Deliverables
Please provide the following in a GITHUB REPOSITORY.

1. A Dockerfile that sets up the environment for your application.
2. A requirements.txt file with all the Python dependencies.
3. A Python script that sets up the API and the ETL process.
4. A brief README explaining how to build and run your application, and how to trigger the ETL process.


Please also provide a script that builds, and runs the docker container. 
You should also provide a script that scaffolds how a user can run the ETL process. This can be `curl` or something else.
Finally, provide a script that queries the database and showcases that it has been populated with the desired features.


## Evaluation
Your solution will be evaluated on the following criteria:

Code quality and organization.
Proper use of Python and Docker.
Successful execution of the ETL process.
Accuracy of the derived features.
