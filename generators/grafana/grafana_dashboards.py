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


def generate_default_dashboard(name: str):
    dashboard = Dashboard(
        title=f"Python generated example dashboard {name}",
        description="Example dashboard using the Random Walk and default Prometheus datasource",
        tags=[],
        timezone="browser",
        panels=[
            GaugePanel(
                title="Random Walk",
                dataSource="default",
                targets=[
                    Target(
                        datasource="grafana",
                        expr="example",
                    ),
                ],
                gridPos=GridPos(h=4, w=4, x=17, y=0),
            ),
        ],
    ).auto_panel_ids()

    return dashboard


def generate(id: str, services: tp.List[str]):
    for service in services:
        dashboard = generate_default_dashboard(service)
        save_dashboard(id, dashboard, service)
