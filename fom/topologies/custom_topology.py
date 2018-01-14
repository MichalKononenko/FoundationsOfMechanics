"""
Defines a topology where sets and open sets are given by the user on
construction
"""
from fom.topologies.abc.finite_topology import FiniteTopology
from typing import Set, TypeVar, Union, Collection
from fom.exceptions import InvalidOpenSets

T = TypeVar('T')


class CustomTopology(FiniteTopology):
    """
    Implements a topology where open sets and elements are given by the user
    """
    def __init__(
            self, elements: Set[T], open_sets: Set[Set[T]]
    ) -> None:
        """

        :param elements: The elements of the topology
        :param open_sets: The open sets in the topology
        """
        self._elements = elements
        self._open_sets = open_sets

        self._assert_first_axiom(elements, open_sets)
        self._assert_second_axiom(open_sets)
        self._assert_third_axiom(open_sets)

    @property
    def elements(self) -> Set[T]:
        """

        :return: The elements of the topology
        """
        return self._elements

    @property
    def open_sets(self) -> Set[Set[T]]:
        """

        :return: The open sets in the topology
        """
        return self._open_sets

    @staticmethod
    def _assert_first_axiom(
            elements: Set[T],
            open_sets: Set[Set[T]]
    ) -> None:
        if (set() not in open_sets) or (frozenset() not in open_sets):
            raise InvalidOpenSets(
                'The open sets given do not contain the empty set'
            )
        if elements not in open_sets:
            raise InvalidOpenSets(
                'The open sets given do not contain the set of all elements'
            )

    @staticmethod
    def _assert_second_axiom(open_sets: Set[Set[T]]) -> None:
        for first_set in open_sets:
            for second_set in open_sets:
                if first_set.intersection(second_set) not in open_sets:
                    raise InvalidOpenSets(
                        'The intersection of the sets {0} and {1} is not an '
                        'open set in {2}'.format(
                            first_set, second_set, open_sets
                        )
                    )

    @staticmethod
    def _assert_third_axiom(open_sets: Set[Set[T]]) -> None:
        for first_set in open_sets:
            for second_set in open_sets:
                if first_set.union(second_set) not in open_sets:
                    raise InvalidOpenSets(
                        'The union of the sets {0} and {1} is not an open set '
                        'in {2}'.format(first_set, second_set, open_sets)
                    )
