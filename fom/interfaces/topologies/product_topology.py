"""
Defines open rectangles for a product topology
"""
import abc
from .topology import Topology
from typing import TypeVar, Container, Generic, Tuple

X = TypeVar('X')
Y = TypeVar('Y')


class ProductTopology(
    Topology[Tuple[X, Y]], Generic[X, Y], metaclass=abc.ABCMeta
):
    """
    A product topology is formed from two topologies by taking the union of the
    set of elements and the union of the open sets of each argument.

    The act of multiplying two topologies introduces a tuple structure on the
    elements on the topology, since multiplication of topologies does not
    commute.

    Topological multiplication is non-associative.
    """
    @property
    @abc.abstractmethod
    def open_rectangles(self) -> Container[Container[Tuple[X, Y]]]:
        """
        Alias for the open sets of a product topology

        :return: The open sets of the product topology
        """
        raise NotImplementedError()
