"""
Defines a finite product topology. This is a product topology formed by
multiplying two finite topologies.
"""
import abc
from .finite_topology import FiniteTopology
from .product_topology import ProductTopology
from typing import TypeVar, Tuple, Set, Generic

X = TypeVar('X')
Y = TypeVar('Y')


class FiniteProductTopology(
    FiniteTopology[Tuple[X, Y]], ProductTopology[X, Y], Generic[X, Y],
    metaclass=abc.ABCMeta
):
    """
    Defines the interface for a topology consisting of the product of two
    finite topologies. The product of two finite topologies is finite. This is
    true because topologies with a finite number of elements have a finite
    number of open sets.
    """
    @property
    @abc.abstractmethod
    def open_rectangles(self) -> Set[Set[Tuple[X, Y]]]:
        """

        :return: The open rectangles on this topology. This is another name for
            the open sets of this topology
        """
        raise NotImplementedError()
