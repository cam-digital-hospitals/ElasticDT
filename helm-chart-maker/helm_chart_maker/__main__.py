"""Rntrypoint for helm_chart_maker."""

import argparse
import sys
from pathlib import Path
from textwrap import dedent

from colorama import Fore

from . import models, prompts, tty
from .chart_yaml_gen import generate_chart_yaml


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
                        help='The output directory to save the chart to. Defaults to "./out/".',
                        metavar='OUTDIR')

    args = parser.parse_args()
    out_path = Path(args.out_dir).resolve()
    print(f'{Fore.YELLOW}Creating "{out_path}" (if not exists)...{Fore.RESET}')
    Path.mkdir(out_path, parents=True, exist_ok=True)

    if args.json is None:
        meta = prompts.meta()

        print()
        chart_data = models.ChartData(meta=meta)

        chart_yaml = generate_chart_yaml(chart_data)
        tty.instruction('OUTPUT - Chart.yaml:')
        print(chart_yaml)
        with open(Path(out_path) / 'Chart.yaml', 'w', encoding='utf-8') as fp:
            print(chart_yaml, file=fp)
    else:
        tty.error('Non-interactive (JSON) mode not yet implemented.')


if __name__ == '__main__':
    main()
