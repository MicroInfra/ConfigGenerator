import glob
import os
import shutil
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.realpath(__file__)) + "/"
TMP_FILES_DIR = os.path.dirname(os.path.realpath(__file__)) + "/tmp/"


def clean():
    try:
        shutil.rmtree(TMP_FILES_DIR)
    except (FileNotFoundError, PermissionError) as err:
        print(err)
        return


def get_path(relative_path: str):
    return BASE_DIR + relative_path


def get_content(relative_path: str):
    with open(get_path("prometheus/prometheus.template"), "r") as file:
        return file.read()


def save_config_file(id: str, relative_path: str, content: str):
    path = TMP_FILES_DIR + id + "/" + relative_path
    output_file = Path(path)
    output_file.parent.mkdir(
        exist_ok=True,
        parents=True,
    )
    output_file.write_text(content)
