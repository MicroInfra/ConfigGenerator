from generators import models, utils


def generate(data: models.GrafanaSettings, id: str):
    content = utils.get_content("grafana/grafana_ini.template.yml")
    utils.save_config_file(id, "grafana/grafana_ini.template.yml", content)
