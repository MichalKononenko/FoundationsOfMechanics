"""
Encodes the idea of an open neighborhood.
"""
from src.interfaces import Topology
from typing import TypeVar, Union, Set, FrozenSet

T = TypeVar('T')
ANY_SET = Union[Set[T], FrozenSet[T], set]


def is_neighborhood(point: T, set_to_check: ANY_SET) -> bool:
    """

    :param point: The point to check
    :param set_to_check: The open set
    :return: True if the set is a neighborhood of the point
    """
    return point in set_to_check


def is_open_neighborhood(
        point: T, neighborhood: ANY_SET, topology: Topology[T]
) -> bool:
    """

    :param point: The element to check
    :param neighborhood: The neighborhood to check
    :param topology: The topology of which the neighborhood of the point
        needs to be an open set
    :return: True if the point is in the open neighborhood of the topology
    """
    return is_neighborhood(point, neighborhood) and \
        neighborhood in topology.open_sets


def is_set_open_neighborhood(
        subset: ANY_SET, neighborhood: ANY_SET, topology: Topology[T]
) -> bool:
    """
    A subset of a topology can also be an open neighborhood. A set
    :math:`U` is an open neighborhood of another set :math:`A` iff
    :math:`U` is open, and :math:`A \subset U`

    :param subset: The subset to check for being an open neighborhood
    :param neighborhood: The open set to check
    :param topology: The topology to check
    :return: True if the set is an open neighborhood
    """
    return subset.issubset(neighborhood) and \
        neighborhood in topology.open_sets
