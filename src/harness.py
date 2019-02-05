import click

from client_connector_test import client_connector_test
from data_probe import data_probe
from duration_testing import duration_testing
from flow_testing import flow_testing
from load_testing import load_testing
from shift_tester import shift_clock_testing


@click.group()
def harness():
    pass


@harness.command()
def client():
    """Test daisy 8 to 16 client connectors"""
    client_connector_test()


@harness.command()
def data():
    """Test daisy root data connections"""
    data_probe()


@harness.command()
def duration():
    """Measure bit length of all daisy chains"""
    duration_testing()


@harness.command()
def flow():
    """Endless data shift of 0001100011..."""
    flow_testing()


@harness.command()
def load():
    """Endless data loading"""
    load_testing()


@harness.command()
def shifter():
    """Endless shift clocking"""
    shift_clock_testing()


if __name__ == '__main__':
    harness()
