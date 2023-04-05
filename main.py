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


@app.post("/")
async def create_config(
    request: models.RequestConfig | None = None,
) -> models.Config:
    utils.clean()
    print(request)
    config = models.Config(
        id=uuid.uuid4().hex,
        grafana=models.GrafanaSettings(
            username=request.grafana.username or "admin",
            password=request.grafana.password or new_password(),
        ),
        prometheus=models.PrometheusSettings(
            username=request.grafana.username or "admin",
            password=request.grafana.password or new_password(),
            exporters=request.prometheus.exporters or [],
        ),
        proxy_manager=models.ProxyManagerSettings(
            username=request.grafana.username or "admin",
            password=request.grafana.password or new_password(),
        ),
        services=request.services or list(),
        enable_nginx_reverse_proxy=request.enable_nginx_reverse_proxy,
    )
    generate_all(config=config)

    return config


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
