from src.interfaces import Topology
from src.intervals import OpenInterval
from src.intervals import ClosedInterval
from typing import Container, Union, Collection


class Interval(Container[float]):
    """
    Describes an interval between two points on the real number line
    """


class RealNumbers(Topology[float]):
    """
    Describes the standard topology of the real numbers. The elements of this
    topology are the real numbers, and the open sets of the topology are the
    sets that are unions of open intervals of real numbers. This is an example
    of a topological space.

    """
    @property
    def elements(self) -> Container[float]:
        return self._Elements()

    @property
    def open_sets(self) -> Container[Container[float]]:
        return self._OpenSets()

    @property
    def closed_sets(self) -> Container[Container[float]]:
        return self._ClosedSets()

    @property
    def get_open_neighborhoods(
            self, point_or_set: Union[float, Container[float]]
    ) -> Container[Container[float]]:
        if isinstance(point_or_set, float):
            set_to_check = frozenset({point_or_set})
        else:
            set_to_check = point_or_set

        return self._OpenNeighborhoods(set_to_check)

    class _Elements(Container[float]):
        """
        Base class for the container of the elements of this topology
        """
        def __contains__(self, item: float) -> bool:
            """

            :param item: The item to check
            :return: True if the item is a float. This means that it is a real
                number, and so it belongs to the elements
            """
            return isinstance(item, float)

    class _OpenSets(Container[OpenInterval[float]]):
        """
        Describes the open sets of the topology
        """
        def __contains__(self, item: OpenInterval[float]) -> bool:
            return isinstance(item, OpenInterval[float])

    class _ClosedSets(Container[ClosedInterval[float]]):
        """
        Describes the closed sets of the topology
        """
        def __contains__(self, item: ClosedInterval[float]) -> bool:
            return isinstance(item, ClosedInterval[float])

    class _OpenNeighborhoods(Container[OpenInterval[float]]):
        """
        Defines the open neighborhoods of a point
        """
        def __init__(self, points: Collection[float]) -> None:
            self._points = points

        def __contains__(self, item: OpenInterval[float]) -> bool:
            return all(point in item for point in self._points)
