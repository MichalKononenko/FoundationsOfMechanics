"""
Defines an abstract class for a topology that includes basic operations on
the containers used to define it.
"""
import abc
from typing import Generic, Container, TypeVar, Tuple, cast

T = TypeVar('T')
X = TypeVar('X')
Y = TypeVar('Y')


class Topology(Generic[T], metaclass=abc.ABCMeta):
    """
    Base class for topologies, defining unions and intersections of containers.
    """
    @property
    @abc.abstractmethod
    def elements(self) -> Container[T]:
        """

        :return: The container of elements
        """
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def open_sets(self) -> Container[Container[T]]:
        """

        :return: The open sets
        """
        raise NotImplementedError()

    class Intersection(Container[T]):
        """
        Defines the intersection of two containers
        """
        def __init__(
                self,
                first_container: Container[T],
                second_container: Container[T]
        ) -> None:
            self._first = first_container
            self._second = second_container

        def __contains__(self, item: object) -> bool:
            t_item = cast(T, item)
            return t_item in self._first and t_item in self._second

        def __repr__(self) -> str:
            """

            :return:
            """
            return '{0}(first_container={1}, second_container={2})'.format(
                self.__class__.__name__, self._first, self._second
            )

    class Product(Container[Tuple[X, Y]], Generic[X, Y]):
        """
        Defines the intersection of two containers. Membership in this
        container is the logical and of membership in either container
        """
        def __init__(
                self,
                first_container: Container[X],
                second_container: Container[Y]
        ) -> None:
            """

            :param first_container: The left side of the composition
            :param second_container: The right side of the composition
            """
            self._first = first_container
            self._second = second_container

        def __contains__(self, item: object) -> bool:
            """

            :param item: The object to test for membership
            :return: ``True`` if the first element of the tuple is in the first
                container and the second element is in the second container
            """
            t_item = cast(Tuple[X, Y], item)
            return t_item[0] in self._first and t_item[1] in self._second

        def __repr__(self) -> str:
            """

            :return: The arguments used to create an instance of this class
            """
            return '{0}(first_container={1}, second_container={2})'.format(
                self.__class__.__name__, self._first, self._second
            )

    class Union(Container[T]):
        """
        Defines a union between two containers. An item is in the union of two
        containers if it is in either container
        """
        def __init__(
                self,
                first_container: Container[T],
                second_container: Container[T]
        ) -> None:
            self._first = first_container
            self._second = second_container

        def __contains__(self, item: object) -> bool:
            """

            :param item: The item to check for membership
            :return: ``True`` if the item is in the container, otherwise false
            """
            return item in self._first or item in self._second

        def __repr__(self) -> str:
            """

            :return: A user-friendly representation of the container
            """
            return '%s(first_container=%s, second_container=%s)' % (
                self.__class__.__name__, self._first, self._second
            )
