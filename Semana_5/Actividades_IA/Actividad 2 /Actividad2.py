"""
Módulo de algoritmos de exploración y búsqueda en grafos.
Incluye implementaciones de BFS, DFS y aplicaciones avanzadas.

Autor: Curso Estructuras de Datos Avanzadas
Fecha: 2025
"""

from collections import deque, defaultdict
from enum import Enum
from typing import List, Dict, Set, Optional, Tuple

class NodeState(Enum):
    """Estados de nodo para detección de ciclos en grafos dirigidos."""
    NOT_VISITED = 0
    IN_PROGRESS = 1
    COMPLETED = 2

# ========================================
# CLASE GRAPH TRAVERSAL
# ========================================

class GraphTraversal:
    """
    Clase que implementa algoritmos de exploración y búsqueda en grafos.
    Soporta grafos dirigidos y no dirigidos.
    """
    
    def __init__(self, directed: bool = False):
        """
        Inicializa el grafo.
        
        Args:
            directed: True si el grafo es dirigido, False en caso contrario.
        """
        self.adjacency_list: Dict[int, List[int]] = defaultdict(list)
        self.directed = directed
    
    def add_edge(self, u: int, v: int) -> None:
        """
        Agrega una arista al grafo.
        
        ### MEJORA (Robustez): Evita aristas duplicadas. ###
        
        Args:
            u: Nodo origen
            v: Nodo destino
        """
        
        # Evitar duplicados (u -> v)
        if v not in self.adjacency_list[u]:
            self.adjacency_list[u].append(v)
        
        if not self.directed:
            # Evitar duplicados (v -> u)
            if u not in self.adjacency_list[v]:
                self.adjacency_list[v].append(u)
        else:
            ### MEJORA (Claridad): Comentario explicando el 'truco'. ###
            # Asegurar que el nodo 'v' (destino) exista como 
            # llave en el grafo, incluso si no tiene vecinos (es "sink").
            # Esto es clave para has_cycle_directed() y topological_sort().
            _ = self.adjacency_list[v]
            
    # ========================================
    # BÚSQUEDA EN AMPLITUD (BFS)
    # ========================================
    
    def bfs(self, start: int) -> List[int]:
        """
        Realiza BFS desde un nodo inicial.
        """
        if start not in self.adjacency_list:
            if any(start in neighbors for neighbors in self.adjacency_list.values()):
                return [start]
            raise ValueError(f"El nodo {start} no existe en el grafo")
        
        visited: Set[int] = set()
        result: List[int] = []
        queue = deque([start])
        
        visited.add(start)
        
        while queue:
            current = queue.popleft()
            result.append(current)
            
            for neighbor in self.adjacency_list[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return result
    
    def bfs_distances(self, start: int) -> Dict[int, int]:
        """
        Calcula distancias desde el nodo inicial usando BFS.
        
        ### MEJORA (Eficiencia): Simplificado. ###
        Solo devuelve distancias de nodos alcanzables.
        El 'set' de visitados es redundante, usamos el dict 'distances'.
        """
        if start not in self.adjacency_list:
            if any(start in neighbors for neighbors in self.adjacency_list.values()):
                 return {start: 0}
            raise ValueError(f"El nodo {start} no existe en el grafo")

        distances: Dict[int, int] = {start: 0}
        queue = deque([start])
        
        while queue:
            current = queue.popleft()
            
            for neighbor in self.adjacency_list[current]:
                # Si el vecino no está en 'distances', no ha sido visitado.
                if neighbor not in distances:
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)
        
        # Ya no es necesario el segundo bucle para 'inf'
        return distances
    
    def bfs_levels(self, start: int) -> Dict[int, List[int]]:
        """
        Agrupa nodos por nivel de distancia desde el inicio.
        """
        if start not in self.adjacency_list:
            if any(start in neighbors for neighbors in self.adjacency_list.values()):
                return {0: [start]}
            raise ValueError(f"El nodo {start} no existe en el grafo")

        levels: Dict[int, List[int]] = defaultdict(list)
        visited: Set[int] = {start}
        queue = deque([(start, 0)])  # (nodo, nivel)
        
        while queue:
            current, level = queue.popleft()
            levels[level].append(current)
            
            for neighbor in self.adjacency_list[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, level + 1))
        
        return dict(levels)
    
    # ========================================
    # BÚSQUEDA EN PROFUNDIDAD (DFS)
    # ========================================
    
    def dfs_recursive(self, start: int) -> List[int]:
        """
        DFS recursivo desde un nodo inicial.
        """
        if start not in self.adjacency_list:
            if any(start in neighbors for neighbors in self.adjacency_list.values()):
                return [start]
            raise ValueError(f"El nodo {start} no existe en el grafo")
        
        visited: Set[int] = set()
        result: List[int] = []
        
        def dfs_helper(node: int) -> None:
            visited.add(node)
            result.append(node)
            
            for neighbor in self.adjacency_list[node]:
                if neighbor not in visited:
                    dfs_helper(neighbor)
        
        dfs_helper(start)
        return result
    
    def dfs_iterative(self, start: int) -> List[int]:
        """
        DFS iterativo usando pila explícita.
        
        ### MEJORA (Eficiencia): Optimizado. ###
        Marca nodos como visitados AL AÑADIRLOS a la pila,
        no al sacarlos. Esto evita que un nodo entre a la
        pila múltiples veces.
        """
        if start not in self.adjacency_list:
            if any(start in neighbors for neighbors in self.adjacency_list.values()):
                return [start]
            raise ValueError(f"El nodo {start} no existe en el grafo")
        
        visited: Set[int] = set()
        result: List[int] = []
        stack = [start]
        
        # Marcar como visitado EN CUANTO se añade a la pila
        visited.add(start) 
        
        while stack:
            current = stack.pop()
            
            # El nodo se procesa al salir
            result.append(current)
            
            # Iteramos en reversa para que el orden de visita
            # sea idéntico al DFS recursivo (opcional pero consistente).
            neighbors = list(self.adjacency_list[current])
            neighbors.reverse()
            
            for neighbor in neighbors:
                if neighbor not in visited:
                    # Marcar como visitado ANTES de añadirlo
                    visited.add(neighbor)
                    stack.append(neighbor)
            
        return result
    
    # ========================================
    # APLICACIONES AVANZADAS
    # ========================================
    
    def has_cycle_directed(self) -> bool:
        """
        Detecta si existe un ciclo en un grafo DIRIGIDO.
        """
        if not self.directed:
            raise ValueError("Este método requiere un grafo dirigido")
        
        state: Dict[int, NodeState] = {
            node: NodeState.NOT_VISITED 
            for node in self.adjacency_list.keys()
        }
        
        def dfs_cycle(node: int) -> bool:
            state[node] = NodeState.IN_PROGRESS
            
            for neighbor in self.adjacency_list[node]:
                neighbor_state = state.get(neighbor, NodeState.NOT_VISITED)
                
                if neighbor_state == NodeState.IN_PROGRESS:
                    return True  # ¡Ciclo detectado!
                
                if neighbor_state == NodeState.NOT_VISITED:
                    if dfs_cycle(neighbor):
                        return True
            
            state[node] = NodeState.COMPLETED
            return False
        
        for node in list(state.keys()):
            if state[node] == NodeState.NOT_VISITED:
                if dfs_cycle(node):
                    return True
        
        return False
    
    def topological_sort(self) -> Optional[List[int]]:
        """
        Realiza ordenamiento topológico en un DAG.
        """
        if not self.directed:
            raise ValueError("Ordenamiento topológico requiere grafo dirigido")
        
        all_nodes = set(self.adjacency_list.keys())
        
        if self.has_cycle_directed():
            return None
        
        visited: Set[int] = set()
        stack: List[int] = []
        
        def dfs_topo(node: int) -> None:
            visited.add(node)
            
            for neighbor in self.adjacency_list[node]:
                if neighbor not in visited:
                    dfs_topo(neighbor)
            
            stack.append(node)
        
        for node in list(all_nodes):
            if node not in visited:
                dfs_topo(node)
        
        stack.reverse()
        return stack
    
    def find_connected_components(self) -> List[List[int]]:
        """
        Encuentra todas las componentes conectadas en un grafo no dirigido.
        """
        if self.directed:
            raise ValueError("Este método requiere un grafo no dirigido")
        
        visited: Set[int] = set()
        components: List[List[int]] = []
        all_nodes = set(self.adjacency_list.keys())
        
        def dfs_component(node: int, component: List[int]) -> None:
            visited.add(node)
            component.append(node)
            
            for neighbor in self.adjacency_list[node]:
                if neighbor not in visited:
                    dfs_component(neighbor, component)
        
        for node in list(all_nodes):
            if node not in visited:
                component: List[int] = []
                dfs_component(node, component)
                components.append(component)
        
        return components
    
    def has_cycle_undirected(self) -> bool:
        """
        Detecta si existe un ciclo en un grafo NO DIRIGIDO.
        """
        if self.directed:
            raise ValueError("Este método requiere un grafo no dirigido")
        
        visited: Set[int] = set()
        all_nodes = set(self.adjacency_list.keys())
        
        def dfs_cycle(node: int, parent: Optional[int]) -> bool:
            visited.add(node)
            
            for neighbor in self.adjacency_list[node]:
                if neighbor not in visited:
                    if dfs_cycle(neighbor, node):
                        return True
                elif neighbor != parent:
                    return True
            
            return False
        
        for node in list(all_nodes):
            if node not in visited:
                if dfs_cycle(node, None):
                    return True
        
        return False

