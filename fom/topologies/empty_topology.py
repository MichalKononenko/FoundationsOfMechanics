from fom.interfaces import Topology
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

    @property
    def _empty_set(self) -> ANY_SET[T]:
        return frozenset()

    def get_open_neighborhoods(
            self, point_or_set: Union[T, ANY_SET]
    ):
        return set()

    def closure(self, subset: ANY_SET[T]) -> ANY_SET[T]:
        """

        :param subset: The subset for which the closure is to be determined
        :return:
        """
        return self._empty_set

    def boundary(self, subset: ANY_SET[T]) -> ANY_SET[T]:
        return self._empty_set

    def complement(self, subset: ANY_SET[T]) -> ANY_SET[T]:
        return self._empty_set

    def interior(self, subset: ANY_SET[T]) -> ANY_SET[T]:
        return self._empty_set

    def __mul__(self, other: Topology) -> Topology:
        return other

    def __eq__(self, other: Topology) -> bool:
        return isinstance(other, self.__class__)
