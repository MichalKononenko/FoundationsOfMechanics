"""
Defines open rectangles for a product topology
"""
import abc
from .topology import Topology
from typing import Set, Generic, TypeVar, FrozenSet, Union, Tuple, Optional

T = TypeVar('T')
ANY_SET = Union[Set[T], FrozenSet[T], set]


class ProductTopology(Topology, metaclass=abc.ABCMeta):
    """
    A product topology is formed from two topologies by taking the union of the
    set of elements and the union of the open sets of each argument
    """
    @property
    @abc.abstractmethod
    def open_rectangles(self) -> ANY_SET[ANY_SET]:
        raise NotImplementedError()
