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
):
    """

    :param point: The element to check
    :param neighborhood: The neighborhood to check
    :param topology: The topology of which the neighborhood of the point
        needs to be an open set
    :return: True if the point is in the open neighborhood of the topology
    """
    return is_neighborhood(point, neighborhood) and \
        neighborhood in topology.open_sets
