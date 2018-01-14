"""
Defines a basis where the open sets of the basis are provided by the user
on construction
"""
from fom.interfaces import Basis as BasisInterface
from fom.interfaces import Topology
from fom.exceptions import InvalidOpenSets
from typing import Set, TypeVar, FrozenSet, Union, Iterator

T = TypeVar('T')
ANY_SET = Union[Set[T], FrozenSet[T], set]


class CustomBasis(BasisInterface):
    """
    Base class for a basis where open sets are provided by the user
    """
    def __init__(
            self,
            basis_sets: ANY_SET[ANY_SET[T]],
            topology: Topology[T]
    ) -> None:
        """

        :param basis_sets: The basis sets
        :param topology: The topology for which the basis is made
        """
        self._check_open_sets(basis_sets, topology)
        self._basis_sets = basis_sets
        self._topology = topology

    @property
    def topology(self) -> Topology[T]:
        """

        :return: The topology for the basis
        """
        return self._topology

    @staticmethod
    def _check_open_sets(
            basis_sets: ANY_SET[ANY_SET[T]],
            topology: Topology[T]
    ) -> None:
        """
        Check that each basis set in this basis is an open set of the topology

        :param basis_sets: The basis sets to use for the check
        :param topology: The topology against which the basis is to be checked
        """
        for basis_set in basis_sets:
            if basis_set not in topology.open_sets:
                raise InvalidOpenSets(
                    'The basis set %s is not an open set of the topology %s' %
                    (basis_set, topology)
                )

    def __contains__(self, item: ANY_SET[T]) -> bool:
        """

        :param item: The open set to check for whether it is in a given basis
        :return: True if the open set is in this basis
        """
        return item in self._basis_sets

    def __len__(self) -> int:
        """

        :return: The number of open sets in the basis
        """
        return len(self._basis_sets)

    def __iter__(self) -> Iterator[T]:
        """

        :return: An iterator over the open sets in the basis
        """
        return iter(self._basis_sets)
