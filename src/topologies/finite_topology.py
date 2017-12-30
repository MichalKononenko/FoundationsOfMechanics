"""
Base class for topologies with a finite number of elements
"""
import abc
from typing import Set, TypeVar, Union, FrozenSet, Tuple, Optional
from .product_topology import ProductTopology
from src.interfaces import Topology

T = TypeVar('T')
ANY_SET = Union[Set[T], FrozenSet[T], set]


class FiniteTopology(Topology, metaclass=abc.ABCMeta):
    """
    Base class for topologies with a finite number of elements. This means that
    the open sets of the topology can be iterated through
    """
    @property
    def closed_sets(self) -> ANY_SET:
        """

        :return: The closed sets in the topology
        """
        return frozenset(
            self.elements.difference(open_set) for open_set in self.open_sets
        )

    def get_open_neighborhoods(
            self, point_or_set: Union[T, ANY_SET]
    ) -> Optional[Tuple[ANY_SET]]:
        """

        :param point_or_set: The point or set for which open neighborhoods
            are to be located
        :return: The collection of elements
        """
        if self._is_empty_topology:
            return None

        if self._is_point(point_or_set):
            open_sets = self._get_open_neighborhoods_for_point(point_or_set)
        else:
            open_sets = self._get_open_neighborhoods_for_set(point_or_set)

        return open_sets

    @property
    def _is_empty_topology(self) -> bool:
        """

        :return: True if the topology is empty
        """
        return frozenset(self.open_sets) == frozenset(frozenset())

    def _is_point(self, point_or_set: Union[T, ANY_SET]) -> bool:
        return isinstance(point_or_set, next(iter(self.elements)).__class__)

    def _get_open_neighborhoods_for_point(self, point: T) -> Tuple[ANY_SET]:
        """

        :param point: The point for which open neighborhoods are to be returned
        :return: The open neighborhoods for this point
        """
        return tuple(
            open_set for open_set in self.open_sets if point in open_set
        )

    def _get_open_neighborhoods_for_set(self, set: ANY_SET) -> Tuple[ANY_SET]:
        """

        :param set: The set for which open neighborhoods are to be returned
        :return: The open neighborhoods for this set
        """
        return tuple(
            open_set for open_set in self.open_sets if set.issubset(open_set)
        )

    def __repr__(self) -> str:
        """

        :return: A user-friendly representation of the topology
        """
        return '{0}(elements={1}, open_sets={2})'.format(
            self.__class__.__name__, self.elements, self.open_sets
        )

    def __mul__(self, other: Topology) -> Topology:
        return ProductTopology(self, other)
