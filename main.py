import asyncio
import secrets
import string
import uuid

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse

from generators import generate_all, models, utils

app = FastAPI()
debug = False


def new_password(length: int = 18):
    alphabet = string.ascii_letters + string.digits + "_"
    return "".join(secrets.choice(alphabet) for _ in range(length))


@app.get("/")
async def root_get():
    return RedirectResponse("/docs")


@app.get("/config/{id:str}")
async def config_get(id: str):
    exists, path = utils.config_exists(id)
    if exists:
        return FileResponse(path, filename="microinfra_config.zip")
    return FileNotFoundError


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
) -> models.Response:
    if debug:
        # utils.clean()
        print("Request is:", request)

    exporters: list = get_field(request, "prometheus.exporters") or []
    id = uuid.uuid4().hex
    config = models.Config(
        id=id,
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
        config_url=utils.get_config_url(id),
    )
    generate_all(config=config)

    utils.archive_configuration(config.id)
    if debug:
        print("GENERATED CONFIG:\n", config)
    else:
        utils.delete_config_folder(config.id)
    return models.Response(config=config, formatted_config=str(config))


def test_config_generate():
    global debug
    debug = True
    loop = asyncio.get_event_loop()
    coroutine = create_config()
    loop.run_until_complete(coroutine)


if __name__ == "__main__":
    # test_config_generate()
    uvicorn.run(app, host="0.0.0.0", port=8085)
