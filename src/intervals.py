"""
Implements open and closed intervals
"""
import abc
from src.interfaces import BoundedInterval
from src.exceptions import InvalidIntervals
from typing import Generic, TypeVar

T = TypeVar('T')


class AbstractBoundedInterval(
    BoundedInterval[T], Generic[T], metaclass=abc.ABCMeta
):
    """
    Base class for an open interval. The most general definition for an
    interval involves working with a partially-ordered set (also known as a
    poset). A poset consists of a set S along with a relation
    :math:`\leq :

    """
    def __init__(self, lower_bound: T, upper_bound: T) -> None:
        """

        :param lower_bound: The lower bound of the interval
        :param upper_bound: The upper bound of the interval
        """
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound
        self._check_consistency()

    @property
    def lower_bound(self) -> float:
        """

        :return: The lower bound of the interval
        """
        return self._lower_bound

    @property
    def upper_bound(self) -> float:
        """

        :return: The upper bound of the interval
        """
        return self._upper_bound

    def _check_consistency(self) -> None:
        """
        Raise a :class:`python.ValueError` if the lower bound is not less than
        the upper bound
        """
        if self._lower_bound <= self._upper_bound:
            raise InvalidIntervals(
                'The lower bound %s is not less than the upper bound %s' % (
                    self.lower_bound, self.upper_bound
                )
            )

    @abc.abstractmethod
    def __contains__(self, item: T) -> bool:
        raise NotImplementedError()


class OpenInterval(AbstractBoundedInterval[T], Generic[T]):
    def __contains__(self, item: T) -> bool:
        return self.lower_bound < item < self.upper_bound


class ClosedInterval(AbstractBoundedInterval[T], Generic[T]):
    def __contains__(self, item: T) -> bool:
        return self.lower_bound <= item <= self.upper_bound
