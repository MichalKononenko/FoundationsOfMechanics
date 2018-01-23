"""
Describes objects
"""
from typing import Generic, Container, TypeVar, Hashable, Collection, Iterator

T = TypeVar('T')


class EmptyContainer(Container[T], Generic[T], Hashable):
    """
    Describes an empty container
    """
    def __contains__(self, item: object) -> bool:
        return False

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __eq__(self, other: object) -> bool:
        return hash(self) == hash(other)


class EmptyContainerCollection(Collection[Container[T]], Generic[T]):
    """
    Describes a collection whose only element is the empty container
    """
    def __init__(self) -> None:
        self._elements = {EmptyContainer()}

    def __contains__(self, item: object) -> bool:
        return item in self._elements

    def __len__(self) -> int:
        return 1

    def __iter__(self) -> Iterator[Container[T]]:
        return iter((EmptyContainer(),))


class EmptyCollection(Collection[T], Generic[T]):
    """
    Descries a collection which has no elements
    """
    def __contains__(self, item: object) -> bool:
        return False

    def __len__(self) -> int:
        return 0

    def __iter__(self) -> Iterator[T]:
        raise StopIteration()
