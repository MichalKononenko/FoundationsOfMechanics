"""
Implements product topologies
"""
from src.interfaces import Topology
from src.interfaces import ProductTopology as ProductTopologyInterface
from itertools import product


class ProductTopology(ProductTopologyInterface):
    """
    Implements the product topology
    """
    def __init__(
            self, first_topology: Topology, second_topology: Topology
    ) -> None:
        self._first = first_topology
        self._second = second_topology

    @property
    def elements(self):
        return self._first.elements.union(self._second.elements)

    @property
    def open_sets(self):
        return frozenset(
            product(self._first.open_sets, self._second.open_sets)
        )

    @property
    def open_rectangles(self):
        return self.open_sets

    @property
    def closed_sets(self):
        return frozenset(
            self.elements.difference(open_set) for open_set in self.open_sets
        )

    def get_open_neighborhoods(self, point_or_set):
        if not isinstance(point_or_set, set):
            set_to_check = frozenset(point_or_set)
        else:
            set_to_check = point_or_set

        return tuple(
            open_set for open_set in self.open_sets if set_to_check.issubset(
                open_set
            )
        )

    def __mul__(self, other: Topology) -> Topology:
        return self.__class__(self, other)

    def __repr__(self) -> str:
        """

        :return: A user-friendly representation of the topology
        """
        return '{0}(elements={1}, open_sets={2})'.format(
            self.__class__.__name__, self.elements, self.open_sets
        )

    def __eq__(self, other: Topology) -> Topology:
        return self.open_sets == other.open_sets
