"""
Describes how to generate a random topology from a set of elements
"""
from src.interfaces import Topology as AbstractTopology
from typing import Set, TypeVar, Union, FrozenSet, Optional
from random import randint, sample

T = TypeVar('T')
ANY_SET = Union[Set[T], FrozenSet[T], set]


class RandomTopology(AbstractTopology):
    """
    Describes a topology where the open sets are made randomly using the
    following algorithm

    Add the empty set and set of elements to the set of open sets
    Make two sets of random length from the provided elements
    Add the random sets, their union, and their intersection
    Repeat until the desired number of open sets are made
    """
    def __init__(
            self,
            elements: ANY_SET,
            number_of_randomizing_rounds: int=5
    ):
        """

        :param elements: The set of elements from which the number of sets is
        to be obtained
        :param number_of_randomizing_rounds: The number of rounds with which
        the topology is to be randomized
        """
        open_sets = set()
        open_sets.add(frozenset())
        open_sets.add(frozenset(elements))

        for _ in range(0, number_of_randomizing_rounds):
            self._add_to_open_sets(elements, open_sets)

        self._elements = elements
        self._open_sets = open_sets

    @staticmethod
    def _add_to_open_sets(elements: ANY_SET, open_sets: Set[ANY_SET]) -> None:
        first_random_set = frozenset(
            sample(elements, randint(0, len(elements)))
        )
        second_random_set = frozenset(
            sample(elements, randint(0, len(elements)))
        )
        open_sets.add(first_random_set)
        open_sets.add(second_random_set)
        open_sets.add(first_random_set.union(second_random_set))
        open_sets.add(first_random_set.intersection(second_random_set))

    @property
    def elements(self) -> ANY_SET:
        """

        :return: The elements of the topology
        """
        return self._elements

    @property
    def open_sets(self) -> ANY_SET[ANY_SET]:
        """

        :return: The open sets
        """
        return self._open_sets
