import os

def validate_env_vars():
    """Ensure necessary environment variables are set."""
    required_vars = [
        "DB_HOST",
        "DB_PORT",
        "DB_USER",
        "DB_PASSWORD",
        "DB_NAME",
        "OPENAI_API_KEY"
    ]
    for var in required_vars:
        if not os.getenv(var):
            raise EnvironmentError(f"Environment variable {var} is not set.")
    
    return f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
