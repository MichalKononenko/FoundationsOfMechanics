"""
Defines a topological space
"""
import abc
from typing import Set, Generic, TypeVar, FrozenSet, Union, Tuple, Optional

T = TypeVar('T')
ANY_SET = Union[Set[T], FrozenSet[T], set]


class Topology(Generic[T], metaclass=abc.ABCMeta):
    """
    A topology, or topological space, is a two-tuple of a set and a set of sets
    such that

    * The empty set and the set are in the collection of open sets
    * The intersection of any two open sets is in the set
    * The union of any two open sets is in the set
    """
    @property
    @abc.abstractmethod
    def elements(self) -> ANY_SET[T]:
        """

        :return: The elements in this topology
        """
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def open_sets(self) -> ANY_SET[ANY_SET[T]]:
        """

        :return: The open sets in the topology.
        """
        raise NotImplementedError()

    @property
    def closed_sets(self) -> ANY_SET[ANY_SET[T]]:
        """

        :return: The closed sets for the topology. A closed set is a set whose
            complement is an open set
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_open_neighborhoods(
            self, point_or_set: Union[T, ANY_SET]
    ) -> Optional[Tuple[ANY_SET]]:
        """

        :param point_or_set: The point or set for which the open neighborhoods
            are to be obtained
        :return: The collection of open neighborhoods
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def closure(self, subset: ANY_SET[T]) -> ANY_SET[T]:
        """

        :param subset: The subset of the elements of the topology for which
            the closure is to be calculated
        :return: The closure of the set. This is defined as the intersection of
            all closed sets that contain the subset
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def interior(self, subset: ANY_SET[T]) -> ANY_SET[T]:
        """

        :param subset: The subset for which the interior is to be calculated
        :return: The interior of the set. This is the union of all open sets
            that contain the subset
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def boundary(self, subset: ANY_SET[T]) -> ANY_SET[T]:
        """

        :param subset: The subset for which the boundary is to be calculated
        :return: The boundary of the set
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def complement(self, subset: ANY_SET[T]) -> ANY_SET[T]:
        """

        :param subset: The subset of the topology for which the complement
            is to be obtained
        :return: The complement of the set. This is the set of all elements
            in the topology that are not in the subset
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def __mul__(self, other: 'Topology[T]') -> 'Topology[T]':
        """

        :param other: The other topology against which this one is to be
            multiplied
        :return: The product topology
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def __eq__(self, other: 'Topology') -> bool:
        """
        Axiomatic set theory states that two sets are equal iff their elements
        are equal. Using this axiom, let two topologies be equal iff their
        elements and their open sets are equal.

        :param other: The topology against which this is to be compared for
            equality
        :return: True if the topologies are equal, otherwise False
        """
        raise NotImplementedError()
