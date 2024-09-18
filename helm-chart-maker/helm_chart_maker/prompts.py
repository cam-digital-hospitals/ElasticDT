"""Helm chart maker.  Asks a bunch of questions to make a Helm chart."""

import json
import re

import semver
from colorama import Fore
from pydantic import ValidationError

from .cli import error, instruction, prompt, raw_error
from .models import TAGS, ChartMeta, Deployment, Maintainer, check_tags


def meta() -> ChartMeta:
    """Get metadata for a Helm chart, which is outputted to Chart.yaml."""

    print()
    instruction("What name do you want to give your chart?")
    while True:
        # TODO: make RFC 1035 utility function
        chart_name = prompt("name: ")
        try:
            assert chart_name, "Chart name cannot be empty, try again."
            assert re.fullmatch(r"[a-z][a-z0-9-]*[a-z0-9]", chart_name), """\
                Chart name should contain only lowercase letters, digits, and hyphens, but the first
                character must be a lowercase letter and hyphens may not appear in the first or
                last positions. Try again."""
            assert len(chart_name) < 48, """\
                The maximum supported chart name length is 47 characters. This ensures that any
                additional resources associated with this deployment, e.g.,
                `my-deployment-httproute`, compiles with the maximum name length of 63
                (RFC 1035). Try again."""
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
        instruction(f"* {k}: {v}", hanging=2)
    while True:
        try:
            tags = [x for s in str.split(
                prompt("tags: "), ";") if (x := s.strip()) != '']
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
        maintainer = {k: v for k, v in maintainer.items()
                      if v is not None and v != ''}
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


def deployment() -> Deployment:
    """Prompt for information relating to a Helm chart's Deployment specification,
    excluding information in the ChartMeta object."""

    def get_containers() -> list[dict]:
        """Get the list of containers."""

        containers = []
        all_ports = []
        idx = 0

        while True:
            print()
            instruction("""\
                        Enter the name and tag of the Docker image you want to use, e.g. 
                        "ghcr.io/cam-digital-hospitals/elasticdt/ui-homepage:latest". If
                        no tag is given, "latest" will be assumed. A blank entry will end
                        the list of containers.""")
            try:
                image_tag = prompt('image_tag: ')
                if not image_tag:
                    if not containers:
                        print()
                        no_deploy = prompt(
                            "No containers defined. Are you sure you want to create"
                            "a chart without a deployment? [y/N]: ")
                        no_deploy = no_deploy.strip().lower()
                        if no_deploy != 'y':
                            continue  # return to prompt
                        else:
                            return containers
                    else:
                        return containers
                image_tag = image_tag.split(':')

                assert len(image_tag) in (1, 2), \
                    """Input must be in the format "image[:tag]". Try again."""
                if len(image_tag) == 1:
                    image_tag.append('latest')
            except AssertionError as e:
                error(str(e))

            idx += 1

            print()
            instruction("""\
                        Enter a list of port numbers that the container will listen on, separated
                        by spaces. Port numbers must be unique across all containers in a pod.
                        Leave blank if no ports are to be exposed to the cluster.""")
            while True:
                try:
                    ports = prompt("ports: ", default=[])
                    if not ports:
                        break
                    ports = [int(port) for port in ports.split()]

                    # Check all port numbers valid
                    for port in ports:
                        assert 0 < port < 30000, \
                            f"""\
                            Port {port} is not between 1 and 29999. Note that ports 30000-32767
                            are reserved for NodePorts only. Try again."""

                    # Check no duplicate ports for container
                    assert len(set(ports)) == len(ports), \
                        """Duplicate port numbers detected. Try again."""

                    # Check no duplicate ports across entire pod
                    test_all_ports = [*all_ports, *ports]
                    assert len(set(test_all_ports)) == len(test_all_ports), \
                        """\
                        Some ports requested by this container have already been assigned to
                        other containers in the pod. Try again."""
                    all_ports = test_all_ports
                    break

                except AssertionError as e:
                    error(str(e))

            print()
            instruction("""\
                        Great! Let's add some data to our volume. You can add a
                        PersistentVolumeClaim, ConfigMap, or Secret. Note that we will only
                        prompt for the name of the data object for now, you can use our
                        separate tools later for creating the data object itself.""")
            data = []
            while True:
                x = prompt("1. PVC; 2: ConfigMap; 3: Secret; 4(default): quit [1-4]: ",
                           default='4')
                if x == '4':
                    print(f"{Fore.YELLOW}End of specification for Container #{
                        idx}.{Fore.YELLOW}\n")
                    break
                if x in ['1', '2', '3']:
                    t = int(x)
                    data_type = ['', 'pvc', 'configMap', 'secret'][t]
                    # TODO check RFC 1035 compatibility
                    data_name = prompt('data_name: ')
                    x = f"Enter the mount path for {data_name}."
                    if t in (2, 3):
                        x += (
                            "If \"envFrom\" is supplied, the "
                            f"{'ConfigMap' if t == 2 else 'Secret'} will be converted into a "
                            "list of environment variables instead."
                        )
                    # TODO check non-empty string
                    mount_path = prompt('mountPath: ')
                    data.append({
                        'type': data_type,
                        'name': data_name,
                        'mount_path': mount_path
                    })
                    print(f"{Fore.YELLOW}Added {data_name} to container.{Fore.YELLOW}\n")

            containers.append({
                'image': image_tag[0],
                'tag': image_tag[1],
                'ports': sorted(ports),
                'data': data
            })

    containers = get_containers()
    # print(json.dumps(containers, indent=2))

    print()
    print()
    instruction(f"{len(containers)} container(s) specified!")
    instruction(
        "How many replications of this pod do you want on the cluster? (Default: 1)")
    while True:
        try:
            x = prompt("replicas: ", default=1)
            replicas = int(x)
            assert replicas > 0, 'Number of replicas must be positive. Try again.'
            break
        except ValueError:
            error(f'Cannot parse "{x}" as an integer. Try again.')
        except AssertionError as e:
            error(str(e))

    return Deployment(replicas=replicas, containers=containers)
