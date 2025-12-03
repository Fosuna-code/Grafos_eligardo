import pytest
from graph_traversal import GraphTraversal
def test_bfs_simple_graph():
    graph = GraphTraversal()
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    graph.add_edge(2, 4)
    
    result = graph.bfs(1)
    
    assert result == [1, 2, 3, 4]

def test_bfs_shortest_path():
    graph = GraphTraversal()
    edges = [(1,2), (1,3), (2,4), (3,4), (4,5)]
    for u, v in edges:
        graph.add_edge(u, v)
    
    path = graph.bfs_shortest_path(1, 5)
    
    assert path is not None
    assert len(path) == 4  # 3 aristas
    assert path[0] == 1
    assert path[-1] == 5

def test_dfs_detects_cycle():
    graph = GraphTraversal(directed=True)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 1)  # Ciclo
    
    assert graph.has_cycle_directed() == True

def test_topological_sort_dag():
    graph = GraphTraversal(directed=True)
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    graph.add_edge(2, 4)
    graph.add_edge(3, 4)
    
    order = graph.topological_sort()
    
    assert order is not None
    assert order[0] == 1
    assert order[-1] == 4

def test_connected_components():
    graph = GraphTraversal()
    graph.add_edge(1, 2)
    graph.add_edge(3, 4)
    graph.add_edge(5, 6)
    
    components = graph.find_connected_components()
    
    assert len(components) == 3

# ========================================
# TESTS PARA CASOS LÍMITE (EDGE CASES)
# ========================================

def test_bfs_non_existent_node():
    graph = GraphTraversal()
    graph.add_edge(1, 2)
    
    with pytest.raises(ValueError, match="El nodo 99 no existe"):
        graph.bfs(99)

def test_dfs_non_existent_node():
    graph = GraphTraversal()
    graph.add_edge(1, 2)
    
    with pytest.raises(ValueError, match="El nodo 99 no existe"):
        graph.dfs_recursive(99)
    
    with pytest.raises(ValueError, match="El nodo 99 no existe"):
        graph.dfs_iterative(99)

def test_bfs_empty_graph():
    graph = GraphTraversal()
    
    with pytest.raises(ValueError):
        graph.bfs(1)

def test_bfs_single_node():
    graph = GraphTraversal()
    graph.add_edge(1, 1)  # Nodo con self-loop
    
    result = graph.bfs(1)
    
    assert len(result) == 1
    assert result[0] == 1

def test_dfs_isolated_node():
    graph = GraphTraversal()
    graph.add_edge(1, 1)  # Nodo aislado
    
    result = graph.dfs_recursive(1)
    
    assert len(result) == 1

def test_bfs_disconnected_graph():
    graph = GraphTraversal()
    graph.add_edge(1, 2)
    graph.add_edge(3, 4)
    
    result = graph.bfs(1)
    
    assert len(result) == 2
    assert 1 in result
    assert 2 in result
    assert 3 not in result
    assert 4 not in result

if __name__ == "__main__":
    pytest.main([__file__, "-v"])