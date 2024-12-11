# AirSense - Insights of Flights

## Architectural Design

### Microservices Overview

- `AirGateway` and `AirConnector` are containerized using Docker and run within AWS App Runner.
- `AirBroker` leverages Databricks to preprocess data and generate final data tables.
- `AirStore` is a GraphSQL database running on AWS RDS Aurora, designed to store and maintain all flight-related data.

These services work together to form a stable and efficient microservices application.

### Diagram

- insert image here

## Services

### AirGateway

`AirGateway` is powered by Flask and aims to handle users' and administrators' restful API requests and forward them to proper mircro-services (`AirConnector`, `AirStore`). It has the ability to handle at least 10,000 requests per seconds.

### AirBroker

`AirBroker` leverages databricks to preprocess data and generate final data tables that will be ready use for `AirGateway`.

### AirConnector

`AirConnector` connectes `AirBroker` and `AirStore`. It transfers data tables from databricks to `AirStore` and ready for query by `AirGateway`.

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

### Python

**Attn: If you would like to test functions locally, please follow instructions below.**

- *please use Python3 version `3.12.8` and usage of `pyenv` and virtual environment is highly recommended.*

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
