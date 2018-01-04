"""
Implements product topologies
"""
from src.interfaces import Topology, T, ANY_SET
from src.interfaces import ProductTopology as ProductTopologyInterface
from src.exceptions import InvalidSubset
from itertools import product
from functools import reduce
import operator


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

    def complement(self, subset: ANY_SET[T]) -> ANY_SET[T]:
        """

        :param subset: The subset for which the complement is to be retrieved
        :return: The complement
        """
        self._assert_subset(subset)
        return self.elements.difference(subset)

    def closure(self, subset: ANY_SET[T]) -> ANY_SET[T]:
        """

        :param subset: The subset for which the closure is to be calculated
        :return: The closure
        """
        self._assert_subset(subset)
        s = frozenset(subset)
        return reduce(
            operator.and_,
            filter(s.issubset, self.closed_sets),
            set()
        )

    def interior(self, subset: ANY_SET[T]) -> ANY_SET[T]:
        """

        :param subset: The subset for which the interior is to be calculated
        :return: The interior
        """
        self._assert_subset(subset)
        return reduce(
            operator.or_,
            filter(subset.issubset, self.open_sets),
            set()
        )

    def boundary(self, subset: ANY_SET[T]) -> ANY_SET[T]:
        """

        :param subset: The subset for which the boundary is to be calculated
        :return: The boundary
        """
        self._assert_subset(subset)
        return self.closure(subset) and self.closure(self.complement(subset))

    def _assert_subset(self, subset: ANY_SET[T]) -> None:
        """

        :param subset:
        :return:
        """
        if not self.elements.issuperset(subset):
            raise InvalidSubset(
                'The set %s is not a subset of %s' % subset, self.elements
            )

    def __mul__(self, other: Topology) -> Topology:
        return self.__class__(self, other)

    def __repr__(self) -> str:
        """

        :return: A user-friendly representation of the topology
        """
        return '{0}(elements={1}, topological_subsets.py={2})'.format(
            self.__class__.__name__, self.elements, self.open_sets
        )

    def __eq__(self, other: Topology) -> Topology:
        return self.open_sets == other.open_sets
