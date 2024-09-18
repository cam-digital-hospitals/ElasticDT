"""Generate the YAML files for the Helm chart."""

import yaml

from .models import FullValues


def generate_chart_yaml(data: FullValues):
    """Generate Chart.yaml."""
    meta = {
        'apiVersion': 'v2',
        'name': data.meta.name,
        'version': str(data.meta.version),
        'appVersion': x if (x:= data.meta.appVersion) else None,
        'description': x if (x := data.meta.description) else None,
        'keywords': list(data.meta.tags),
        'maintainers': (
            [m.model_dump(exclude_none=True, mode='json') for m in x]
            if (x := data.meta.maintainers)
            else None
        )
    }
    meta = {k: v for k,v in meta.items() if v is not None}

    return yaml.dump(meta, sort_keys=False)
