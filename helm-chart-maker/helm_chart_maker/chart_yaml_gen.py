"""Generate the Chart.yaml file."""

import yaml

from .models import ChartData


def generate_chart_yaml(data: ChartData):
    """Generate a yaml string from the chart data."""
    meta = {
        'apiVersion': 'v2',
        'name': data.meta.name,
        'version': str(data.meta.version),
    }

    if (x := data.meta.app_version) and len(x) > 0:
        meta['appVersion'] = x

    if (x := data.meta.description) and len(x) > 0:
        meta['description'] = x

    meta['keywords'] = list(data.meta.tags)

    if len(x := data.meta.maintainers) > 0:
        meta['maintainers'] = [m.model_dump(exclude_none=True, mode='json') for m in x]

    return yaml.dump(meta, sort_keys=False)
