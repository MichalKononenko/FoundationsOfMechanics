"""
Defines a topology where sets and open sets are given by the user on
construction
"""
from fom.interfaces import FiniteTopology as FiniteTopologyInterface
from fom.interfaces import Topology as TopologyInterface
from typing import TypeVar, Union, Collection, Generic, Iterator
from typing import Container, Iterable
from fom.exceptions import InvalidOpenSets

T = TypeVar('T')


class CustomTopology(FiniteTopologyInterface[T], Generic[T]):
    """
    Implements a finite topology where open sets and elements are given by the
    user
    """
    def __init__(
            self, elements: Collection[T], open_sets: Collection[Collection[T]]
    ) -> None:
        """

        :param elements: The set of elements in the topology
        :param open_sets: The open sets in the topology
        """
        self._elements = elements
        self._open_sets = open_sets

        self._assert_first_axiom(elements, open_sets)

    @property
    def elements(self) -> Collection[T]:
        """

        :return: The elements of the topology
        """
        return self._elements

    @property
    def open_sets(self) -> Collection[Collection[T]]:
        """

        :return: The open sets
        """
        return self._open_sets

    @property
    def closed_sets(self) -> Collection[Collection[T]]:
        """

        :return: The collection of closed sets in this topology
        """
        return self._ClosedSets(self)

    def get_open_neighborhoods(
            self, point_or_set: Union[T, Container[T]]
    ) -> Collection[Collection[T]]:
        """

        :param point_or_set: The point or set for which the open neighborhoods
            are to be obtained
        :return: The open neighborhoods
        """
        if self._is_point(point_or_set):
            neighborhoods = self._OpenNeighborhoodsForPoint(self, point_or_set)
        else:
            neighborhoods = self._OpenNeighborhoodsForSet(self, point_or_set)

        return neighborhoods

    def closure(self, subset: Container[T]) -> Collection[T]:
        """

        :param subset: The set for which the closure is to be obtained
        :return: The closure
        """
        closed_sets_containing_subset = filter(
            lambda set_: self._open_set_contains_container(set_, subset),
            self.closed_sets
        )

        return self._Intersection(self, closed_sets_containing_subset)

    def interior(self, subset: Container[T]) -> Collection[T]:
        """

        :param subset:
        :return:
        """
        open_sets_containing_subset = filter(
            lambda set_: self._open_set_contains_container(set_, subset),
            self.open_sets
        )

        return self._Union(self, open_sets_containing_subset)

    def boundary(self, subset: Container[T]) -> Collection[T]:
        """

        :param subset: The subset for which the boundary is to be calculated
        :return:
        """
        return self._Intersection(
            self, [self.closure(subset), self.complement(self.closure(subset))]
        )

    def complement(self, subset: Container[T]) -> Collection[T]:
        """

        :param subset:
        :return:
        """
        return self._Complement(self, subset)

    @staticmethod
    def _is_point(point_or_set: Union[T, Container[T]]):
        return not isinstance(point_or_set, Container)

    def _open_set_contains_container(
            self,
            open_set: Collection[T],
            container: Container[T]
    ) -> bool:
        closed_set_has_container = any((
            element in container for element
            in self.complement(open_set)))
        all_elements_in_container = all((
            element in container for element in open_set
        ))
        return all_elements_in_container and not closed_set_has_container

    @staticmethod
    def _assert_first_axiom(
            elements: Collection[T],  open_sets: Collection[Collection[T]]
    ) -> None:
        contains_empty_set = False
        contains_set_of_elements = False
        for open_set in open_sets:
            if all(element not in open_set for element in elements):
                contains_empty_set = True
            if all(element in open_set for element in elements):
                contains_set_of_elements = True

        if not contains_empty_set:
            raise InvalidOpenSets(
                'The set of open sets does not contain the empty set'
            )

        if not contains_set_of_elements:
            raise InvalidOpenSets(
                'The set of open sets not contain the set of elements'
            )


    def __mul__(self, other: TopologyInterface[T]) -> TopologyInterface[T]:
        return self

    def __eq__(self, other: object) -> bool:
        if not (hasattr(other, 'elements') and hasattr(other, 'open_sets')):
            is_equal = False
        else:
            is_equal = (other.elements == self.elements) and (other.open_sets == self.open_sets)

        return is_equal

    class _ClosedSets(Collection[Collection[T]], Generic[T]):
        """
        Base class for the collection of closed sets
        """
        def __init__(self, topology: FiniteTopologyInterface[T]) -> None:
            """

            :param topology: The topology for which the closed sets are to be
                obtained
            """
            self._topology = topology

        def __len__(self) -> int:
            """

            :return: The number of closed sets in the collection. This is equal
                to the number of open sets in the parent topology since every
                closed set has a complementary open set
            """
            return len(self._topology.open_sets)

        def __iter__(self) -> Iterator[Collection[T]]:
            """

            :return: An iterator iterating through the closed sets
            """
            return (
                self._topology.complement(open_set)
                for open_set in self._topology.open_sets
            )

        def __contains__(self, item: Collection[T]) -> bool:
            """

            :param item: The item to check for membership in the topology
            :return: ``True`` if the set is a closed set in the topology,
                otherwise ``False``
            """
            return self._topology.complement(item) in self._topology.open_sets

        def __repr__(self) -> str:
            return '%s(topology=%s)' % (
                self.__class__.__name__, self._topology
            )

    class _OpenNeighborhoodsForPoint(Collection[Collection[T]], Generic[T]):
        """
        The collection of open neighborhoods
        """
        def __init__(
                self,
                topology: FiniteTopologyInterface[T],
                point: T
        ) -> None:
            self._topology = topology
            self._point = point

        def __iter__(self) -> Iterator[Collection[T]]:
            return (
                open_set for open_set in self._topology.open_sets
                if self._point in open_set
            )

        def __len__(self) -> int:
            """

            :return: The number of open neighborhoods
            """
            return len(frozenset(self))

        def __contains__(self, item: Collection[T]) -> bool:
            """

            :param item: The open set to see if it is a neighborhood
            :return:
            """
            return item in frozenset(self)

    class _OpenNeighborhoodsForSet(Collection[Collection[T]], Generic[T]):
        def __init__(
                self,
                topology: FiniteTopologyInterface[T],
                container: Container[T]
        ) -> None:
            self._topology = topology
            self._container = container

        def __iter__(self) -> Iterator[Collection[T]]:
            """

            :return: The open neighborhoods
            """
            return (
                open_set for open_set in self._topology.open_sets if
                self._open_set_contains_container(open_set, self._container)
            )

        def __len__(self) -> int:
            return len(frozenset(self))

        def __contains__(self, item: Collection[T]) -> bool:
            return item in frozenset(self)

        def _open_set_contains_container(
                self,
                open_set: Collection[T],
                container: Container[T]
        ) -> bool:
            closed_set_has_container = any(
                element in container for element
                in self._topology.complement(open_set))
            all_elements_in_container = all(
                element in container for element in open_set
            )

            return all_elements_in_container and not closed_set_has_container

    class _Intersection(Collection[T], Generic[T]):
        """
        Base class for intersection of a set of sets
        """
        def __init__(
                self,
                topology: FiniteTopologyInterface[T],
                containers_to_intersect: Iterable[Container[T]]
        ) -> None:
            self._topology = topology
            self._containers = containers_to_intersect

        def __iter__(self) -> Iterator[T]:
            return (
                element for element in self._topology.elements
                if all(element in container for container in self._containers)
            )

        def __len__(self) -> int:
            return len(frozenset(self))

        def __contains__(self, item: T) -> bool:
            return item in frozenset(self)

    class _Union(Collection[T], Generic[T]):
        """
        Base class for the union of a set of sets
        """
        def __init__(
                self,
                topology: FiniteTopologyInterface[T],
                containers_to_intersect: Iterable[Container[T]]
        ) -> None:
            self._topology = topology
            self._containers = containers_to_intersect

        def __iter__(self) -> Iterator[T]:
            return (
                element for element in self._topology.elements
                if any(element in container for container in self._containers)
            )

        def __len__(self) -> int:
            return len(frozenset(self))

        def __contains__(self, item: T) -> bool:
            return item in frozenset(self)

    class _Complement(Collection[T], Generic[T]):
        """

        """
        def __init__(
                self,
                topology: FiniteTopologyInterface[T],
                subset: Container[T]
        ) -> None:
            self._topology = topology
            self._subset = subset

        def __iter__(self) -> Iterator[T]:
            return (
                element for element in self._topology.elements
                if element not in self._subset
            )

        def __len__(self) -> int:
            return len(frozenset(self))

        def __contains__(self, item: T) -> bool:
            return item in frozenset(self)
