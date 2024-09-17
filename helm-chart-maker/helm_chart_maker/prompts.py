"""Helm chart maker.  Asks a bunch of questions to make a Helm chart."""

import re

from colorama import Fore
from pydantic import ValidationError
import semver

from .models import TAGS, ChartMeta, check_tags, Maintainer
from .tty import error, instruction, prompt, raw_error


def meta() -> ChartMeta:
    """Get metadata for a Helm chart, which is outputted to Chart.yaml."""

    instruction("""\
          Hello from helm-chart-maker!

          What name do you want to give your chart?""")
    while True:
        chart_name = prompt("name: ")
        try:
            assert len(chart_name), "Chart name cannot be empty, try again."
            assert re.fullmatch(r"[a-z][a-z0-9-]*[a-z0-9]", chart_name), """\
                Chart name should contain only lowercase letters, digits, and hyphens, but the first
                character must be a lowercase letter and hyphens may not appear in the first or
                last positions. Try again."""
            break
        except AssertionError as e:
            error(str(e))

    print()
    instruction("Give your chart a description (default=blank)")
    chart_description = prompt("description: ")

    print()
    instruction("""\
                What is the version number of your project? Use [MAJOR].[MINOR].[PATCH]
                for the version number (default=0.1.0).""")
    while True:
        chart_version = prompt("version: ", default='0.1.0')
        try:
            ver = semver.Version.parse(chart_version)
            assert ver.prerelease is None and ver.build is None
            break
        except ValueError:
            error(f"""\
                  \"{chart_version}\" is not a valid version string. Valid strings are in the
                  format \"[MAJOR].[MINOR].[PATCH]\". Try again.""")

    print()
    instruction("""\
                Enter an app version, or leave blank to omit. Unlike the chart version,
                this version string can have any format. For a single-container chart, the
                app version should match the tag of the container image, e.g. 'latest'.
                (default=None)""")
    chart_app_version = prompt("appVersion: ", default=None)

    print()
    instruction("""\
                Enter a list of chart tags, seperated by semicolons. The first tag defines
                the primary service type and must be one of:""")
    for k, v in TAGS.items():
        instruction(f"* {k}: {v}")
    while True:
        try:
            tags = [x for s in str.split(prompt("tags: "), ";") if (x := s.strip()) != '']
            if check_tags(tags):
                break
        except AssertionError as e:
            error(str(e))

    print()
    instruction("""\
                Enter a list of service dependency names, seperated by semicolons. Leave blank if
                there are no dependencies. Installing the generated Helm chart will fail if the
                listed dependencies are not already running on the cluster.""")
    reqs = [f"requires({x})" for s in str.split(prompt("requires: "), ";")
            if (x := s.strip()) != '']

    tags = [*tags, *reqs]

    print()
    instruction("""\
                Define the maintainers of this Helm chart and its associated containers.
                The name is required for each maintainer; emails and URLs are optional.
                Enter a blank name to terminate the list of maintainers.""")
    maintainers = []
    n = 1
    while True:
        name = prompt("name: ")
        if name == '':
            break
        email = prompt("email: ", default=None)
        url = prompt("url: ", default=None)
        maintainer = {"name": name, "email": email, "url": url}
        maintainer = {k: v for k, v in maintainer.items() if v is not None and v != ''}
        try:
            Maintainer.model_validate(maintainer)
        except ValidationError as e:
            raw_error(f'Pydantic validation error: {str(e)}\n\nTry again.')
        print(f"{Fore.YELLOW}Maintainer {n}: {maintainer}{Fore.RESET}\n")
        maintainers.append(maintainer)
        n += 1

    ret = ChartMeta(
        name=chart_name,
        description=chart_description,
        version=chart_version,
        app_version=chart_app_version,
        tags=tags,
        maintainers=maintainers
    )
    return ret
