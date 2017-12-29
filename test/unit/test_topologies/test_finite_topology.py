"""
Contains unit tests for the finite topology
"""
import unittest
from hypothesis import given, assume
from ..generators import topologies
from src.interfaces import Topology


class TestFiniteTopology(unittest.TestCase):
    """
    Base class for unit testing finite topologies
    """


class TestGetOpenNeighborhoods(TestFiniteTopology):
    """
    Contains unit tests for the method that gets the first elements
    """
    @given(topologies())
    def test_get_open_neighborhood_of_point(self, topology: Topology) -> None:
        """

        :param topology: The topology for which open neighborhoods are to be
            obtained
        """
        assume(frozenset(topology.elements) != frozenset())
        first_point = next(iter(topology.elements))
        open_neighborhoods = topology.get_open_neighborhoods(first_point)
        self.assertIsNotNone(open_neighborhoods)
        self.assertGreater(len(open_neighborhoods), 0)

    @given(topologies())
    def test_get_open_neighborhood_of_set(self, topology: Topology) -> None:
        """

        :param topology: The topology for which open neighborhoods are to be
            obtained
        :return:
        """
        assume(frozenset(topology.elements) != frozenset())
        first_point = frozenset({next(iter(topology.elements))})
        open_neighborhoods = topology.get_open_neighborhoods(first_point)
        self.assertIsNotNone(open_neighborhoods)
        self.assertGreater(len(open_neighborhoods), 0)
