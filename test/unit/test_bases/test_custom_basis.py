"""
A basis containing all the open sets of a topology is a basis for the topology.
"""
import unittest
from hypothesis import given
from test.unit.generators import topologies
from src.interfaces import Topology
from src.bases import CustomBasis


class TestCustomBasis(unittest.TestCase):
    """
    Contains unit tests for the basis
    """
    @given(topologies())
    def test_topology(self, topology: Topology) -> None:
        """

        :param topology: The topology to test
        :return:
        """
        basis = CustomBasis(topology.open_sets, topology)
        self.assertEqual(basis.topology, topology)
