import click

""" Testing Harness for hardware modules of Big Muddy Railroad """

from big_muddy_io import BigMuddyIO
from client_connector_test import client_connector_test
from data_probe import data_probe
from duration_testing import duration_testing
from flow_testing import flow_testing
from load_testing import load_testing
from shift_tester import shift_clock_testing
from wide_client_connector import wide_client_connector_test

COMMAND_OPTIONS = [
    click.option(
        '--check/--no-check',
        default=True,
        help="Should clock loop be checked"
    ),
]


def add_click_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


@click.group()
def harness():
    pass


@harness.command()
def client():
    """Test daisy 8 to 16 client connectors"""
    client_connector_test(BigMuddyIO.system())


@harness.command()
def data():
    """Test daisy root data connections"""
    data_probe(BigMuddyIO.system())


@harness.command()
def duration():
    """Measure bit length of all daisy chains"""
    duration_testing(BigMuddyIO.system())


@harness.command()
@add_click_options(COMMAND_OPTIONS)
def flow(check):
    """Endless data shift of 0001100011..."""
    flow_testing(BigMuddyIO.system(check))


@harness.command()
@add_click_options(COMMAND_OPTIONS)
def load(check):
    """Endless data loading"""
    load_testing(BigMuddyIO.system(check))


@harness.command()
@add_click_options(COMMAND_OPTIONS)
def shifter(check):
    """Endless shift clocking"""
    shift_clock_testing(BigMuddyIO.system(check))


@harness.command()
@click.option("--connector", default=1, help="specify which connector is hooked to test jig")
def wide(connector):
    """Test daisy 16 to 8 client connectors"""
    wide_client_connector_test(BigMuddyIO.system(), connector)


if __name__ == '__main__':
    harness()
