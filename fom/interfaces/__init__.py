"""
Contains abstract interfaces for components in this library. These are abstract
classes that raise :class:`python.NotImplementedError` for each abstract method
that they define. These classes also have no internal business logic or state,
making them safe for multiple inheritance.

The purpose of these classes is to expose the type and contract for the
:mod:`fom` library to internal components and to other users. The contract
represents the method that each implementation of the interface is guaranteed
to implement.

"""
from .topologies import FiniteTopology
from .topologies import Topology
from .topologies import ProductTopology
from .topologies import FiniteProductTopology
from .basis import Basis
from .intervals import Interval, BoundedInterval
