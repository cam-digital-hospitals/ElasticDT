"""Rntrypoint for helm_chart_maker."""

import argparse
from pathlib import Path
from textwrap import dedent

import yaml
from colorama import Fore

from . import cli, models, prompts
from .yaml_gen import generate_chart_yaml


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        prog='HelmChartMaker',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=dedent("""\
            Helm Chart Maker with interactive and JSON modes.
            
            Use without arguments for interactive mode, or with --json=file to supply an
            configuration file.""")
    )
    parser.add_argument('--json',
                        help='JSON file to parse in non-interactive mode.',
                        metavar='FILENAME')
    parser.add_argument('-o', '--out-dir',
                        default='./out/',
                        help='The output directory to save the chart to. Defaults to "./out/". '
                             'If set to "-", print to screen only.',
                        metavar='OUTDIR')

    args = parser.parse_args()

    if args.out_dir != '-':
        out_path = Path(args.out_dir).resolve()
        print(f'{Fore.YELLOW}Creating "{
              out_path}" (if not exists)...{Fore.RESET}')
        Path.mkdir(out_path, parents=True, exist_ok=True)

    if args.json is None:

        cli.instruction("Hello from helm-chart-maker!")
        print()
        cli.instruction("""############ PART 1 of {n} -- CHART METADATA ############""")
        chart_meta = prompts.meta()

        print()
        cli.instruction("""############ PART 2 of {n} -- DEPLOYMENT ############""")
        deployment_data = prompts.deployment()

        full_chart = models.FullChart(
            meta=chart_meta,
            deployment=deployment_data
        )
        print()
        print()
        cli.instruction("######################################################################")
        print()
        cli.instruction('INPUT SUMMARY:')
        print(yaml.dump(full_chart.model_dump(mode='json'), sort_keys=False))

        # CHART.YAML
        chart_yaml = generate_chart_yaml(full_chart)
        cli.instruction('OUTPUT - Chart.yaml:')
        print(chart_yaml)
        if args.out_dir != '-':
            with open(Path(out_path) / 'Chart.yaml', 'w', encoding='utf-8') as fp:
                print(chart_yaml, file=fp)
    else:
        cli.error('Non-interactive (JSON) mode not yet implemented.')


if __name__ == '__main__':
    main()
