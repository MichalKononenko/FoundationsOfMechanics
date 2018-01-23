from hypothesis.strategies import composite, integers, frozensets
from fom.interfaces import FiniteTopology as AbstractTopology
from fom.topologies import RandomTopology


@composite
def topologies(
        draw, elements=frozensets(integers()), number_of_rounds=5
) -> AbstractTopology[int]:
    """

    :param draw: A function provided by the hypothesis library that knows how
        to sample from a generator
    :param elements: A generator of sets of elements from which the topology
        is to be built
    :param number_of_rounds: The number of randomization rounds for which the
        topology is to be built
    :return: A random topology
    """
    return RandomTopology(draw(elements), number_of_rounds)
