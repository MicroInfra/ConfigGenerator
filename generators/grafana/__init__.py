import jinja2

from generators import models, utils


def generate(data: models.Config, id: str):
    # Create grafana.ini file
    template_str = utils.get_content("grafana/grafana_ini.template.txt")
    template = jinja2.Template(template_str)
    content = template.render(
        username=data.grafana.username,
        password=data.grafana.password,
    )
    utils.save_config_file(id, "grafana/grafana.ini", content)
    # Create provisioning file with datasource
    template_str = utils.get_content("grafana/prometheus.template")
    template = jinja2.Template(template_str)
    content = template.render(
        prometheus_url=data.prometheus.url,
    )
    utils.save_config_file(id, "grafana/prometheus.yaml", content)

    utils.mkdir(id, "grafana-data", permissions=0o777)
