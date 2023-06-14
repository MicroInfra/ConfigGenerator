import json
import typing as tp

from grafanalib._gen import DashboardEncoder
from grafanalib.core import *

from generators import utils


def save_dashboard(id: str, dashboard: Dashboard, name: str):
    dashboard_json = json.dumps(
        dashboard.to_json_data(),
        sort_keys=True,
        indent=2,
        cls=DashboardEncoder,
    )
    utils.save_config_file(
        id, f"grafana/dashboards/{name}.json", dashboard_json
    )


def generate_default_dashboard(name, authorised_requests=False):
    panels = [
        RowPanel(
            title="RPS",
            gridPos=GridPos(h=0, w=0, x=0, y=0),
        ),
        TimeSeries(
            title="Request Count",
            dataSource="Prometheus",
            targets=[
                Target(
                    expr="increase(%(name)s_request_count_total{}[$__interval])"
                    % {"name": name},
                    legendFormat=name,
                ),
            ],
            gridPos=GridPos(h=9, w=24, x=0, y=1),
        ),
        TimeSeries(
            title="RPS by response code",
            dataSource="Prometheus",
            targets=[
                Target(
                    expr="increase(%(name)s_response_code_total{}[$__interval])"
                    % {"name": name},
                    legendFormat="{{code}}",
                ),
            ],
            legendDisplayMode="table",
            legendPlacement="right",
            legendCalcs=["min", "max", "mean", "last"],
            gridPos=GridPos(h=9, w=12, x=0, y=10),
        ),
        TimeSeries(
            title="RPS by url",
            dataSource="Prometheus",
            targets=[
                Target(
                    expr="increase(%(name)s_url_rps_total{}[$__interval])"
                    % {"name": name},
                    legendFormat="{{url}}",
                ),
            ],
            legendDisplayMode="table",
            legendPlacement="right",
            legendCalcs=["min", "max", "mean", "last"],
            gridPos=GridPos(h=9, w=12, x=12, y=10),
        ),
        RowPanel(
            title="Latency",
            gridPos=GridPos(h=0, w=0, x=0, y=19),
        ),
        TimeSeries(
            title="Service latency",
            dataSource="Prometheus",
            targets=[
                Target(
                    expr="%(name)s_response_latency_ms{}" % {"name": name},
                    legendFormat="{{name}} latency" % {"name": name},
                ),
            ],
            legendDisplayMode="table",
            legendPlacement="right",
            legendCalcs=[
                "min",
                "max",
                "mean",
            ],
            gridPos=GridPos(h=9, w=24, x=0, y=20),
        ),
        RowPanel(
            title="Geo",
            gridPos=GridPos(h=0, w=0, x=0, y=29),
        ),
        TimeSeries(
            title="RPS by ip",
            dataSource="Prometheus",
            targets=[
                Target(
                    expr="increase(%(name)s_ip_rps_total{}[$__interval])"
                    % {"name": name},
                    legendFormat="{{ip}}",
                ),
            ],
            gridPos=GridPos(h=9, w=24, x=0, y=30),
        ),
        RowPanel(
            title="Request/response size",
            gridPos=GridPos(h=0, w=0, x=0, y=39),
        ),
        TimeSeries(
            title="Request size",
            dataSource="Prometheus",
            targets=[
                Target(
                    expr="%(name)s_request_size{})" % {"name": name},
                    legendFormat="{{name}} request size" % {"name": name},
                ),
            ],
            gridPos=GridPos(h=9, w=12, x=0, y=40),
        ),
        TimeSeries(
            title="Response size",
            dataSource="Prometheus",
            targets=[
                Target(
                    expr="%(name)s_request_size{})" % {"name": name},
                    legendFormat="{{name}} request size" % {"name": name},
                ),
            ],
            gridPos=GridPos(h=9, w=12, x=12, y=40),
        ),
    ]
    y = 49

    if authorised_requests:
        panels.extend(
            [
                RowPanel(
                    title="Authorised requests",
                    gridPos=GridPos(h=0, w=0, x=0, y=y),
                ),
                TimeSeries(
                    title="Amount of authorised requests",
                    dataSource="Prometheus",
                    targets=[
                        Target(
                            expr="increase(%(name)s_authorised_requests_total{}[$__interval]))"
                            % {"name": name},
                            legendFormat="authorised",
                        ),
                        Target(
                            expr="increase(%(name)s_not_authorised_requests_total{}[$__interval]))"
                            % {"name": name},
                            legendFormat="Not authorised",
                        ),
                    ],
                    scaleDistributionType="log",
                    gridPos=GridPos(h=9, w=12, x=0, y=y + 1),
                ),
            ]
        )
        y += 10

    dashboard = Dashboard(
        title=f"{name} dashboard",
        description="Default dashboard for service genereted using https://github.com/MicroInfra",
        timezone="browser",
        panels=panels,
    ).auto_panel_ids()

    return dashboard


def generate(id: str, services: tp.List[str]):
    for service in services:
        dashboard = generate_default_dashboard(service)
        save_dashboard(id, dashboard, service)
