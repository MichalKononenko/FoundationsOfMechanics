from hypothesis.strategies import composite, integers, frozensets
from src.interfaces import Topology as AbstractTopology
from src.topologies import RandomTopology


@composite
def topologies(
        draw, elements=frozensets(integers()), number_of_rounds=5
) -> AbstractTopology:
    return RandomTopology(draw(elements), number_of_rounds)
