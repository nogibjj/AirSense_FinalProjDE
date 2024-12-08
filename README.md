# AirSense_FinalProjDE

## Services

### API Gateway

API Gateway handles user requests and forward them to proper mircro-services. It has the ability to handle at least 10,000 requests per seconds.

#### Development using Python3

For developers: please use Python3 version `3.12.8` and usage of `pyenv` and virtual environment is highly recommended.

##### Pyenv

```bash
pyenv install 3.12.8
pyenv global 3.12.8
# restart terminal if necessary
which python3 # /home/[username]/.pyenv/shims/python3
python3 -V # Python 3.12.8
```

##### Virtual Environment

```bash
cd gateway
python3 -m venv venv
source venv/bin/activate
which python3 # [repo]/gateway/venv/bin/python3
```

##### Install

```bash
pip install
```

##### Run service

```python3
python3 app.py
```
