"""
Contains tests for the custom topology
"""
import unittest
from typing import Set, FrozenSet, Union, TypeVar
from src.topologies.custom_topology import CustomTopology
from src.interfaces import Topology
from hypothesis import given
from test.unit.generators import topologies

T = TypeVar('T')
ANY_SET = Union[Set[T], FrozenSet[T], set]


class TestCustomTopology(unittest.TestCase):
    """
    Contains tests for the custom topology
    """
    def setUp(self) -> None:
        """
        Provide some elements
        """

    @property
    def x1(self) -> str:
        return 'element x1'

    @property
    def x2(self) -> str:
        return 'element x2'

    @property
    def elements(self) -> Set[str]:
        return {self.x1, self.x2}

    @property
    def open_sets(self) -> ANY_SET:
        return {frozenset({}), frozenset({self.x1}), frozenset({self.x1, self.x2})}

    @property
    def invalid_open_sets(self) -> ANY_SET[ANY_SET]:
        return {frozenset({self.x1})}


class TestCustomTopologyConstructor(TestCustomTopology):
    """
    Tests that the constructor allows a valid topology
    """
    def test_valid_topology(self):
        topol = CustomTopology(self.elements, self.open_sets)
        self.assertEqual(self.elements, topol.elements)
        self.assertEqual(self.open_sets, topol.open_sets)

    def test_invalid_topology(self):
        with self.assertRaises(ValueError):
            CustomTopology(self.elements, self.invalid_open_sets)


class TestCustomTopologyGenerator(TestCustomTopology):
    """
    Tests that the topology generator makes random topologies
    """
    @given(topologies())
    def test_generator(self, topol: Topology) -> None:
        self.assertIsInstance(topol, Topology)
