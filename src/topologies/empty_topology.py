from src.interfaces import Topology
from typing import Set, TypeVar, Union, FrozenSet, Tuple, Optional

T = TypeVar('T')
ANY_SET = Union[Set[T], FrozenSet[T], set]


class EmptyTopology(Topology):
    @property
    def elements(self):
        return set()

    @property
    def open_sets(self):
        return frozenset(frozenset())

    @property
    def closed_sets(self):
        return frozenset(frozenset())

    def get_open_neighborhoods(
            self, point_or_set: Union[T, ANY_SET]
    ):
        return set()

    def __mul__(self, other: Topology) -> Topology:
        return other

