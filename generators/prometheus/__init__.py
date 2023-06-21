import jinja2

from generators import models, utils


def generate(data: models.PrometheusSettings, id: str):
    template_str = utils.get_content("prometheus/prometheus.template")
    template = jinja2.Template(template_str)
    content = template.render(
        exporters=[exporter.__dict__ for exporter in data.exporters]
    )
    utils.save_config_file(id, "prometheus/prometheus.yml", content)

    # alert_rules = utils.get_content(
    #     "prometheus/ransomeware.rules.template.yml"
    # )
    # utils.save_config_file(id, "prometheus/ransomeware.rules.yml", alert_rules)
