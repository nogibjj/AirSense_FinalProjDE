import os


def test_html_files(directory="./services/connector/ui/"):
    """checks html files exists"""
    html_files = [f for f in os.listdir(directory) if f.endswith(".html")]

    for html_file in html_files:
        file_path = os.path.join(directory, html_file)
        assert os.path.exists(file_path) and os.path.isfile(file_path)


if __name__ == "__main__":
    test_html_files()
