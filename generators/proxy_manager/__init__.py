import json

import jinja2

from generators import models, utils


def generate(data: models.Config):
    services = []
    template_str = utils.get_content("proxy_manager/default_rules.py")
    for service in data.services:
        template = jinja2.Template(template_str)
        rules = template.render(
            service_name=service.name,
            exporter_auth_token=data.microinfra_exporter.auth_token,
            exporter_url=data.microinfra_exporter.url,
        )
        services.append(
            {
                "serviceName": service.name,
                "serviceUrl": service.url,
                "listenPort": service.listen_port,
                "proxyType": "http",
                "rules": rules,
            }
        )

    utils.save_config_file(
        data.id, "proxy_manager/settings.json", json.dumps(services)
    )
