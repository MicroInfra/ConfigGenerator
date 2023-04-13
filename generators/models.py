import typing as tp

from pydantic import BaseModel, Field


class GrafanaSettings(BaseModel):
    username: str
    password: str

    def __str__(self):
        return f"Login: {self.username}\n" + f"Password: {self.password}"


class Exporter(BaseModel):
    name: str
    host_port: str
    metrics_path: str = "/metrics"
    params: dict | None = None

    def __str__(self):
        return (
            f"Name: {self.name}\n"
            + f"URL: {self.host_port}\n"
            + f"Metrics Path: {self.metrics_path}\n"
            + f"Params: {self.params}\n___"
        )


class PrometheusSettings(BaseModel):
    username: str
    password: str
    url: str = "http://localhost:9090"
    exporters: tp.List[Exporter]

    def __str__(self):
        return (
            f"Login: {self.username}\n"
            + f"Password: {self.password}\n"
            + f"Exporters:\n"
            + f"{str().join([str(e) for e in self.exporters])}\n"
        )


class ProxyManagerSettings(BaseModel):
    username: str
    password: str


class RequestGrafanaSettings(BaseModel):
    username: str | None = None
    password: str | None = None


class RequestPrometheusSettings(BaseModel):
    username: str | None = None
    password: str | None = None
    exporters: tp.List[Exporter] | None = None


class RequestProxyManagerSettings(BaseModel):
    username: str | None = None
    password: str | None = None


class Service(BaseModel):
    name: str
    url: str


class RequestConfig(BaseModel):
    grafana: RequestGrafanaSettings | None = None
    prometheus: RequestPrometheusSettings | None = None
    proxy_manager: RequestProxyManagerSettings | None = None
    services: tp.List[str] | None = None
    enable_nginx_reverse_proxy: bool = Field(
        default=False,
        description="Learn more: https://hub.docker.com/r/jwilder/nginx-proxy",
    )


class Config(BaseModel):
    id: str
    grafana: GrafanaSettings
    prometheus: PrometheusSettings
    proxy_manager: ProxyManagerSettings
    services: tp.List[str]
    enable_nginx_reverse_proxy: bool

    def __str__(self):
        return (
            f"ID: {self.id}\n"
            + f"Grafana:\n{str(self.grafana)}\n\n"
            + f"Prometheus:\n{str(self.prometheus)}"
        )
