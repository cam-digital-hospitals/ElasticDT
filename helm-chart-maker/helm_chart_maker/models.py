"""Pydantic dataclasses for helm_chart_maker."""

from collections.abc import Sequence
from os import PathLike
from typing import Annotated, Literal, Optional

import pydantic as pyd
from annotated_types import Ge, Le
from pydantic_extra_types.semantic_version import SemanticVersion

TAGS = {
    "SEN": "Sensing, collects data from various sensors.",
    "DI":  "Data integration, combines data from various sources to provide a unified view",
    "DS":  "Data storage, handles data manipulation and processing operations.",
    "ACT": "Actuation, performs actions in response to data inputs or user commands.",
    "SEC": "Security, e.g. authentication, authorization, and/or encryption.",
    "UI":  "User interface, GUI or CLI.",
    "MNT": "Maintainence, system status/diagnostics, updates/upgrades, etc.",
}
"""A set of valid tags for the Helm chart's service type."""


def check_tags(tags: Sequence[str]) -> Sequence[str]:
    """Check for a valid list of tags."""
    assert len(tags) > 0, 'Chart must have at least one tag. Try again.'
    for i, tag in enumerate(tags):
        assert len(tag) > 0, f'Tag #{i+1} has length zero. Try again.'
    assert tags[0] in TAGS, 'The first tag is not from the list of special tags.  Try again.'

    return tags


class FullChart(pyd.BaseModel):
    """The full set of inputs for generating the Helm chart."""
    meta: 'ChartMeta'
    deployment: 'Deployment'


### Chart Meta ###
class ChartMeta(pyd.BaseModel):
    """Metadata about the Helm chart that appears in Chart.yaml."""
    name: str
    description: str
    version: SemanticVersion
    app_version: Optional[str]
    tags: Annotated[Sequence[str], pyd.AfterValidator(check_tags)]
    maintainers: Sequence['Maintainer']


class Maintainer(pyd.BaseModel):
    """Metadata about a maintainer."""
    name: str
    email: Optional[pyd.EmailStr] = pyd.Field(default=None)
    url: Optional[pyd.HttpUrl] = pyd.Field(default=None)


### Deployment ###
class Deployment(pyd.BaseModel):
    """Data about a deployment, excluding the common information in the ChartMeta instance."""
    replicas: pyd.PositiveInt
    containers: Sequence['Container']


class Container(pyd.BaseModel):
    """Data about a container in a pod (for a deployment)."""
    image: str
    tag: str
    ports: set[Annotated[int, Ge(0), Le(30000)]]
    data: Sequence['ContainerData']


class ContainerData(pyd.BaseModel):
    """Container data specification."""
    type: Literal['pvc','configMap','secret']
    name: str
    mount_path: PathLike  # We will treat "envFrom" as a special case
