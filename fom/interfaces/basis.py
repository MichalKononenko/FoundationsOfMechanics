"""
A basis for a topology is a collection of open sets such that every open set is
a union of elements of the basis set
"""
import abc
from collections.abc import Collection
from typing import Set, Generic, TypeVar, FrozenSet, Union
from fom.interfaces.topologies.topology import Topology

T = TypeVar('T')
ANY_SET = Union[Set[T], FrozenSet[T], set]


class Basis(Collection, Generic[T], metaclass=abc.ABCMeta):
    """
    Base class for the basis of a topology. Bases are collections of open sets
    such that every open set in the topology can be expressed as a union of
    the basis sets.
    """
    @property
    @abc.abstractmethod
    def topology(self) -> Topology[T]:
        """

        :return: The topology with which this basis is associated
        """
        raise NotImplementedError()
