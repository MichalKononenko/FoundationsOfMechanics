"""
Describes a topology that contains a finite number of elements, and therefore
a finite number of open sets
"""
import abc
from .topology import Topology, T, Y
from typing import Union, Generic, Container, Collection, Tuple, overload


class FiniteTopology(Topology[T], Generic[T], metaclass=abc.ABCMeta):
    """
    Describes the interface for a topology with a finite number of open sets.
    This method specializes the return types in the topology interface for
    types that are better-suited to handling finite containers.

    """
    @property
    @abc.abstractmethod
    def elements(self) -> Collection[T]:
        """

        :return: The elements in the topology
        """
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def open_sets(self) -> Collection[Collection[T]]:
        """

        :return: The open sets in the topology
        """
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def closed_sets(self) -> Collection[Collection[T]]:
        """

        :return: The closed sets for the topology. A closed set is a set whose
            complement is an open set
        """
        raise NotImplementedError()

    @abc.abstractmethod
    @overload
    def get_open_neighborhoods(
            self, point_or_set: T
    ) -> Collection[Collection[T]]:
        pass

    @abc.abstractmethod
    @overload
    def get_open_neighborhoods(
            self, point_or_set: Container[T]
    ) -> Collection[Collection[T]]:
        pass

    @abc.abstractmethod
    def get_open_neighborhoods(
            self, point_or_set: Union[T, Container[T]]
    ) -> Collection[Collection[T]]:
        """

        :param point_or_set: The point or set for which the open neighborhoods
            are to be obtained
        :return: The open neighborhoods. An open neighborhood :math:`U` for a
            point :math`u` in the topology (:math:`u \in S` where :math:`S` is
            the set of elements in the topology) is the Set of all open
            sets that contain the point.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def closure(self, subset: Container[T]) -> Collection[T]:
        """

        :param subset: The subset of the elements of the topology for which
            the closure is to be calculated
        :return: The closure of the set. This is defined as the intersection of
            all closed sets that contain the subset
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def interior(self, subset: Container[T]) -> Collection[T]:
        """

        :param subset: The subset for which the interior is to be calculated
        :return: The interior of the set. This is the union of all open sets
            that contain the subset
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def boundary(self, subset: Container[T]) -> Collection[T]:
        """

        :param subset: The subset for which the boundary is to be calculated
        :return: The boundary of the set. The boundary of a set is the
            intersection of all closed sets containing the subset.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def complement(self, subset: Container[T]) -> Collection[T]:
        """

        :param subset: The subset of the topology for which the complement
            is to be obtained
        :return: The complement of the set. This is the set of all elements
            in the topology that are not in the subset
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def __mul__(self, other: Topology[Y]) -> Topology[Tuple[T, Y]]:
        """

        :param other: The other topology against which this one is to be
            multiplied
        :return: The product topology
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def __eq__(self, other: object) -> bool:
        """
        Axiomatic set theory states that two sets are equal iff their elements
        are equal. Using this axiom, let two topologies be equal iff their
        elements and their open sets are equal.

        :param other: The topology against which this is to be compared for
            equality
        :return: True if the topologies are equal, otherwise False
        """
        raise NotImplementedError()
