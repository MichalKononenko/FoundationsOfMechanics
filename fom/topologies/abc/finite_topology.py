"""
Base class for topologies with a finite number of elements
"""
import abc
from typing import Set, TypeVar, Union, Generic, Collection, Container
from typing import Iterator, Tuple, cast
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


class FiniteTopology(
    FiniteTopologyInterface[T], Generic[T], metaclass=abc.ABCMeta
):
    """
    Base class for topologies with a finite number of elements. This means that
    the open sets of the topology can be iterated through
    """
    @property
    def closed_sets(self) -> Collection[Collection[T]]:
        """

        :return: The closed sets in the topology
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

    def complement(self, subset: Container[T]) -> Set[T]:
        """

        :param subset: The subset for which the complement is to be retrieved
        :return: The complement
        """
        return frozenset(
            (element for element in self.elements if element not in subset)
        )

    def closure(self, subset: Set[T]) -> Set[T]:
        """

        :param subset: The subset for which the closure is to be calculated
        :return: The closure
        """
        self._assert_subset(subset)
        s = frozenset(subset)
        return reduce(
            operator.and_,
            filter(s.issubset, self.closed_sets),
            set()
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

    def boundary(self, subset: Set[T]) -> Set[T]:
        """

        :param subset: The subset for which the boundary is to be calculated
        :return: The boundary
        """
        self._assert_subset(subset)
        return self.closure(subset) and self.closure(self.complement(subset))

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

    class Intersection(Collection[T], AbstractTopology.Intersection):
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

    class Union(Collection[T], AbstractTopology.Union):
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

    class Product(Collection[Tuple[T, Y]], AbstractTopology.Product):
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

    class _ClosedSets(Collection[T]):
        """
        Returns the closed sets
        """
        def __init__(self, topology: FiniteTopologyInterface[T]):
            self._topology = topology

        def __iter__(self) -> Iterator[Collection[T]]:
            return (
                self._topology.complement(open_set)
                for open_set in self._topology.open_sets
            )

        def __len__(self) -> int:
            return len(self._topology.open_sets)

        def __contains__(self, item: object) -> bool:
            cast_item = cast(Collection[T], item)
            return self._topology.complement(cast_item) \
                   in self._topology.open_sets
