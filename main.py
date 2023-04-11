import secrets
import uuid

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from generators import generate_all, models, utils

app = FastAPI()


def new_password(length: int = 10):
    return secrets.token_urlsafe(length)


@app.get("/")
async def root_get():
    return RedirectResponse("/docs")


def get_field(request, fields: str):
    obj = request
    for field in fields.split("."):
        try:
            obj = getattr(obj, field)
        except AttributeError:
            return None
    return obj


@app.post("/")
async def create_config(
    request: models.RequestConfig | None = None,
) -> models.Config:
    utils.clean()
    print(request)
    config = models.Config(
        id=uuid.uuid4().hex,
        grafana=models.GrafanaSettings(
            username=get_field(request, "grafana.username") or "admin",
            password=get_field(request, "grafana.password") or new_password(),
        ),
        prometheus=models.PrometheusSettings(
            username=get_field(request, "prometheus.username") or "admin",
            password=get_field(request, "prometheus.password")
            or new_password(),
            exporters=get_field(request, "prometheus.password") or [],
        ),
        proxy_manager=models.ProxyManagerSettings(
            username=get_field(request, "proxy_manager.username") or "admin",
            password=get_field(request, "proxy_manager.password")
            or new_password(),
        ),
        services=get_field(request, "enable_nginx_reverse_proxy") or list(),
        enable_nginx_reverse_proxy=get_field(
            request, "enable_nginx_reverse_proxy"
        )
        or False,
    )
    generate_all(config=config)

    return config


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
