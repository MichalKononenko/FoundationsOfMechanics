"""
Responsible for generating a random finite topology and giving back a subset
of elements in that topology. This set is not necessarily open or closed
"""
from hypothesis.strategies import composite, frozensets, sampled_from
from .topologies import topologies as topology_generator
from collections import namedtuple

TopologicalSubset = namedtuple('TopologicalSubset', ['topology', 'subset'])


@composite
def topological_subsets(
        draw, topologies=topology_generator(),
) -> TopologicalSubset:
    topology = draw(topologies)
    return TopologicalSubset(topology, draw(frozensets(
        sampled_from(list(topology.elements))
    )))
