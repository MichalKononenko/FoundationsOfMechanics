"""
Contains unit tests for the finite topology
"""
import unittest
from hypothesis import given, assume
from hypothesis.strategies import lists
from test.unit.generators import topologies
from src.interfaces import Topology
from functools import reduce
from typing import List
import operator
from src.topologies import EmptyTopology


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
    def test_closed_sets(self, topology: Topology) -> None:
        """
        Test that the complement of the closed sets of the topology are open
        sets

        :param topology: The topology for which closed sets are to be tested
        """
        for closed_set in topology.closed_sets:
            self.assertIn(
                topology.elements.difference(closed_set), topology.open_sets
            )


class TestProduct(TestFiniteTopology):
    """
    Tests that multiplying two finite topologies together produces a product
    topology
    """
    @given(lists(topologies()))
    def test_multiplication(self, topology_list: List[Topology]):
        """
        Tests that multiplying random topologies yields a topology with
        elements being the union of all elements in each topology.

        :param topology_list: A list of randomly-generated topologies to
            multiply
        """
        product = reduce(operator.mul, topology_list, EmptyTopology())
        self.assertIsInstance(product, Topology)
        elements = reduce(
            lambda x, y: x.union(y),
            map(lambda x: x.elements, topology_list),
            set()
        )
        self.assertEqual(elements, product.elements)
