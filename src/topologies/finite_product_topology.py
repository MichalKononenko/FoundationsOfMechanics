"""
Implements product topologies
"""
from src.interfaces import FiniteProductTopology as FPTInterface
from src.interfaces import FiniteTopology
from src.exceptions import InvalidSubset
from itertools import product
from typing import Generic, TypeVar, Set, Tuple, Union
from functools import reduce
import operator

X = TypeVar('X')
Y = TypeVar('Y')
T = TypeVar('T')


class FiniteProductTopology(FPTInterface[X, Y], Generic[X, Y]):
    """
    Implements the product topology
    """
    def __init__(
            self,
            first_topology: FiniteTopology[X],
            second_topology: FiniteTopology[Y]
    ) -> None:
        """

        :param first_topology: The left-hand-side of the multiplicand
        :param second_topology: The right-hand side of the multiplication
        """
        self._first = first_topology
        self._second = second_topology

    @property
    def elements(self) -> Set[Tuple[X, Y]]:
        elements_ = frozenset(
            product(self._first.elements, self._second.elements)
        )  # type: Set[Tuple[X, Y]]
        return elements_

    @property
    def open_sets(self) -> Set[Set[Tuple[X, Y]]]:
        open_sets_ = frozenset(
            product(self._first.open_sets, self._second.open_sets)
        )  # type: Set[Set[Tuple[X, Y]]]
        return open_sets_

    @property
    def open_rectangles(self) -> Set[Set[Tuple[X, Y]]]:
        return self.open_sets

    @property
    def closed_sets(self) -> Set[Tuple[X, Y]]:
        closed_sets = frozenset(
            self.complement(open_set) for open_set in self.open_sets
        )  # type: Set[Tuple[X, Y]]
        return closed_sets

    def get_open_neighborhoods(
            self, point_or_set: Union[Tuple[X, Y], Set[Tuple[X, Y]]]
    ) -> Set[Set[Tuple[X, Y]]]:
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

    def complement(self, set_: Set[Tuple[X, Y]]) -> Set[Tuple[X, Y]]:
        """

        :param set_: The set for which the complement is to be checked
        :return: The complement of the set
        """
        self._assert_subset(set_)
        return self.elements.difference(set_)

    def closure(self, set_: Set[Tuple[X, Y]]) -> Set[Tuple[X, Y]]:
        """

        :param set_: The set for which the closure is to be retrieved
        :return: The closure of the set
        """
        self._assert_subset(set_)
        return reduce(
            operator.and_,
            filter(set_.issubset, self.closed_sets),
            set()
        )

    def interior(self, set_: Set[Tuple[X, Y]]) -> Set[Tuple[X, Y]]:
        self._assert_subset(set_)
        return reduce(
            operator.or_,
            filter(set_.issubset, self.open_sets),
            set()
        )

    def boundary(self, set_: Set[Tuple[X, Y]]) -> Set[Tuple[X, Y]]:
        self._assert_subset(set_)
        return self.closure(set_) and self.closure(self.complement(set_))

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

    def _assert_subset(self, subset: Set[Tuple[X, Y]]) -> None:
        """

        :param subset:
        :return:
        """
        if not self.elements.issuperset(subset):
            raise InvalidSubset(
                'The set %s is not a subset of %s' % subset, self.elements
            )

    def __eq__(self, other: 'FiniteProductTopology[X, Y]') -> bool:
        """

        :param other: The topology against which this topology is to be
            compared
        :return: True if the topologies are equal, otherwise False
        """
        return self.open_sets == other.open_sets

    def __mul__(
            self, other: FiniteTopology[T]
    ) -> 'FiniteProductTopology[Tuple[Tuple[X, Y], T]]':
        """

        :param other: The topology with which this topology is to be multiplied
        :return: The product of the topologies
        """
        return self.__class__(self, other)

    def __repr__(self) -> str:
        """

        :return: A user-friendly representation of the topology
        """
        return '{0}(elements={1}, topological_subsets.py={2})'.format(
            self.__class__.__name__, self.elements, self.open_sets
        )
