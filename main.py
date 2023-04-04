import secrets

from fastapi import FastAPI

from generators import models

app = FastAPI()


def gen_password(length: int = 10):
    return secrets.token_urlsafe(length)


@app.post("/")
async def read_items(
    request: models.RequestConfig | None = None,
) -> models.Config:
    print(request)
    config = models.Config(
        grafana=models.GrafanaSettings(
            username=request.grafana.username or "admin",
            password=request.grafana.password or gen_password(),
        ),
        prometheus=models.PrometheusSettings(
            username=request.grafana.username or "admin",
            password=request.grafana.password or gen_password(),
        ),
        proxy_manager=models.ProxyManagerSettings(
            username=request.grafana.username or "admin",
            password=request.grafana.password or gen_password(),
        ),
        services=request.services,
        enable_nginx_reverse_proxy=request.enable_nginx_reverse_proxy,
    )

    return config
