"""
Provides the most general definition of topological space
"""
import abc
from typing import Generic, TypeVar, Union, Container, Tuple, overload

T = TypeVar('T')
Y = TypeVar('Y')


class Topology(Generic[T], metaclass=abc.ABCMeta):
    """
    A topology, or topological space, is a two-tuple of a set and a set of sets
    such that

    * The empty set and the set are in the collection of open sets
    * The intersection of any two open sets is in the set
    * The union of any two open sets is in the set

    Each element in the set of sets are referred to as open sets

    .. note::

        Since this is the most general type of topology, this interface can
        only provide a class:`python.typing.Container` for the elements and
        open sets. This allows for representations of uncountably-infinite
        topologies. Finite topologies are refined in sub-interfaces.

    .. note::

        The definition of containment is a bit interesting when it comes to
        :class:`python.typing.Container`. This because containers only
        implement the ``__contains__`` function, which only answers whether
        an element is in that container. Therefore, a set contains a container
        iff all elements in that open set are in the container, and there is
        no element in the topology that is in the container, but not in the
        open set. The first table below shows an example of containment being
        ``True``. The second table shows an example of containment being
        ``False``.

    +---------------------+----------------------+-----------------------+
    | Element of Topology | Elements In Open Set | Elements In Container |
    +---------------------+----------------------+-----------------------+
    |       ``a``         |      ``a``           |     ``a``             |
    +---------------------+----------------------+-----------------------+
    |       ``b``         |      ``b``           |     ``b``             |
    +---------------------+----------------------+-----------------------+
    |       ``c``         |      ``c``           |                       |
    +---------------------+----------------------+-----------------------+
    |       ``d``         |                      |                       |
    +---------------------+----------------------+-----------------------+

    +---------------------+----------------------+-----------------------+
    | Element of Topology | Elements In Open Set | Elements In Container |
    +---------------------+----------------------+-----------------------+
    |       ``a``         |      ``a``           |     ``a``             |
    +---------------------+----------------------+-----------------------+
    |       ``b``         |      ``b``           |     ``b``             |
    +---------------------+----------------------+-----------------------+
    |       ``c``         |      ``c``           |                       |
    +---------------------+----------------------+-----------------------+
    |       ``d``         |                      |     ``d``             |
    +---------------------+----------------------+-----------------------+

    """
    @property
    @abc.abstractmethod
    def elements(self) -> Container[T]:
        """

        :return: The elements in this topology
        """
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def open_sets(self) -> Container[Container[T]]:
        """

        :return: The open sets in the topology.
        """
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def closed_sets(self) -> Container[Container[T]]:
        """

        :return: The closed sets for the topology. A closed set is a set whose
            complement is an open set
        """
        raise NotImplementedError()

    @abc.abstractmethod
    @overload
    def get_open_neighborhoods(
            self, point_or_set: T
    ) -> Container[Container[T]]:
        """

        :param point_or_set: The point for which the open neighborhoods
            need to be retrieved
        :return: The open neighborhoods
        """
        pass

    @abc.abstractmethod
    @overload
    def get_open_neighborhoods(
            self, point_or_set: Container[T]
    ) -> Container[Container[T]]:
        """

        :param point_or_set: The set for which open neighborhoods are to be
            obtained
        :return: The open neighborhoods
        """
        pass

    @abc.abstractmethod
    def get_open_neighborhoods(
            self, point_or_set: Union[T, Container[T]]
    ) -> Container[Container[T]]:
        r"""

        :param point_or_set: The point or set for which the open neighborhoods
            are to be obtained
        :return: The open neighborhoods. An open neighborhood :math:`U` for a
            point :math`u` in the topology (:math:`u \in S` where :math:`S` is
            the set of elements in the topology) is the collection of all open
            sets that contain the point.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def closure(self, subset: Container[T]) -> Container[T]:
        """

        :param subset: The subset of the elements of the topology for which
            the closure is to be calculated
        :return: The closure of the set. This is defined as the intersection of
            all closed sets that contain the subset.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def interior(self, subset: Container[T]) -> Container[T]:
        """

        :param subset: The subset for which the interior is to be calculated
        :return: The interior of the set. This is the union of all open sets
            that contain the subset
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def boundary(self, subset: Container[T]) -> Container[T]:
        """

        :param subset: The subset for which the boundary is to be calculated
        :return: The boundary of the set. The boundary of a set is the
            intersection of all closed sets containing the subset.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def complement(self, subset: Container[T]) -> Container[T]:
        """

        :param subset: The subset of the topology for which the complement
            is to be obtained
        :return: The complement of the set. This is the set of all elements
            in the topology that are not in the subset
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def __mul__(self, other: 'Topology[Y]') -> 'Topology[Tuple[T, Y]]':
        """

        :param other: The other topology against which this one is to be
            multiplied
        :return: The product topology formed by multiplying the topologies
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def __eq__(self, other: object) -> bool:
        """
        Axiomatic set theory states that two sets are equal iff their elements
        are equal. Using this axiom, let two topologies be equal iff their
        elements and their open sets are equal.

        :param other: The topology against which this is to be compared for
            equality
        :return: True if the topologies are equal, otherwise False
        """
        raise NotImplementedError()
