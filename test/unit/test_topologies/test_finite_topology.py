"""
Contains unit tests for the finite topology
"""
import unittest
from hypothesis import given, assume
from hypothesis.strategies import lists
from test.unit.generators import topologies, topological_subsets
from test.unit.generators import TopologicalSubset
from src.interfaces import Topology
from functools import reduce
from typing import List, TypeVar
import operator
from src.topologies import EmptyTopology

T = TypeVar('T')


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


class TestComplement(TestFiniteTopology):
    """
    Contains unit tests for the complement function
    """
    @given(topologies())
    def test_complement(self, topology: Topology[int]) -> None:
        """
        The complement of the complement of a set should be the same set

        :param topology: The topology on which the complement is to be tested
        """
        for open_set in topology.open_sets:
            self.assertEqual(
                open_set,
                topology.complement(topology.complement(open_set))
            )


class TestBoundary(TestFiniteTopology):
    """
    Contains unit tests for the boundary function
    """
    @given(topological_subsets())
    def test_boundary_is_closed(
            self,
            test_parameters: TopologicalSubset
    ) -> None:
        """
        Check that the boundary of a set is closed

        :param test_parameters: The topology and subset on which this test is to be
            run
        """
        self.assertIn(
            test_parameters.topology.boundary(test_parameters.subset),
            test_parameters.topology.closed_sets
        )

    @given(topological_subsets())
    def test_boundary_is_equal_to_complement(
            self,
            test_parameters: TopologicalSubset
    ) -> None:
        """

        :param test_parameters: The parameters for the test, containing a
            topology, and a subset of the elements of the topology. These
        :return:
        """
        self.assertEqual(
            test_parameters.topology.boundary(test_parameters.subset),
            test_parameters.topology.boundary(
                test_parameters.topology.complement(test_parameters.subset)
            )
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
