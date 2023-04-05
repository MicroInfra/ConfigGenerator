from generators import docker_compose, grafana, models, prometheus


def generate_all(config: models.Config):
    prometheus.generate(config.prometheus, config.id)
    grafana.generate(config.grafana, config.id)
    docker_compose.generate(config.id)
