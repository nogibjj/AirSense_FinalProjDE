# AirSense - Insights of Flights
[![Install](https://github.com/nogibjj/airsense/actions/workflows/install.yml/badge.svg)](https://github.com/nogibjj/airsense/actions/workflows/install.yml)
[![Lint](https://github.com/nogibjj/airsense/actions/workflows/lint.yml/badge.svg)](https://github.com/nogibjj/airsense/actions/workflows/lint.yml)
[![Format](https://github.com/nogibjj/airsense/actions/workflows/format.yml/badge.svg)](https://github.com/nogibjj/airsense/actions/workflows/format.yml)
[![Test](https://github.com/nogibjj/airsense/actions/workflows/test.yml/badge.svg)](https://github.com/nogibjj/airsense/actions/workflows/test.yml)

## [YouTube Demo Video](https://youtu.be/FHHl5CH5i4w)

## Team Members:
- Jamie Liu
- Xianjing Huang
- Yijia Zhao

## Get Started

`docker compose up --build`

## System Design

### Microservices Overview

- `AirGateway` and `AirConnector` are containerized using Docker and run within AWS App Runner.
- `AirBroker` leverages Databricks to preprocess data and generate final data tables.
- `AirStore` is a GraphSQL database running on AWS RDS Aurora, designed to store and maintain all flight-related data.

These services work together to form a stable and efficient microservices application.

### Diagram

![AirSense-design](/airsense_diagram.png)

## Services
The application is deployed on AWS App Runner 
and can be accessed using the following link:

[https://watgt5vczp.us-east-2.awsapprunner.com](https://watgt5vczp.us-east-2.awsapprunner.com)

![runner](/imgs/appRunner.png)

### AirGateway

`AirGateway` is powered by Flask and aims to handle users' and administrators' restful API requests and forward them to proper mircro-services (`AirConnector`, `AirStore`). It has the ability to handle at least 10,000 requests per seconds.

- Test connectivity with `AirConnector`: `curl [host_uri]/connector`
- Test query: `/api/dynamic_query?table_name=busiest_airports_by_delays&limit=6&where=Avg_Departure_Delay:87,Total_Arrivals:4`

### AirBroker

`AirBroker` leverages databricks to preprocess data and generate final data tables that will be ready use for `AirGateway`.

### AirConnector

`AirConnector` connectes `AirBroker` and `AirStore`. It transfers data tables from databricks to `AirStore` and ready for query by `AirGateway`.

- To transfer: `curl -X POST "[host_uri]:8000/transfer_table?table_name=delays_by_day"`

### AirStore

`AirStore` is a GraphSQL database running on AWS RDS `Aurora` that aims to store and maintain all flights related data and ready for use by other services.

- For developer: view and manage [AWS Aurora Database](https://us-east-1.console.aws.amazon.com/rds/home?region=us-east-1#database:id=airsense-pg;is-cluster=true)

## Development

### Repo Structure (demo only)

```
AirSense/
├── README.md
├── .gitignore
├── docker-compose.yml
├── requirements.txt
├── shared/
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   ├── config.py
│   ├── tests/
├── services/
│   ├── gateway/     # API Gateway microservice
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── config.py
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── tests/
│   │       ├── test_routes.py
│   └── connector/
│       ├── main.py
│       ├── Dockerfile
│       ├── requirements.txt
│       └── tests/
│           ├── test_connector.py
├── tools/
│   ├── .keep
└── scripts/
    ├── start_all.sh
    ├── deploy.sh

```

### Docker

**Attn: If develope under docker, you dont have to use any python virtual environment mentioned below, as each image has its own environment in docker engine, which is highly recommened.**

- Instructions for set up [Docker Engine](https://docs.docker.com/engine/install/) and [Desktop](https://docs.docker.com/desktop/).

```bash
docker compose build
docker compose up
```

#### Container Registry--AWS ECR
The Docker image is hosted on AWS ECR. 
AWS Elastic Container Registry (ECR) is a fully managed container registry service provided by AWS. 
It allows to store, manage, and deploy container images securely.

![ECR](/imgs/ECR.png)

### Python

**Attn: If you would like to test functions locally, please follow instructions below.**

- _please use Python3 version `3.12.8` and usage of `pyenv` and virtual environment is highly recommended._

#### Install Python using Pyenv [https://github.com/pyenv/pyenv](https://github.com/pyenv/pyenv)

```bash
pyenv install 3.12.8
pyenv global 3.12.8
# restart terminal if necessary
which python3 # /home/[username]/.pyenv/shims/python3
python3 -V # Python 3.12.8
```

##### Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
which python3 # [repo_name]/services/venv/bin/python3
```

##### Install Libraries

```bash
pip install --no-cache-dir -r requirements.txt
```

##### Run

```python3
python3 shared/tests/connect_aws_rds.py
```

### Logging
We use AWS CloudWatch for logging. AWS CloudWatch is a 
monitoring and observability service provided by AWS. 
It helps track the performance and health of AWS resources and applications.

<img src="/imgs/log01.png" alt="1" style="width:600px;">

## Load Test - Quantitative Assessment
We use **Locust** test to load test for our Flask app. 
This is a useful platform for testing web application. 
It helps us assess how our web application handles increased requests. 
The code for running Locust test in stored in `locustfile.py`. 
To run this, use `pip install locust` to install locust on codespace or local machine. 
Then run locust command to run the web version locust test. 
This can be used within the link provided by running the command.

We use AWS app runner for auto-scaling which automatically scale up based on the amount of user requests. 
- Concurrency: 100 requests per instance
- Instance Size: 1-25 instances
- Virtual CPU & memory: 1 vCPU & 2 GB

**1000 users, spawn-rate 50**:

<img src="/imgs/load01.png" alt="1" style="width:600px;">

<img src="/imgs/load02.png" alt="2" style="width:600px;">

When 1,000 users sent 23,223 requests, the success rate was 100%, and the app's RPS (Requests Per Second) remained stable at around 320.

**6000 users, spawn-rate 50**:

<img src="/imgs/load03.png" alt="3" style="width:600px;">

<img src="/imgs/load04.png" alt="4" style="width:600px;">

When 6,000 users sent 70,964 requests, the success rate was 100%, and the app's RPS (Requests Per Second) remained stable at around 630.

The service didn't achieve 10,000 RPS. Here are the potential reasons:
- Autoscaling Delays: App Runner may not scale fast enough to handle the sudden spike in traffic to achieve 10,000 RPS.
- Compute and Memory: Insufficient compute (CPU) or memory on the instances can cause the application to slow down or fail under heavy load.
- Threading/Concurrency: Limited use of asynchronous programming or threading can restrict performance under heavy load.

## CI/CD Pipeline
CI/CD, short for Continuous Integration and Continuous Delivery, 
refers to a set of practices aimed at automating the processes of building, testing, and deploying code. 
The purpose of CI/CD is to streamline the integration and testing of code changes 
while ensuring the continuous delivery of updated software versions.

This repository implements a CI/CD pipeline that is triggered 
whenever changes are pushed to the master branch. 
The pipeline is configured in the `.github/workflows` directory, 
which contains several files, each outlining specific jobs in the process. 
These jobs include installing dependencies, linting, formatting code, and running tests. 
The badges displayed at the top of the README indicate that all jobs in the pipeline are 
currently running successfully.

## Infrastructure as Code (IaC)
To further streamline our deployment process and ensure consistent, repeatable setups, 
we integrate Infrastructure as Code (IaC) practices using CloudFormation.

AWS CloudFormation is a service that helps model and set up AWS resources using infrastructure as code. 
With CloudFormation, we define our infrastructure in a YAML template `cloudformation.yaml`, 
and AWS takes care of provisioning and managing those resources for us.
```
AWSTemplateFormatVersion: "2010-09-09"
Description: Deploy Flask App using CloudFormation

Resources:
  FlaskAppRunnerService:
    Type: AWS::AppRunner::Service
    Properties:
      ServiceName: "airsense"
      SourceConfiguration:
        ImageRepository:
        ...
```

## Reflections
All reflections including team member self reflection files and 
team reflection after meeting are included in the `Team_Reflections` folder in this repository.