# ========================================
# CLASE PATHFINDER (CORREGIDA)
# ========================================

class PathFinder:
    """
    Utiliza un grafo (GraphTraversal) para encontrar caminos.
    """
    def __init__(self, graph: GraphTraversal):
        """
        Inicializa el buscador de caminos con un grafo existente.
        """
        self.graph = graph

    def find_shortest_path(self, start: int, end: int) -> Optional[List[int]]:
        """
        Encuentra el camino más corto (en número de saltos) usando BFS.
        """
        if start not in self.graph.adjacency_list:
             raise ValueError(f"El nodo {start} no existe en el grafo")
        if end not in self.graph.adjacency_list:
             raise ValueError(f"El nodo {end} no existe en el grafo")
        
        if start == end:
            return [start]

        parent: Dict[int, Optional[int]] = {start: None}
        visited: Set[int] = {start}
        queue = deque([start])
        
        found = False
        
        while queue and not found:
            current = queue.popleft()
            
            if current == end:
                found = True
                break
            
            for neighbor_name in self.graph.adjacency_list[current]:
                if neighbor_name not in visited:
                    visited.add(neighbor_name)
                    parent[neighbor_name] = current
                    queue.append(neighbor_name)
        
        if not found:
            return None
        
        # Reconstruir camino
        path: List[int] = []
        node = end
        while node is not None:
            path.append(node)
            node = parent.get(node)
        
        path.reverse()

        if path[0] == start:
            return path
        else:
            return None # No se encontró un camino válido

    ### MEJORA (Extensibilidad): Añadido BFS Bidireccional ###
    def find_shortest_path_bidirectional(self, start: int, end: int) -> Optional[List[int]]:
        """
        Encuentra el camino más corto usando BFS Bidireccional.
        Más eficiente para grafos grandes.
        
        NOTA: Esta implementación simple asume un grafo NO DIRIGIDO.
        Para un grafo dirigido, requeriría un grafo transpuesto.
        """
        if self.graph.directed:
            raise ValueError(
                "BFS Bidireccional simple solo implementado para grafos no dirigidos."
            )
        
        if start not in self.graph.adjacency_list:
            raise ValueError(f"Nodo {start} no existe")
        if end not in self.graph.adjacency_list:
            raise ValueError(f"Nodo {end} no existe")

        if start == end:
            return [start]

        # BFS desde el inicio
        queue_start = deque([start])
        visited_start = {start: None}  # Almacena {nodo: padre}

        # BFS desde el final
        queue_end = deque([end])
        visited_end = {end: None}  # Almacena {nodo: padre}
        
        meeting_point = None

        while queue_start and queue_end and not meeting_point:
            
            # --- Expansión desde el INICIO ---
            current_start = queue_start.popleft()
            if current_start in visited_end:
                meeting_point = current_start
                break

            for neighbor in self.graph.adjacency_list[current_start]:
                if neighbor not in visited_start:
                    visited_start[neighbor] = current_start
                    queue_start.append(neighbor)

            if not queue_start: break

            # --- Expansión desde el FINAL ---
            current_end = queue_end.popleft()
            if current_end in visited_start:
                meeting_point = current_end
                break

            for neighbor in self.graph.adjacency_list[current_end]:
                if neighbor not in visited_end:
                    visited_end[neighbor] = current_end
                    queue_end.append(neighbor)

        if not meeting_point:
            return None

        # --- Reconstruir camino ---
        path = []
        node = meeting_point
        while node is not None:
            path.append(node)
            node = visited_start.get(node)
        path.reverse()
        
        # Quitar el punto de encuentro duplicado
        path.pop() 

        node = visited_end.get(meeting_point)
        while node is not None:
            path.append(node)
            node = visited_end.get(node)

        return path


