"""
Describes exceptions
"""


class InvalidOpenSets(ValueError):
    """
    Thrown if the combination of elements and open sets provided into a
    topology do not meet the axioms of a topological space
    """


class InvalidSubset(ValueError):
    """
    Thrown if a relative topology is defined on a set that is not a subset
    of the elements of the base topology
    """


class InvalidIntervals(ValueError):
    """
    Thrown if an interval is defined that does not have a real value
    """