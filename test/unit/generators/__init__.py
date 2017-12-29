"""
Defines generators for test fixtures
"""
from hypothesis.strategies import composite, integers, frozensets
from src.interfaces import Topology as AbstractTopology
from src.custom_topology import CustomTopology


@composite
def topologies(
        draw, elements=frozensets(integers())
) -> AbstractTopology:
    topol_elements = draw(elements)
    open_sets = set()
    open_sets.add(frozenset())
    open_sets.add(topol_elements)

    return CustomTopology(topol_elements, frozenset(open_sets))
