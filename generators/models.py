import dataclasses
import typing as tp

from pydantic import BaseModel, Field


@dataclasses.dataclass
class GrafanaSettings:
    username: str
    password: str


@dataclasses.dataclass
class PrometheusSettings:
    username: str
    password: str


@dataclasses.dataclass
class ProxyManagerSettings:
    username: str
    password: str


@dataclasses.dataclass
class RequestGrafanaSettings:
    username: str | None = None
    password: str | None = None


@dataclasses.dataclass
class RequestPrometheusSettings:
    username: str | None = None
    password: str | None = None


@dataclasses.dataclass
class RequestProxyManagerSettings:
    username: str | None = None
    password: str | None = None


@dataclasses.dataclass
class RequestConfig(BaseModel):
    grafana: RequestGrafanaSettings | None = None
    prometheus: RequestPrometheusSettings | None = None
    proxy_manager: RequestProxyManagerSettings | None = None
    services: tp.List[str] | None = None
    enable_nginx_reverse_proxy: bool = Field(
        default=False,
        description="Learn more: https://hub.docker.com/r/jwilder/nginx-proxy",
    )


class Item(BaseModel):
    name: str = Field(example="Foo")
    description: str | None = Field(default=None, example="A very nice Item")
    price: float = Field(example=35.4)
    tax: float | None = Field(default=None, example=3.2)


@dataclasses.dataclass
class Config(BaseModel):
    grafana: GrafanaSettings
    prometheus: PrometheusSettings
    proxy_manager: ProxyManagerSettings
    services: tp.List[str]
    enable_nginx_reverse_proxy: bool
