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

    The empty set and the set are in the collection of open sets
    The intersection of any two open sets is in the set
    The union of any two sets is in the set
    """
    @property
    @abc.abstractmethod
    def elements(self) -> ANY_SET:
        """

        :return: The elements in this topology
        """
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def open_sets(self) -> ANY_SET[ANY_SET]:
        """

        :return: The open sets in the topology.
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
