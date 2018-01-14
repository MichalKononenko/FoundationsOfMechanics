"""
Describes an interval between two points. An interval is a container that has
a lower and upper bound
"""
import abc
from typing import TypeVar, Container, Generic

T = TypeVar('T')


class Interval(Container[T], Generic[T], metaclass=abc.ABCMeta):
    """
    Base class for an interval.
    """


class BoundedInterval(Interval[T], Generic[T], metaclass=abc.ABCMeta):
    """
    Base class for an interval with a lower and upper bound
    """
    @property
    def lower_bound(self) -> T:
        """

        :return: The lower bound for this interval
        """
        raise NotImplementedError()

    @property
    def upper_bound(self) -> T:
        """

        :return: The upper bound for this interval
        """
        raise NotImplementedError()

