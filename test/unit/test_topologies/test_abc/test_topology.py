"""
Contains unit tests for the intersection and union operations
"""
import unittest
from typing import Set, Container, cast
from fom.topologies.abc import Topology as AbstractTopology
from hypothesis import given
from hypothesis.strategies import sets, integers


class ConcreteTopology(AbstractTopology[int]):
    """
    Base class for the topology
    """
    @property
    def elements(self) -> Container[int]:
        raise NotImplementedError()

    @property
    def open_sets(self) -> Container[Container[int]]:
        raise NotImplementedError()


class TestTopology(unittest.TestCase):
    """
    Base class for testing the abstract topology
    """
    def setUp(self) -> None:
        self.topology = ConcreteTopology()


class TestIntersection(TestTopology):
    """
    Contains unit tests for the intersection of two containers
    """
    @given(sets(integers()), sets(integers()))
    def test_container_intersection(
            self, left_set: Set[int], right_set: Set[int]
    ) -> None:
        """

        :param left_set:
        :param right_set:
        """
        intersected_elements = left_set.intersection(right_set)
        cast_left = cast(Container[int], left_set)
        cast_right = cast(Container[int], right_set)
        container = ConcreteTopology.Intersection(cast_left, cast_right)
        self.assertTrue(
            all(element in container for element in intersected_elements)
        )


class TestUnion(TestTopology):
    """
    Contains unit tests for determining the union of two containers
    """
    @given(sets(integers()), sets(integers()))
    def test_container_union(
            self, left_set: Set[int], right_set: Set[int]
    ) -> None:
        """

        :param left_set: The left side of the set to union
        :param right_set: The right side of the set to union
        """
        union_elements = left_set.union(right_set)
        cast_left = cast(Container[int], left_set)
        cast_right = cast(Container[int], right_set)
        container = ConcreteTopology.Union(cast_left, cast_right)
        self.assertTrue(
            all(element in container for element in union_elements)
        )
