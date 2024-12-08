# AirSense_FinalProjDE

## Architectural Diagram

## Services

### API Gateway

API Gateway handles user requests and forward them to proper mircro-services. It has the ability to handle at least 10,000 requests per seconds.

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
