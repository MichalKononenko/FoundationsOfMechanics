"""
Defines a topology where sets and open sets are given by the user on
construction
"""
from fom.topologies.abc.finite_topology import FiniteTopology
from typing import Set, TypeVar, Union, FrozenSet
from fom.exceptions import InvalidOpenSets

T = TypeVar('T')
ANY_SET = Union[Set[T], FrozenSet[T], set]


class CustomTopology(FiniteTopology):
    """
    Implements a topology where open sets and elements are given by the user
    """
    def __init__(self, elements: ANY_SET, open_sets: ANY_SET):
        """

        :param elements: The elements of the topology
        :param open_sets: The open sets in the topology
        """
        self._elements = frozenset(elements)
        self._open_sets = frozenset(open_sets)

        self._assert_first_axiom(elements, open_sets)
        self._assert_second_axiom(open_sets)
        self._assert_third_axiom(open_sets)

    @property
    def elements(self) -> ANY_SET:
        """

        :return: The elements of the topology
        """
        return self._elements

    @property
    def open_sets(self) -> ANY_SET[ANY_SET]:
        """

        :return: The open sets in the topology
        """
        return self._open_sets

    @staticmethod
    def _assert_first_axiom(
            elements: ANY_SET,
            open_sets: ANY_SET[ANY_SET]
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
