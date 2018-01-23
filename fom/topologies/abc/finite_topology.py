"""
Base class for topologies with a finite number of elements
"""
import abc
from typing import Set, TypeVar, Union, Generic, Collection, Container
from typing import Iterator, Tuple, cast, Iterable
from fom.topologies.finite_product_topology import FiniteProductTopology
from fom.topologies.abc.topology import Topology as AbstractTopology
from fom.interfaces import Topology
from fom.interfaces import FiniteTopology as FiniteTopologyInterface
from fom.exceptions import InvalidSubset
from functools import reduce
import operator
import itertools

T = TypeVar('T')
X = TypeVar('X')
Y = TypeVar('Y')
E = TypeVar('E')


class FiniteTopology(
    FiniteTopologyInterface[T], Generic[T], metaclass=abc.ABCMeta
):
    """
    Base class for topologies with a finite number of elements.
    Since these topologies have finite elements, then they must also have a
    finite number of open sets, since the most open sets that a topology can
    have is equal to the power set of the elements. Elements and open sets
    can be iterated through in a finite topology
    """
    @property
    @abc.abstractmethod
    def elements(self) -> Collection[T]:
        """

        :return: The set of elements in the topology
        """
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def open_sets(self) -> Collection[Collection[T]]:
        """

        :return: The open sets in the topology
        """
        raise NotImplementedError()

    @property
    def closed_sets(self) -> Collection[Collection[T]]:
        """

        :return: The closed sets in the topology. A set is a closed set iff its
            complement is an open set.
        """
        return self._ClosedSets(self)

    def get_open_neighborhoods(
            self, point_or_set: Union[T, Set[T]]
    ) -> Set[Set[T]]:
        """

        :param point_or_set: The point or set for which open neighborhoods
            are to be located
        :return: The collection of elements
        """
        if self._is_point(point_or_set):
            open_sets = self._get_open_neighborhoods_for_point(point_or_set)
        else:
            open_sets = self._get_open_neighborhoods_for_set(point_or_set)

        return open_sets

    def complement(self, subset: Container[T]) -> Collection[T]:
        """

        :param subset: The subset for which the complement is to be retrieved
        :return: The complement
        """
        return self._Complement(self, subset)

    def closure(self, subset: Container[T]) -> Collection[T]:
        """

        :param subset: The subset for which the closure is to be calculated
        :return: The closure
        """
        closed_sets_containing_subset = (
            closed_set for closed_set in self.closed_sets
            if self._collection_contains_container(closed_set, subset)
        )
        return reduce(
            lambda x, y: self.Intersection(x, y),
            closed_sets_containing_subset,
            self.elements
        )

    def interior(self, subset: Set[T]) -> Set[T]:
        """

        :param subset: The subset for which the interior is to be calculated
        :return: The interior
        """
        self._assert_subset(subset)
        return reduce(
            operator.or_,
            filter(subset.issubset, self.open_sets),
            set()
        )

    def boundary(self, subset: Container[T]) -> Collection[T]:
        """

        :param subset: The subset for which the boundary is to be calculated
        :return: The boundary
        """
        return self.Intersection(
            self.closure(subset), self.closure(self.complement(subset))
        )

    @property
    def _is_empty_topology(self) -> bool:
        """

        :return: True if the topology is empty
        """
        return frozenset(self.open_sets) == frozenset(frozenset())

    def _is_point(self, point_or_set: Union[T, Set[T]]) -> bool:
        return isinstance(point_or_set, next(iter(self.elements)).__class__)

    def _get_open_neighborhoods_for_point(self, point: T) -> Set[Set[T]]:
        """

        :param point: The point for which open neighborhoods are to be returned
        :return: The open neighborhoods for this point
        """
        neighborhoods = frozenset(
            open_set for open_set in self.open_sets if point in open_set
        )  # type: Set[Set[T]]
        return neighborhoods

    def _get_open_neighborhoods_for_set(self, set_: Set[T]) -> Set[Set[T]]:
        """

        :param set_: The set for which open neighborhoods are to be returned
        :return: The open neighborhoods for this set
        """
        neighborhoods = frozenset(
            open_set for open_set in self.open_sets if open_set.issuperset(
                set_)
        )  # type: Set[Set[T]]
        return neighborhoods

    def _assert_subset(self, subset: Set[T]) -> None:
        """

        Checks that the set is a subset of the elements of the elements of the
        topology. If it is not, raise a :class:`InvalidSubset` error

        :param subset: The argument to check
        """
        if not self.elements.issuperset(subset):
            raise InvalidSubset(
                'The set %s is not a subset of %s' % subset, self.elements
            )

    def _collection_contains_container(
            self, collection: Collection[T], container: Container[T]
    ) -> bool:
        """
        Checks that a collection contains a container. Define a collection as
        containing a container if and only if no elements in the topology that
        are not in the collection are in the container

        :param collection:
        :param container:
        :return:
        """
        elements_outside_container = {
            element for element in self.elements
            if element in collection and element not in container
        }
        return len(elements_outside_container) == 0

    def __repr__(self) -> str:
        """

        :return: A user-friendly representation of the topology
        """
        return '{0}(elements={1}, open_sets={2})'.format(
            self.__class__.__name__, self.elements, self.open_sets
        )

    def __mul__(
            self, other: FiniteTopologyInterface[X]
    ) -> FiniteProductTopology[T, X]:
        return FiniteProductTopology(self, other)

    def __eq__(self, other: Topology[T]) -> bool:
        return self.open_sets == other.open_sets

    class _FiniteCollection(
            Collection[E], Generic[E], metaclass=abc.ABCMeta
    ):
        """
        Abstract class representing a finite collection of elements that can
        be equated to other elements
        """
        def __eq__(self, other: object) -> bool:
            """
            Equality test. As per the axiom of set theory, a set is equal to
            another set if and only if all elements in the set are equal to
            each other. The first part of the equality test checks if the other
            object is iterable. The second part iterates through it and checks
            if all elements are equal.

            The equality test runs in linear time.

            :param other: The object to check for equality
            :return: ``True`` if the objects are equal to each other
            """
            are_equal = False

            if hasattr(other, '__iter__'):
                cast_other = cast(Iterable[T], other)
                are_equal = set(self) == set(cast_other)

            return are_equal

        def __hash__(self) -> int:
            return hash(iter(self))

    class Intersection(_FiniteCollection[T], AbstractTopology.Intersection):
        """
        Refine intersections to include iteration and containment as well
        """
        def __init__(
                self,
                first_collection: Collection[T],
                second_collection: Collection[T]
        ) -> None:
            super(FiniteTopology.Intersection, self).__init__(
                first_collection, second_collection
            )
            self._combined_elements = frozenset(
                filter(
                    lambda x: x in first_collection and x in second_collection,
                    itertools.chain(first_collection, second_collection)
                )
            )

        def __iter__(self) -> Iterator[T]:
            """

            :return: An iterator iterating through the elements in the
                intersection
            """
            return iter(self._combined_elements)

        def __len__(self) -> int:
            return len(self._combined_elements)

    class Union(_FiniteCollection[T], AbstractTopology.Union):
        def __init__(
                self,
                first_collection: Collection[T],
                second_collection: Collection[T]
        ) -> None:
            super(FiniteTopology.Union, self).__init__(
                first_collection, second_collection
            )
            self._combined_elements = frozenset(
                itertools.chain(first_collection, second_collection)
            )

        def __iter__(self) -> Iterator[T]:
            return iter(self._combined_elements)

        def __len__(self) -> int:
            return len(self._combined_elements)

    class Product(_FiniteCollection[Tuple[T, Y]], AbstractTopology.Product):
        def __init__(
                self,
                first_collection: Collection[T],
                second_collection: Collection[Y]
        ) -> None:
            super(FiniteTopology.Product, self).__init__(
                first_collection, second_collection
            )
            self._combined_elements = frozenset(
                itertools.product(first_collection, second_collection)
            )

        def __iter__(self) -> Iterator[Tuple[X, Y]]:
            return iter(self._combined_elements)

        def __len__(self) -> int:
            return len(self._combined_elements)

    class _ClosedSets(_FiniteCollection[T]):
        """
        Represents the collection of closed sets in the topology
        """
        def __init__(self, topology: FiniteTopologyInterface[T]) -> None:
            """

            :param topology: The topology for which the closed sets are to
                be generated
            """
            self._topology = topology

        def __iter__(self) -> Iterator[Collection[T]]:
            """

            :return: An iterator that iterates through the closed sets in
                the topology, by taking the complement of each open set
            """
            return (
                self._topology.complement(open_set)
                for open_set in self._topology.open_sets
            )

        def __len__(self) -> int:
            """

            :return: The number of closed sets in the topology. Since each open
                set has a corresponding closed set, then the number of closed
                sets is equal to the number of open sets.
            """
            return len(self._topology.open_sets)

        def __contains__(self, item: object) -> bool:
            """

            :param item: The item to test for membership. For a container, this
                is only true if the complement of the elements in the container
                corresponds to an open set.
            :return: ``True`` if the set is a closed set, otherwise ``False``.

            .. note::

                While the type annotation says that any object can be passed
                into this, the recommended type is ``Container[T]``, where
                ``T`` is the underlying type of the topology.

            """
            cast_item = cast(Container[T], item)
            return self._topology.complement(cast_item) \
                in self._topology.open_sets

        def __repr__(self) -> str:
            """

            :return: A human-friendly representation of the closed sets object
            """
            return '{0}(topology={1})'.format(
                self.__class__.__name__, self._topology
            )

    class _Complement(_FiniteCollection[T]):
        """
        Represents the complement of a given open set. A complement, as defined
        in definition 1.1.1 in Abraham and Marsden, is the set of elements in
        a topology that are not in a given set.
        """
        def __init__(
                self,
                topology: FiniteTopologyInterface[T],
                base_set: Container[T]
        ) -> None:
            """

            :param topology: The topological space in which the complement is
                being taken
            :param base_set: The set of elements for which the complement is
                to be taken.
            """
            self._topology = topology
            self._set = base_set

        def __iter__(self) -> Iterator[T]:
            """

            :return: A generator that loops over all elements in the topology
                and yields the elements that are not in the set given to this
                object during construction.
            """
            for element in self._topology.elements:
                if element not in self._set:
                    yield element

        def __len__(self) -> int:
            """

            :return: The number of elements in the complement
            """
            return len(frozenset(iter(self)))

        def __contains__(self, item: object) -> bool:
            """
            Membership test for the complement

            :param item: The item that is to be checked for membership. It is
                recommended that this item has type ``T``, where ``T`` is the
                type of element of the topology for which the complement was
                taken
            :return: ``True`` if the item is in the complement, otherwise
                ``False``.
            """
            c_item = cast(T, item)
            return \
                c_item in self._topology.elements and c_item not in self._set

        def __repr__(self) -> str:
            """

            :return: A human-friendly representation of the constructor
                arguments of this object
            """
            return "{0}(topology={1}, base_set={2})".format(
                self.__class__.__name__, self._topology, self._set
            )
