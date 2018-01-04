"""
Base class for topologies with a finite number of elements
"""
import abc
from typing import Set, TypeVar, Union, Generic
from .finite_product_topology import FiniteProductTopology
from src.interfaces import Topology
from src.interfaces import FiniteTopology as FiniteTopologyInterface
from src.exceptions import InvalidSubset
from functools import reduce
import operator

T = TypeVar('T')
X = TypeVar('Y')


class FiniteTopology(
    FiniteTopologyInterface[T], Generic[T], metaclass=abc.ABCMeta
):
    """
    Base class for topologies with a finite number of elements. This means that
    the open sets of the topology can be iterated through
    """
    @property
    def closed_sets(self) -> Set[Set[T]]:
        """

        :return: The closed sets in the topology
        """
        closed_sets = frozenset(
            self.complement(open_set) for open_set in self.open_sets
        )  # type: Set[Set[T]]
        return closed_sets

    def get_open_neighborhoods(
            self, point_or_set: Union[T, Set[T]]
    ) -> Set[Set[T]]:
        """

        :param point_or_set: The point or set for which open neighborhoods
            are to be located
        :return: The collection of elements
        """
        if self._is_point(point_or_set):
            open_sets = self._get_open_neighborhoods_for_point(point_or_set)
        else:
            open_sets = self._get_open_neighborhoods_for_set(point_or_set)

        return open_sets

    def complement(self, subset: Set[T]) -> Set[T]:
        """

        :param subset: The subset for which the complement is to be retrieved
        :return: The complement
        """
        self._assert_subset(subset)
        return self.elements.difference(subset)

    def closure(self, subset: Set[T]) -> Set[T]:
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

    def interior(self, subset: Set[T]) -> Set[T]:
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

    def boundary(self, subset: Set[T]) -> Set[T]:
        """

        :param subset: The subset for which the boundary is to be calculated
        :return: The boundary
        """
        self._assert_subset(subset)
        return self.closure(subset) and self.closure(self.complement(subset))

    @property
    def _is_empty_topology(self) -> bool:
        """

        :return: True if the topology is empty
        """
        return frozenset(self.open_sets) == frozenset(frozenset())

    def _is_point(self, point_or_set: Union[T, Set[T]]) -> bool:
        return isinstance(point_or_set, next(iter(self.elements)).__class__)

    def _get_open_neighborhoods_for_point(self, point: T) -> Set[Set[T]]:
        """

        :param point: The point for which open neighborhoods are to be returned
        :return: The open neighborhoods for this point
        """
        neighborhoods = frozenset(
            open_set for open_set in self.open_sets if point in open_set
        )  # type: Set[Set[T]]
        return neighborhoods

    def _get_open_neighborhoods_for_set(self, set_: Set[T]) -> Set[Set[T]]:
        """

        :param set_: The set for which open neighborhoods are to be returned
        :return: The open neighborhoods for this set
        """
        neighborhoods = frozenset(
            open_set for open_set in self.open_sets if open_set.issuperset(
                set_)
        )  # type: Set[Set[T]]
        return neighborhoods

    def _assert_subset(self, subset: Set[T]) -> None:
        """

        Checks that the set is a subset of the elements of the elements of the
        topology. If it is not, raise a :class:`InvalidSubset` error

        :param subset: The argument to check
        """
        if not self.elements.issuperset(subset):
            raise InvalidSubset(
                'The set %s is not a subset of %s' % subset, self.elements
            )

    def __repr__(self) -> str:
        """

        :return: A user-friendly representation of the topology
        """
        return '{0}(elements={1}, open_sets={2})'.format(
            self.__class__.__name__, self.elements, self.open_sets
        )

    def __mul__(
            self, other: FiniteTopologyInterface[X]
    ) -> FiniteProductTopology[T, X]:
        return FiniteProductTopology(self, other)

    def __eq__(self, other: Topology[T]) -> bool:
        return self.open_sets == other.open_sets
