import unittest
import networkx as nx


def is_eulerian(G):
    """Returns True if and only if `G` is Eulerian.

    A graph is *Eulerian* if it has an Eulerian circuit. An *Eulerian
    circuit* is a closed walk that includes each edge of a graph exactly
    once.

    Parameters
    ----------
    G : NetworkX graph
       A graph, either directed or undirected.

    Examples
    --------
    >>> nx.is_eulerian(nx.DiGraph({0: [3], 1: [2], 2: [3], 3: [0, 1]}))
    True
    >>> nx.is_eulerian(nx.complete_graph(5))
    True
    >>> nx.is_eulerian(nx.petersen_graph())
    False

    Notes
    -----
    If the graph is not connected (or not strongly connected, for
    directed graphs), this function returns False.

    """
    if G.is_directed():
        # Every node must have equal in degree and out degree and the
        # graph must be strongly connected
        return (all(G.in_degree(n) == G.out_degree(n) for n in G) and
                nx.is_strongly_connected(G))
    # An undirected Eulerian graph has no vertices of odd degree and
    # must be connected.
    return all(d % 2 == 0 for v, d in G.degree()) and nx.is_connected(G)

def has_eulerian_path(G):
    """Return True iff `G` has an Eulerian path.

    An Eulerian path is a path in a graph which uses each edge of a graph
    exactly once.

    A directed graph has an Eulerian path iff:
        - at most one vertex has out_degree - in_degree = 1,
        - at most one vertex has in_degree - out_degree = 1,
        - every other vertex has equal in_degree and out_degree,
        - and all of its vertices with nonzero degree belong to a
        - single connected component of the underlying undirected graph.

    An undirected graph has an Eulerian path iff:
        - exactly zero or two vertices have odd degree,
        - and all of its vertices with nonzero degree belong to a
        - single connected component.

    Parameters
    ----------
    G : NetworkX Graph
        The graph to find an euler path in.

    Returns
    -------
    Bool : True if G has an eulerian path.

    See Also
    --------
    is_eulerian
    eulerian_path
    """
    if G.is_directed():
        ins = G.in_degree
        outs = G.out_degree
        semibalanced_ins = sum(ins(v) - outs(v) == 1 for v in G)
        semibalanced_outs = sum(outs(v) - ins(v) == 1 for v in G)
        return (semibalanced_ins <= 1 and
                semibalanced_outs <= 1 and
                sum(G.in_degree(v) != G.out_degree(v) for v in G) <= 2 and
                nx.is_weakly_connected(G))
    else:
        return (sum(d % 2 == 1 for v, d in G.degree()) in (0, 2)
                and nx.is_connected(G))

class TestEulerMethods(unittest.TestCase):

  def test_seven_bridges_of_konigsberg(self):
    K=nx.MultiGraph(name="Königsberg")
    K.add_edges_from([("A","B","Honey Bridge"),
                       ("A","B","Blacksmith's Bridge"),
                       ("A","C","Green Bridge"),
                       ("A","C","Connecting Bridge"),
                       ("A","D","Merchant's Bridge"),
                       ("C","D","High Bridge"),
                       ("B","D","Wooden Bridge")])
    self.assertFalse(K.is_directed())
    self.assertFalse(has_eulerian_path(K))

  def test_five_bridges_of_kaliningrad(self):
    K=nx.MultiGraph(name="Königsberg")
    K.add_edges_from([("A","B","Honey Bridge"),
                       ("A","C","Green Bridge"),
                       ("A","D","Merchant's Bridge"),
                       ("C","D","High Bridge"),
                       ("B","D","Wooden Bridge")])
    self.assertFalse(K.is_directed())
    self.assertTrue(has_eulerian_path(K))

if __name__ == '__main__':
    unittest.main()