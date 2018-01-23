"""
Contains unit tests for relative topologies
"""
import unittest
from fom.interfaces import Topology
from fom.topologies import RelativeTopology, CustomTopology
from hypothesis import given, assume
from test.unit.generators import topologies


class TestRelativeTopology(unittest.TestCase):
    """
    Base class for testing relative topologies
    """
    def setUp(self):
        self.elements = frozenset({'item 1', 'item 2'})
        self.open_sets = frozenset({frozenset(), self.elements})
        self.custom_topology = CustomTopology(self.elements, self.open_sets)


class TestConstructor(TestRelativeTopology):
    """
    Tests the constructor
    """
    @given(topologies())
    def test_valid_subset(self, topology: Topology):
        """
        Tests that an isolated topology containing just the first element of
        a larger topology is a valid relative topology

        :param topology: The topology for which a relative topology is to be
            constructed
        :return:
        """
        assume(len(list(topology.elements)) >= 2)
        first_element = next(iter(topology.elements))
        subset = frozenset({first_element})

        relative_topology = RelativeTopology(subset, topology)
        self.assertIn(first_element, relative_topology.elements)

    def test_invalid_subset(self) -> None:
        """
        Tests that attempting to make an invalid relative topology throws an
        error
        """
        with self.assertRaises(ValueError):
            RelativeTopology(frozenset({'item 3'}), self.custom_topology)
