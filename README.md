# AirSense_FinalProjDE

## Architectural Diagram

## Services

### AirGateway

AirGateway handles users' and administrators' restful API requests and forward them to proper mircro-services (`AirCentral`, `AirCrawler`, `AirStore`). It has the ability to handle at least 10,000 requests per seconds.

### AirCrawler

AirCrawler is scheduled to craw daily ADS-B data from open data resources [https://github.com/adsblol/globe_history_2024](https://github.com/adsblol/globe_history_2024), unzip data, and convert raw json data to database `AirStore`.

- A sample of a processed aircraft data is located at [here](./doc/trace_full_a61d00.json).

### AirCentral

AirCentral is the main processor of AirSense application, and it serves parsing user request, retriving, filtering, and outputing expected data from database `AirStore`.

### AirStore

AirStore is a GraphSQL database aims to store and maintain all flight/aircraft related data and ready for use by other services.

## Development

### Repo Structure (demo only)

```
AirSense/
├── README.md
├── .gitignore
├── docker-compose.yml
├── shared/
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   ├── config.py
│   ├── tests/
│   └── requirements.txt
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
│   └── processor/
│       ├── processor/
│       │   ├── __init__.py
│       │   ├── main.py
│       │   ├── config.py
│       ├── Dockerfile
│       ├── requirements.txt
│       └── tests/
│           ├── test_processor.py
├── tools/
│   ├── cli_tool/
│   │   ├── main.py
│   │   ├── utils.py
│   │   └── tests/
│   │       ├── test_cli.py
└── scripts/
    ├── start_all.sh
    ├── deploy.sh

```

### Python

For developers: please use Python3 version `3.12.8` and usage of `pyenv` and virtual environment is highly recommended.

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
cd services/[service_name]
python3 -m venv [service_name]
source [service_name]/bin/activate
which python3 # [repo_name]/services/[service_name]/bin/python3
```

##### Install Libraries

```bash
pip install --no-cache-dir -r requirements.txt
```

##### Run service

```python3
python3 run.py
```

### Docker
