"""
Describes relative topologies. These are subsets of topologies formed by taking
in a topology and a subset, and then intersecting the open sets with the
subsets
"""
from fom.interfaces import Topology
from fom.topologies.finite_topology import FiniteTopology
from typing import Set, TypeVar, Union, FrozenSet
from fom.exceptions import InvalidSubset

T = TypeVar('T')
ANY_SET = Union[Set[T], FrozenSet[T], set]


class RelativeTopology(FiniteTopology):
    """
    Defines a topology relative to another by finding the intersection of the
    open sets of a topology with a subset of the other topology
    """
    def __init__(self, subset: ANY_SET, topology: Topology[T]) -> None:
        """

        :param subset: The subset of elements to extract from the topology
        :param topology: The base topology
        """
        self._assert_is_subset(subset, topology)
        self._elements = subset
        self._open_sets = frozenset(
            subset.intersection(open_set) for open_set in topology.open_sets
        )

    @staticmethod
    def _assert_is_subset(subset: ANY_SET, topology: Topology[T]):
        if not subset.issubset(topology.elements):
            raise InvalidSubset(
                'Set %s is not a subset of the elements of %s' %
                (subset, topology)
            )

    @property
    def elements(self) -> ANY_SET:
        """

        :return: The elements of the topology
        """
        return self._elements

    @property
    def open_sets(self) -> ANY_SET[ANY_SET]:
        """

        :return: The topology's open sets
        """
        return self._open_sets
