"""
Contains a generator for a basis
"""
from src.interfaces import Basis
from .topologies import topologies
from hypothesis.strategies import composite


@composite
def bases(
        draw, topology=topologies()
) -> Basis:
    """

    :param draw: A function that draws random data
    :param topology: The generator for topologies
    :return: A random basis for the topology
    """
