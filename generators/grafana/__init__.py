import jinja2

from generators import models, utils
from generators.grafana import grafana_dashboards


def generate(data: models.Config):
    # Create grafana.ini file
    template_str = utils.get_content("grafana/grafana_ini.template.txt")
    template = jinja2.Template(template_str)
    content = template.render(
        username=data.grafana.username,
        password=data.grafana.password,
        prometheus_url=data.prometheus.url,
    )
    utils.save_config_file(data.id, "grafana/grafana.ini", content)
    # Create provisioning file with datasource
    template_str = utils.get_content("grafana/prometheus.template")
    template = jinja2.Template(template_str)
    content = template.render(
        prometheus_url=data.prometheus.url,
    )
    utils.save_config_file(data.id, "grafana/prometheus.yaml", content)

    # Import dashboard settings
    content = utils.get_content("grafana/dashboard.yaml")
    utils.save_config_file(data.id, "grafana/dashboard.yaml", content)

    # Predefine folder for data
    utils.mkdir(data.id, "grafana-data", permissions=0o777)

    grafana_dashboards.generate(
        id=data.id, services=[ser.name for ser in data.services]
    )
    # content = utils.get_content("grafana/test.dashboard.json")
    # utils.save_config_file(data.id, "grafana/dashboards/test.json", content)
