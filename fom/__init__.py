"""
Library for working with symplectic geometries as defined in Abraham and
Marsden's Foundations of Mechanics. This works attempts to mirror the
definitions in the textbook as close as possible.

The :mod:`fom.interfaces` contains the API documentation, defined in the form
of Python abstract classes that have no implemented methods. When wiring
custom objects into this library, it is recommended that these interfaces are
implemented in order to provide robust code. They should have no implementation
conflicts.

Type consistency is checked by ``mypy``.

"""