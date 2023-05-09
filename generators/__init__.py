from generators import (
    docker_compose,
    grafana,
    models,
    prometheus,
    proxy_manager,
)


def generate_all(config: models.Config):
    prometheus.generate(config.prometheus, config.id)
    grafana.generate(config)
    docker_compose.generate(config)
    proxy_manager.generate(config)
