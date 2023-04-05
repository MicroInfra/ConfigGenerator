from generators import utils


def generate(id: str):
    content = utils.get_content("docker_compose/docker-compose.template.yml")
    utils.save_config_file(id, "docker-compose.yml", content)
