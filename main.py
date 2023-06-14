import asyncio
import secrets
import string
import uuid

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from generators import generate_all, models, utils

app = FastAPI()


def new_password(length: int = 18):
    alphabet = string.ascii_letters + string.digits + "_"
    return "".join(secrets.choice(alphabet) for _ in range(length))


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
    request: models.RequestConfig | None = None, debug: bool = False
) -> models.Response:
    utils.clean()
    print("Request is:", request)
    exporters: list = get_field(request, "prometheus.exporters") or []
    exporters.append(
        models.Exporter(name="windows", host_port="10.240.19.231:8080")
    )
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
            exporters=exporters,
        ),
        proxy_manager=models.ProxyManagerSettings(
            username=get_field(request, "proxy_manager.username") or "admin",
            password=get_field(request, "proxy_manager.password")
            or new_password(),
        ),
        microinfra_exporter=models.MicroinfraExporterSettings(
            auth_token=new_password()
        ),
        services=get_field(request, "services") or list(),
        enable_nginx_reverse_proxy=get_field(
            request, "enable_nginx_reverse_proxy"
        )
        or False,
    )
    generate_all(config=config)
    if debug:
        print("GENERATED CONFIG:\n", config)
    return models.Response(config=config, formatted_config=str(config))


def test():
    loop = asyncio.get_event_loop()
    coroutine = create_config(debug=True)
    loop.run_until_complete(coroutine)


if __name__ == "__main__":
    # test()
    uvicorn.run(app, host="0.0.0.0", port=8085)
