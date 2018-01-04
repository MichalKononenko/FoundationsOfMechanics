"""
Contains implementations for working with topologies. A topology, or
topological space, is a set of elements :math:`S` and a set of sets
:math:`\Sigma` called open sets such that

* The empty set :math:`\emptyset` and the set of all elements :math:`S` are
    open sets
* The intersection of any two open sets is an open set
* The union of any two open sets is open

"""
from .custom_topology import CustomTopology
from .random_topology import RandomTopology
from .relative_topology import RelativeTopology
from .empty_topology import EmptyTopology
from .finite_product_topology import FiniteProductTopology
