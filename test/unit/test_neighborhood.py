from .generators import topologies
import unittest
from hypothesis import given, assume
from src.interfaces import Topology
from src.neighborhood import is_neighborhood, is_open_neighborhood
from src.neighborhood import is_set_open_neighborhood


class TestIsNeighborhood(unittest.TestCase):
    """
    Contains test for the is_neighborhood function
    """
    @given(topologies())
    def test_is_neighborhood_true(self, topology: Topology) -> None:
        """
        The first element of the topology should always be in the set of all
        possible elements, and the set of all elements in the topology is
        always an open set (and a closed set for that matter). The point must
        be in the set of all elements, which is always an open neighborhood

        :param topology: The topology to check. Must be a non-empty topology
        """
        assume(topology.elements != frozenset())
        first_element = next(iter(topology.elements))
        self.assertTrue(is_neighborhood(first_element, topology.elements))


class TestIsOpenNeighborhood(unittest.TestCase):
    """
    Contains tests for the open neighborhood function
    """
    @given(topologies())
    def test_is_open_neighborhood(self, topology: Topology) -> None:
        """
        The first element of the topology should always be in the set of all
        possible elements, which is an open set of the topology. Therefore,
        this point is an open neighborhood

        :param topology: The topology to check. Must be a non-empty topology
        """
        assume(topology.elements != frozenset())
        first_element = next(iter(topology.elements))
        self.assertTrue(
            is_open_neighborhood(first_element, topology.elements, topology)
        )


class TestSetIsOpenNeighborhood(unittest.TestCase):
    """
    Contains tests for the set open neighborhood
    """
    @given(topologies())
    def test_is_set_open(self, topology: Topology) -> None:
        """

        :param topology: The topology to check
        """
        assume(topology.elements != frozenset())
        first_set = next(iter(topology.open_sets))
        self.assertTrue(
            is_set_open_neighborhood(first_set, first_set, topology)
        )
