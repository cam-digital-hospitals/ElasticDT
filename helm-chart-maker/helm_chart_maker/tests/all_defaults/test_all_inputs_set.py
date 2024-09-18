"""Tests that the generated Helm chart matches the expected output."""

from filecmp import dircmp
import os
from unittest.mock import patch

from helm_chart_maker.__main__ import main

workdir = os.path.dirname(os.path.realpath(__file__))


def test_all_inputs_set():
    """Check that the expected output is generated in the case all inputs are set explicitly."""
    with open(workdir+'/in.txt', 'r', encoding='utf-8') as fp:
        with patch('sys.argv', ['prog', '-o', workdir+'/out']):
            with patch('sys.stdin', fp):
                main()
    x = dircmp(workdir+'/out', workdir+'/expected')
    assert len(x.left_only) == 0, f'Files found only in "out" directory: {x.left_only}'
    assert len(x.right_only) == 0, f'Files found only in "expected" directory: {x.right_only}'
    assert len(x.diff_files) == 0, f'Some files do not match expected output: {x.diff_files}'