# ========================================
# PROGRAMA DE DEMOSTRACIÓN (CORREGIDO)
# ========================================

def main():
    """Función principal de demostración."""
    print("=== DEMOSTRACIÓN BFS Y DFS ===\n")
    
    # Crear grafo no dirigido (red social)
    graph = GraphTraversal(directed=False)
    edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (5, 7)]
    for u, v in edges:
        graph.add_edge(u, v)
    
    print("Grafo: 1-2, 1-3, 2-4, 2-5, 3-6, 5-7")
    print()
    
    # BFS
    print("--- BFS desde nodo 1 ---")
    bfs_result = graph.bfs(1)
    print(f"Orden: {' → '.join(map(str, bfs_result))}")
    
    distances = graph.bfs_distances(1)
    print("Distancias desde 1 (solo alcanzables):")
    for node in sorted(distances.keys()):
        print(f"   Nodo {node}: {distances[node]} aristas")
    
    levels = graph.bfs_levels(1)
    print("Nodos por nivel:")
    for level in sorted(levels.keys()):
        print(f"   Nivel {level}: {levels[level]}")
    print()
    
    # DFS
    print("--- DFS desde nodo 1 ---")
    dfs_rec = graph.dfs_recursive(1)
    print(f"Recursivo: {' → '.join(map(str, dfs_rec))}")
    
    dfs_iter = graph.dfs_iterative(1)
    print(f"Iterativo: {' → '.join(map(str, dfs_iter))}")
    print()
    
    # PathFinder (BFS Estándar)
    print("--- Camino más corto de 1 a 7 (BFS Estándar) ---")
    path_finder = PathFinder(graph)
    path = path_finder.find_shortest_path(1, 7)
    
    if path:
        print(f"Camino: {' → '.join(map(str, path))}")
        print(f"Longitud: {len(path) - 1} aristas")
    else:
        print("No se encontró camino.")
    print()

    ### MEJORA: Demo del BFS Bidireccional ###
    print("--- Camino más corto de 1 a 7 (BFS Bidireccional) ---")
    try:
        bi_path = path_finder.find_shortest_path_bidirectional(1, 7)
        if bi_path:
            # El orden puede ser [1, 2, 5, 7] o [1, 3, 6, ...] 
            # dependiendo de la implementación.
            # Lo importante es la longitud.
            print(f"Camino encontrado: {' → '.join(map(str, bi_path))}")
            print(f"Longitud: {len(bi_path) - 1} aristas")
        else:
            print("No se encontró camino.")
    except ValueError as e:
        print(f"Error: {e}")
    print()
    
    # Detección de ciclos (grafo dirigido)
    print("--- Detección de Ciclos (Dirigido) ---")
    digraph = GraphTraversal(directed=True)
    digraph.add_edge(1, 2)
    digraph.add_edge(2, 3)
    digraph.add_edge(3, 1)  # Ciclo: 1→2→3→1
    digraph.add_edge(3, 4)
    
    print("Grafo dirigido: 1→2, 2→3, 3→1, 3→4")
    print(f"¿Tiene ciclo? {'SÍ' if digraph.has_cycle_directed() else 'NO'}")
    print()

    #
    print("--- Detección de Ciclos (Dirigido) ---")
    digraph = GraphTraversal(directed=True)
    digraph.add_edge(1, 2)
    digraph.add_edge(2, 3)
    digraph.add_edge(3, 4)  
    digraph.add_edge(4, 2)
    
    print("Grafo dirigido: 1→2, 2→3, 3→4, 4→2")
    print(f"¿Tiene ciclo? {'SÍ' if digraph.has_cycle_directed() else 'NO'}")
    print()


    # Ordenamiento topológico
    print("--- Ordenamiento Topológico ---")
    dag = GraphTraversal(directed=True)
    dag.add_edge(1, 2)
    dag.add_edge(1, 3)
    dag.add_edge(2, 4)
    dag.add_edge(3, 4)
    
    print("DAG: 1→2, 1→3, 2→4, 3→4")
    topo_sort = dag.topological_sort()
    if topo_sort:
        print(f"Orden topológico: {' → '.join(map(str, topo_sort))}")
    print()
    
    # Componentes conectadas
    print("--- Componentes Conectadas ---")
    disconnected = GraphTraversal(directed=False)
    disconnected.add_edge(1, 2)
    disconnected.add_edge(2, 3)
    disconnected.add_edge(4, 5)
    disconnected.add_edge(6, 7)
    disconnected.add_edge(7, 8)
    disconnected.add_edge(9, 9) # Nodo aislado
    
    print("Grafo: {1-2-3}, {4-5}, {6-7-8}, {9}")
    components = disconnected.find_connected_components()
    print(f"Número de componentes: {len(components)}")
    for i, comp in enumerate(components, 1):
        print(f"   Componente {i}: {sorted(comp)}")


if __name__ == "__main__":
    #El codigo funciona con los mismos test que aplicamos en la integracion con la semana 4 👻
    main()