# Helm chart maker

This python module creates Helm charts from a series of command-line prompts or from a JSON file (via a Pydantic class instance in both cases).

```console
$ uvpy -m helm_chart_maker -h
usage: HelmChartMaker [-h] [--json FILENAME] [-o OUTDIR]

Helm Chart Maker with interactive and JSON modes.

Use without arguments for interactive mode, or with --json=file to supply an
configuration file.

options:
  -h, --help            show this help message and exit
  --json FILENAME       JSON file to parse in non-interactive mode.
  -o OUTDIR, --out-dir OUTDIR
                        The output directory to save the chart to. Defaults to "./out/".
```