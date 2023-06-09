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
    with open(get_path(relative_path), "r") as file:
        return file.read()


def save_config_file(
    id: str, relative_path: str, content: str, permissions=0o666
):
    path = TMP_FILES_DIR + id + "/" + relative_path
    output_file = Path(path)
    output_file.parent.mkdir(
        exist_ok=True,
        parents=True,
    )
    output_file.write_text(content)
    os.chmod(path, permissions)


def mkdir(id: str, relative_folder_path: str, permissions=0o666):
    path = TMP_FILES_DIR + id + "/" + relative_folder_path
    os.mkdir(path)
    os.chmod(path, permissions)


def config_exists(id: str) -> (bool, str):
    path = TMP_FILES_DIR + id + ".zip"
    if os.path.exists(path):
        return True, path
    return False, ""


def archive_configuration(id: str):
    path = TMP_FILES_DIR + id
    shutil.make_archive(path, "zip", path)


def delete_config_folder(id: str):
    path = TMP_FILES_DIR + id
    shutil.rmtree(path)


def get_config_url(id: str) -> str:
    return f"https://api.microinfra.justmark0.me/config/{id}"
