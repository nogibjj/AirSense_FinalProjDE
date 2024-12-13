# AirSense - Insights of Flights

[![Install](https://github.com/nogibjj/airsense/actions/workflows/install.yml/badge.svg)](https://github.com/nogibjj/airsense/actions/workflows/install.yml)
[![Lint](https://github.com/nogibjj/airsense/actions/workflows/lint.yml/badge.svg)](https://github.com/nogibjj/airsense/actions/workflows/lint.yml)
[![Format](https://github.com/nogibjj/airsense/actions/workflows/format.yml/badge.svg)](https://github.com/nogibjj/airsense/actions/workflows/format.yml)
[![Test](https://github.com/nogibjj/airsense/actions/workflows/test.yml/badge.svg)](https://github.com/nogibjj/airsense/actions/workflows/test.yml)

_AirSense is a microservices-based application designed to provide insights into flights, focusing on efficient data handling and scalability. The project combines several components to manage, preprocess, and serve flight-related data seamlessly. The system aims to process and respond to user queries about flights with high concurrency and reliability._

## Demo Presentation

[![Watch the video](https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg)](https://www.youtube.com/watch?v=dQw4w9WgXcQ)

Alternative: Watch the video on [YouTube](https://www.youtube.com/watch?v=dQw4w9WgXcQ).

## Team Members:

- Jamie Liu
- Xianjing Huang
- Yijia Zhao

## Get Started

Make sure Docker Engine is installed on your host machine, and just one command to ship!

`docker compose up --build`

## System Design

### Microservices Overview

- `AirGateway`: Handles user and administrator REST API requests and routes them to the appropriate microservices. Designed for high throughput, managing up to 10,000 requests per second.

- `AirBroker`: Utilizes Databricks for data preprocessing and generating final datasets.

- `AirConnector`: Facilitates data transfer between AirBroker and AirStore.

- `AirStore`: A GraphSQL database hosted on AWS RDS Aurora, maintaining all flight-related data for query purposes.

_Why AirConnector?_: It brings ready-to-ship data to AirStore, which is closer to our server. For a single query, users can query and get their results within **0.2 seconds** instead of **12 seconds** if fetching from `AirBroker` directly.

These services work together to form a stable and efficient microservices application.

### Diagram

<img src="/imgs/airsense-2.png" alt="airsense-2" style="width:70%;">

### Services

The application is deployed on AWS App Runner.

![runner](/imgs/appRunner.png)

#### AirGateway

Designed for **Publics**.

- _Access using the following link:
  [https://watgt5vczp.us-east-2.awsapprunner.com](https://watgt5vczp.us-east-2.awsapprunner.com)_

`AirGateway` is powered by Flask and aims to handle users' and administrators' restful API requests and forward them to proper mircro-services (`AirConnector`, `AirStore`). It has the ability to handle at least 10,000 requests per seconds.

1. Users can utilize the advanced search function to query any keywords throughout the entire database, with results returned in milliseconds.

<div style="display: flex; justify-content: space-around;">
  <img src="/imgs/home-1.png" alt="home-1" style="width:45%;">
  <img src="/imgs/home-2.png" alt="home-2" style="width:45%;">
</div>

2. Users can interact with an interactive database exploration tool, enabling them to view data by order, ascending, descending, limit, and more.

<div style="display: flex; justify-content: space-around;">
  <img src="/imgs/explore-1.png" alt="explore-1" style="width:45%;">
  <img src="/imgs/explore-2.png" alt="explore-2" style="width:45%;">
</div>

3. Gateway also provides powerful query API portal, allowing user and other services query data via Restful API easily.

<div style="display: flex; justify-content: space-around;">
  <img src="/imgs/api-1.png" alt="api-1" style="width:45%;">
  <img src="/imgs/api-2.png" alt="api-2" style="width:45%;">
</div>

Query test example:

`[host_uri]/api/dynamic_query?table_name=busiest_airports_by_delays&limit=6&where=Avg_Departure_Delay:87,Total_Arrivals:4`

#### AirConnector

Designed for **Administrator**.

- _Access using the following link:
  [https://pywepkfr9p.us-east-2.awsapprunner.com/](https://pywepkfr9p.us-east-2.awsapprunner.com/)_

`AirConnector` connectes `AirBroker` and `AirStore`. It transfers data tables from databricks to `AirStore` and ready for query by `AirGateway`. Administrator can check the status of two database services, manually transfer data, and see history of operations.

- Transfering test example:

  `curl -X POST "[host_uri]:8000/transfer_table?table_name=delays_by_day`

<img src="/imgs/admin.png" alt="AdminDash" style="width:600px;">

## Leveraging LLM for Chatbot

We have integrated an advanced chatbot powered by OpenAI's API. This allows users to interact with the application through natural language conversations. Users can ask questions and get insights about flights, data, and any concern while using this application

### Key Features:

- **Natural Language Processing**: Understands and processes user queries in plain English.
- **Real-time Responses**: Provides instant answers to user questions.
- **Contextual Understanding**: Maintains context to handle follow-up questions effectively.

<img src="/imgs/chat.png" alt="Chatbot" style="width:600px;">

## Dependencies

### Languages and Frameworks:

- Python 3.12.8

- Flask: For powering `AirGateway` user interface and Restful API requests.

- FastAPI: For powering `AirConnector` and administrator interface.

- Spark: For preprocessing raw data and outputting clean tables in Databricks.

- SQL: For querying and GraphSQL database for data storage.

### Tools and Services:

- Databricks: For data preprocessing.

- Docker: Containerization of services for consistency and portability.

- AWS Elastic Container Registry (ECR): Store, manage, and deploy container images securely.

- AWS App Runner: For auto-scaling microservices.

- AWS RDS Aurora: As the relational database solution.

- Locust: For load testing Flask applications.

- CloudFormation: Infrastructure as Code for streamlined AWS resource provisioning.

- CloudWatch: For monitoring and observability of AWS resources and applications.

### Development Tools:

- Pyenv: Python version management.

- Virtual Environment: For dependency isolation during development.

- GitHub Actions: CI/CD pipelines for automated testing and deployment.

## Development

For details regarding repo structure and how to set up development environment, see [development.md](/development.md).

## Logging

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

## Others

### Potential Areas for Improvement

- Performance Optimization:
  Adopt VPC and ECS for faster inner communication.

- Enhanced Scalability:
  Experiment with alternative scaling solutions like Kubernetes for container orchestration. Use Load balancer and Redis to distribute server workloads.

### AI in Programing

- We used Copilot as frontend helper for the design of UI (html and css).

### About

![about](/imgs/about.png)
