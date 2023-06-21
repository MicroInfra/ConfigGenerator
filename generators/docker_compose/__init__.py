import jinja2

from generators import models, utils


def generate(config: models.Config):
    template_str = utils.get_content(
        "docker_compose/docker-compose.template.yml"
    )
    template = jinja2.Template(template_str)
    content = template.render(
        exporter_auth_token=config.microinfra_exporter.auth_token,
        use_docker_network=config.use_docker_network or False,
    )
    utils.save_config_file(config.id, "docker-compose.yml", content)
