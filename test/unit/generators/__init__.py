"""
Defines generators for test fixtures. A generator is a function that describes
how to take "primitive" generators provided by :mod:`hypothesis` and compose
them into more complicated generators. These more complicated generators create
instances of whatever type is required for testing. Primitive generators rely
on the random-number generator to create random test cases. Thus, each unit
test can be run multiple times with randomly-generated data.
"""
from .topologies import topologies
from .topological_subsets import topological_subsets, TopologicalSubset
