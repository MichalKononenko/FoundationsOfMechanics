"""
Describes an empty topology. This is a topology that has no element, and whose
only open set is an empty set.
"""
from fom.interfaces import Topology
from fom.identity_objects import EmptyContainer, EmptyContainerCollection
from typing import TypeVar, Union, Generic, Container, Tuple, overload

T = TypeVar('T')
Y = TypeVar('Y')


class EmptyTopology(Topology[T], Generic[T]):
    """
    Describes a topology which has no elements, and whose only open set is
    the empty set. In the language of Python containers, this is a topology
    whose element is a container that contains no elements.
    """
    @property
    def elements(self) -> Container[T]:
        return EmptyContainer()

    @property
    def open_sets(self) -> Container[Container[T]]:
        return EmptyContainerCollection()

    @property
    def closed_sets(self):
        return EmptyContainerCollection()

    @overload
    def get_open_neighborhoods(
            self, point_or_set: T
    ) -> Container[Container[T]]:
        """

        :param point_or_set:
        :return:
        """
        pass

    @overload
    def get_open_neighborhoods(
            self, point_or_set: Container[T]
    ) -> Container[Container[T]]:
        """

        :param point_or_set:
        :return:
        """
        pass

    def get_open_neighborhoods(
            self, point_or_set: Union[T, Container[T]]
    ) -> Container[Container[T]]:
        return EmptyContainerCollection()

    def closure(self, subset: Container[T]) -> Container[T]:
        """

        :param subset: The subset for which the closure is to be determined
        :return: The closure. On the empty topology. This is always the empty
            set
        """
        return EmptyContainer()

    def boundary(self, subset: Container[T]) -> Container[T]:
        """

        :param subset: The subset for which the boundary is to be determined
        :return: The empty set
        """
        return EmptyContainer()

    def complement(self, subset: Container[T]) -> Container[T]:
        """

        :param subset: The subset for which the complement is to be obtained
        :return:
        """
        return EmptyContainer()

    def interior(self, subset: Container[T]) -> Container[T]:
        return EmptyContainer()

    def __mul__(self, other: Topology[Y]) -> Topology[Tuple[T, Y]]:
        return other

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)
