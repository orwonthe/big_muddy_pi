import click

from big_muddy.clocking_checker import ClockingChecker

""" Testing Harness for hardware modules of Big Muddy Railroad """

from big_muddy.big_muddy_io import BigMuddyIO
from big_muddy.client_connector_test import client_connector_test
from big_muddy.data_probe import data_probe
from big_muddy.duration_testing import duration_testing
from big_muddy.flow_testing import flow_testing
from big_muddy.load_testing import load_testing
from big_muddy.shift_tester import shift_clock_testing
from big_muddy.wide_client_connector import wide_client_connector_test

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
@add_click_options(COMMAND_OPTIONS)
def flow(check):
    """Endless data shift of 0001100011..."""
    ClockingChecker.set_raise_clock_exceptions(check)
    flow_testing()


@harness.command()
@add_click_options(COMMAND_OPTIONS)
def load(check):
    """Endless data loading"""
    ClockingChecker.set_raise_clock_exceptions(check)
    load_testing(BigMuddyIO.system())


@harness.command()
@add_click_options(COMMAND_OPTIONS)
def shifter(check):
    """Endless shift clocking"""
    ClockingChecker.set_raise_clock_exceptions(check)
    shift_clock_testing()


@harness.command()
@click.option("--connector", default=1, help="specify which connector is hooked to test jig")
def wide(connector):
    """Test daisy 16 to 8 client connectors"""
    wide_client_connector_test(connector)


if __name__ == '__main__':
    harness()
