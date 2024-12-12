import requests
import os

def create_directory(path):
    """
    Creates a directory in DBFS if it doesn't already exist.
    """
    local_path = path.replace("dbfs:/", "/dbfs/")
    if not os.path.exists(local_path):
        os.makedirs(local_path, exist_ok=True)
        print(f"Directory created at {path}")
    else:
        print(f"Directory already exists at {path}")


def extract(url, file_path):
    """
    Downloads a file from the specified URL and saves it to the specified DBFS path.
    """
    # Ensure the directory exists
    directory_path = "/".join(file_path.split("/")[:-1])
    create_directory(directory_path)

    print(f"Starting download from {url}")
    local_path = file_path.replace("dbfs:/", "/dbfs/")

    try:
        with requests.get(url, stream=True, timeout=120) as response:
            response.raise_for_status()  # Raise error for bad responses (4xx or 5xx)
            with open(local_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):  # Download in 8 KB chunks
                    file.write(chunk)
        print(f"File successfully downloaded to {local_path}")
        # Sync the file to DBFS namespace
        dbutils.fs.cp(f"file:{local_path}", file_path)
        print(f"File synced to DBFS: {file_path}")
        downloaded_size = os.path.getsize(local_path)
        print(f"Downloaded file size: {downloaded_size} bytes")
        # with open(local_path, "r") as file:
        #     print(file.read(500))  # Preview the first 500 characters
    except Exception as e:
        print(f"Error during download: {e}")
    


if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/nogibjj/Xianjing_Huang_Mini_Proj_test/refs/heads/main/flight_delays2.csv"
    file_path = "dbfs:/FileStore/flight_delays.csv"

    extract(url, file_path)