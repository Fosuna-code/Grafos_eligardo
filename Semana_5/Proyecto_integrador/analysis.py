import os
from collections import deque, defaultdict
from typing import Dict, List, Set, Tuple, Optional


class GraphTraversal:
    """
    Clase que implementa la estructura del grafo y los algoritmos
    de exploración (BFS, DFS) y análisis.
    """
    
    def __init__(self, directed: bool = False):
        """
        Inicializa el grafo.
        
        Args:
            directed: True si el grafo es dirigido, False en caso contrario.
        """
        self.adjacency_list: Dict[str, List[Tuple[str, float]]] = defaultdict(list)
        self.directed = directed

    def load_from_file(self, file_path: str):
        """
        Carga un grafo desde un archivo de texto con manejo robusto de errores.
        (Lógica movida desde la función global 'load_graph')
        """
        if not os.path.exists(file_path):
            print(f"❌ Error: El archivo '{file_path}' no existe.")
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    
                    if not line or line.startswith('#'):
                        continue
                    
                    parts = line.split()
                    if len(parts) < 2:
                        print(f"⚠️  Línea {line_num}: '{line}' ignorada (faltan vértices)")
                        continue
                    
                    from_vertex, to_vertex = parts[0], parts[1]
                    
                    try:
                        weight = float(parts[2]) if len(parts) > 2 else 1.0
                    except (ValueError, IndexError):
                        print(f"⚠️  Línea {line_num}: peso inválido, usando 1.0")
                        weight = 1.0
                    
                    # Agregar arista
                    self.adjacency_list[from_vertex].append((to_vertex, weight))
                    
                    # Asegurar que el nodo 'to_vertex' exista en el dict
                    # si es un nodo sumidero (sin aristas salientes)
                    if to_vertex not in self.adjacency_list:
                         self.adjacency_list[to_vertex] = []
                         
                    # Si es no dirigido, agregar arista inversa
                    if not self.directed:
                        self.adjacency_list[to_vertex].append((from_vertex, weight))
                        
        except FileNotFoundError:
            print(f"❌ Error: No se encontró el archivo '{file_path}'")
        except Exception as e:
            print(f"❌ Error inesperado al leer '{file_path}': {e}")
            
    # --- Métodos de Análisis (Movidos desde funciones globales) ---

    def get_neighbors(self, vertex: str) -> List[Tuple[str, float]]:
        """Obtiene la lista de vecinos de un vértice."""
        return self.adjacency_list.get(vertex, [])

    def has_edge(self, from_vertex: str, to_vertex: str) -> bool:
        """Verifica si existe una arista de from_vertex a to_vertex."""
        neighbors = self.adjacency_list.get(from_vertex, [])
        return any(neighbor == to_vertex for neighbor, _ in neighbors)

    def get_out_degree(self, vertex: str) -> int:
        """Calcula el grado de salida de un vértice."""
        return len(self.adjacency_list.get(vertex, []))

    def get_in_degree(self, vertex: str) -> int:
        """Calcula el grado de entrada de un vértice."""
        in_degree = 0
        for neighbors in self.adjacency_list.values():
            in_degree += sum(1 for neighbor, _ in neighbors if neighbor == vertex)
        return in_degree

    def analyze_graph(self, graph_type: str):
        """Analiza y muestra estadísticas detalladas del grafo."""
        print(f"\n{'='*50}")
        print(f"🔍 Análisis del Grafo {graph_type}")
        print(f"{'='*50}")
        
        if not self.adjacency_list:
            print("⚠️  El grafo está vacío")
            return
        
        vertices = sorted(self.adjacency_list.keys())
        total_edges = sum(len(neighbors) for neighbors in self.adjacency_list.values())
        
        print(f"📊 Estadísticas generales:")
        print(f"   • Vértices: {len(vertices)}")
        print(f"   • Aristas: {total_edges}")
        
        max_possible_edges = len(vertices) * (len(vertices) - 1)
        if max_possible_edges > 0:
            density = total_edges / max_possible_edges
            print(f"   • Densidad: {density:.3f}")
        
        print(f"\n🔍 Detalles por vértice:")
        for vertex in vertices:
            out_deg = self.get_out_degree(vertex)
            in_deg = self.get_in_degree(vertex)
            neighbors = self.get_neighbors(vertex)
            
            neighbor_str = ", ".join([f"{neighbor}({weight:.1f}km)" for neighbor, weight in neighbors])
            
            print(f"   {vertex}: Out-degree={out_deg}, In-degree={in_deg}")
            if neighbors:
                print(f"       └─ Vecinos: [{neighbor_str}]")

    def find_most_connected_vertex(self) -> str:
        """Encuentra el vértice con mayor grado total (entrada + salida)."""
        if not self.adjacency_list:
            return ""
        
        max_degree = -1
        most_connected = ""
        
        for vertex in self.adjacency_list.keys():
            total_degree = self.get_out_degree(vertex) + self.get_in_degree(vertex)
            if total_degree > max_degree:
                max_degree = total_degree
                most_connected = vertex
        
        return most_connected
        
    def extract_degree_sequence(self) -> List[int]:
        """Extrae la secuencia de grados del grafo."""
        degrees = [self.get_out_degree(v) for v in self.adjacency_list.keys()]
        return sorted(degrees, reverse=True)

    def validate_consistency(self) -> bool:
        """Verifica consistencia: suma de grados debe ser par."""
        total_degree = sum(len(neighbors) for neighbors in self.adjacency_list.values())
        return total_degree % 2 == 0

    def adjMatrix(self) -> Tuple[List[List[int]], Dict[str, int]]:
        """Convierte lista de adyacencia a matriz de adyacencia."""
        vertices = sorted(self.adjacency_list.keys())
        index_map = {vertex: idx for idx, vertex in enumerate(vertices)}
        size = len(vertices)
        
        matrix = [[0]*size for _ in range(size)]
        
        for from_vertex, neighbors in self.adjacency_list.items():
            from_idx = index_map[from_vertex]
            for to_vertex, _ in neighbors:
                if to_vertex in index_map: # Asegurarse que el vecino está
                    to_idx = index_map[to_vertex]
                    matrix[from_idx][to_idx] = 1
        
        return matrix, index_map

    def verify_consistency(self, matrix: List[List[int]], index_map: Dict[str, int]) -> List[str]:
        """Compara la lista de adyacencia y la matriz."""
        inconsistencies = []
        vertex_map = {idx: vertex for vertex, idx in index_map.items()}
        
        # 1. Verificación: Lista -> Matriz
        for from_vertex, neighbors in self.adjacency_list.items():
            for to_vertex, _ in neighbors:
                if from_vertex in index_map and to_vertex in index_map:
                    from_idx = index_map[from_vertex]
                    to_idx = index_map[to_vertex]
                    if matrix[from_idx][to_idx] == 0:
                        error_msg = f"❌ Inconsistencia: Arista {from_vertex}→{to_vertex} existe en la lista pero no en la matriz."
                        inconsistencies.append(error_msg)

        # 2. Verificación: Matriz -> Lista
        for from_idx, row in enumerate(matrix):
            for to_idx, value in enumerate(row):
                if value == 1:
                    from_vertex = vertex_map[from_idx]
                    to_vertex = vertex_map[to_idx]
                    if not self.has_edge(from_vertex, to_vertex):
                        error_msg = f"❌ Inconsistencia: Arista {from_vertex}→{to_vertex} existe en la matriz pero no en la lista."
                        inconsistencies.append(error_msg)
                        
        return inconsistencies
        
    # ========================================
    # NUEVOS MÉTODOS: BFS Y DFS
    # ========================================

    def bfs(self, start_vertex: str) -> List[str]:
        """
        Realiza un recorrido en Amplitud (BFS) desde un nodo inicial.
        Ignora los pesos, solo sigue la conectividad.
        """
        if start_vertex not in self.adjacency_list:
            raise ValueError(f"El nodo '{start_vertex}' no existe en el grafo")

        visited: Set[str] = set()
        result: List[str] = []
        queue = deque([start_vertex])
        
        visited.add(start_vertex)
        
        while queue:
            current = queue.popleft()
            result.append(current)
            
            # Adaptado para tuplas (vecino, peso)
            for neighbor_name, _ in self.adjacency_list[current]:
                if neighbor_name not in visited:
                    visited.add(neighbor_name)
                    queue.append(neighbor_name)
        
        return result

    def dfs_recursive(self, start_vertex: str) -> List[str]:
        """
        Realiza un recorrido en Profundidad (DFS) recursivo.
        """
        if start_vertex not in self.adjacency_list:
            raise ValueError(f"El nodo '{start_vertex}' no existe en el grafo")

        visited: Set[str] = set()
        result: List[str] = []
        
        def dfs_helper(node: str):
            visited.add(node)
            result.append(node)
            
            # Adaptado para tuplas (vecino, peso)
            for neighbor_name, _ in self.adjacency_list[node]:
                if neighbor_name not in visited:
                    dfs_helper(neighbor_name)
        
        dfs_helper(start_vertex)
        return result

# ========================================
# CLASE PARA BÚSQUEDA DE CAMINOS
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

    def find_shortest_path(self, start: str, end: str) -> Optional[List[str]]:
        """
        Encuentra el camino más corto (en número de saltos) usando BFS.
        """
        if start not in self.graph.adjacency_list:
             raise ValueError(f"El nodo {start} no existe en el grafo")
        if end not in self.graph.adjacency_list:
             raise ValueError(f"El nodo {end} no existe en el grafo")
        
        if start == end:
            return [start]

        parent: Dict[str, Optional[str]] = {start: None}
        visited: Set[str] = {start}
        queue = deque([start])
        
        found = False
        
        while queue and not found:
            current = queue.popleft()
            
            if current == end:
                found = True
                break
            
            # Adaptado para tuplas (vecino, peso)
            for neighbor_name, _ in self.graph.adjacency_list[current]:
                if neighbor_name not in visited:
                    visited.add(neighbor_name)
                    parent[neighbor_name] = current
                    queue.append(neighbor_name)
        
        if not found:
            return None
        
        # Reconstruir camino
        path: List[str] = []
        node = end
        while node is not None:
            path.append(node)
            node = parent.get(node)
        
        path.reverse()

        if path[0] == start:
            return path
        else:
            return None # No se encontró un camino válido

# ========================================
# FUNCIONES GLOBALES (Algoritmos puros)
# ========================================

def is_graphical_sequence(degrees: List[int]) -> bool:
    """
    Valida secuencia gráfica con Havel-Hakimi.
    """
    if not degrees:
        return True
    
    seq = sorted(degrees, reverse=True)
    
    total_sum = sum(seq)
    if total_sum % 2 != 0:
        return False
    
    # Manejar secuencias con solo ceros
    if seq[0] == 0:
        return True
        
    if seq[0] >= len(seq):
        return False
    
    while seq:
        d1 = seq.pop(0)
        
        if d1 == 0:
            return True
        
        if d1 > len(seq):
            return False
        
        for i in range(d1):
            seq[i] -= 1
            if seq[i] < 0:
                return False
        
        seq.sort(reverse=True)
    
    return True

# ========================================
# PROGRAMA PRINCIPAL (Refactorizado)
# ========================================

def main():
    """Función principal para análisis de grafos."""
    print("🌍 === Análisis de Mapas de Tráfico - Proyecto Semana 3 ===")
    
    # --- Analizar grafo no dirigido ---
    undirected_graph = GraphTraversal(directed=False)
    undirected_graph.load_from_file("edges_undirected.txt")
    undirected_graph.analyze_graph("No Dirigido")
    
    # --- Analizar grafo dirigido ---
    directed_graph = GraphTraversal(directed=True)
    directed_graph.load_from_file("edges_directed.txt")
    directed_graph.analyze_graph("Dirigido")
    
    # --- Pruebas de conectividad (ahora usando métodos de clase) ---
    print(f"\n{'='*50}")
    print("🔗 Pruebas de Conectividad")
    print(f"{'='*50}")
    
    if directed_graph.adjacency_list:
        print(f"¿A→G dirigido? {directed_graph.has_edge('A', 'G')} (esperado: True)")
        print(f"¿G→A dirigido? {directed_graph.has_edge('G', 'A')} (esperado: False)")
        
        if 'A' in directed_graph.adjacency_list:
            print(f"Grado de salida de A: {directed_graph.get_out_degree('A')}")
            print(f"Grado de entrada de A: {directed_graph.get_in_degree('A')}")
        
        most_connected = directed_graph.find_most_connected_vertex()
        if most_connected:
            print(f"Vértice más conectado: {most_connected}")
    
    # ========================================
    # NUEVA SECCIÓN: DEMOSTRACIÓN BFS, DFS Y PATHFINDER
    # ========================================
    print(f"\n{'='*50}")
    print("🚀 Demostración de Recorridos y Búsqueda de Caminos")
    print(f"{'='*50}")

    if directed_graph.adjacency_list:
        start_node = 'A'
        end_node = 'G'
        
        try:
            # 1. Prueba BFS
            print(f"Recorrido BFS desde '{start_node}':")
            bfs_result = directed_graph.bfs(start_node)
            print(f"   -> {' → '.join(bfs_result)}")
            
            # 2. Prueba DFS
            print(f"Recorrido DFS desde '{start_node}':")
            dfs_result = directed_graph.dfs_recursive(start_node)
            print(f"   -> {' → '.join(dfs_result)}")
            
            # 3. Prueba PathFinder
            print(f"Buscando camino más corto de '{start_node}' a '{end_node}':")
            path_finder = PathFinder(directed_graph)
            shortest_path = path_finder.find_shortest_path(start_node, end_node)
            
            if shortest_path:
                print(f"   -> Camino encontrado: {' → '.join(shortest_path)}")
                print(f"   -> Longitud: {len(shortest_path) - 1} saltos")
            else:
                print(f"   -> No se encontró camino de '{start_node}' a '{end_node}'")

        except ValueError as e:
            print(f"Error en la demostración: {e}")
            
    # --- Implementación Hakimi ---
    print(f"\n{'='*50}")
    print("🛡️  Pruebas de Havel-Hakimi")
    print(f"{'='*50}")
    
    seq_valid = [3, 2, 2, 1]
    print(f"Caso 1: {seq_valid} -> {'✓ Gráfica' if is_graphical_sequence(seq_valid) else '✖ No Gráfica'}")
    seq_invalid = [3, 3, 3, 1]
    print(f"Caso 2: {seq_invalid} -> {'✓ Gráfica' if is_graphical_sequence(seq_invalid) else '✖ No Gráfica'}")

    if undirected_graph.adjacency_list:
        extracted_seq = undirected_graph.extract_degree_sequence()
        print(f"\nSecuencia del mapa (no dirigido): {extracted_seq}")
        print(f"¿Es gráfica? {'✓ Gráfica' if is_graphical_sequence(extracted_seq) else '✖ No Gráfica'}")
        print(f"¿Consistente (suma par)? {'✓ Consistente' if undirected_graph.validate_consistency() else '✖ Inconsistente'}")

    # --- Matriz de adyacencia ---
    print(f"\n{'='*50}")
    print("🧮 Matriz de Adyacencia (Grafo Dirigido)")
    print(f"{'='*50}")
    
    if directed_graph.adjacency_list:
        matrix, index_map = directed_graph.adjMatrix()
        vertices_list = sorted(index_map.keys())
        
        # Imprimir cabecera
        print("    ", end="")
        for v in vertices_list:
            print(f" {v} ", end="")
        print()
        print("  " + "---" * len(vertices_list))
        
        # Imprimir filas
        for idx, row in enumerate(matrix):
            print(f"{vertices_list[idx]} |", end="")
            for val in row:
                print(f" {val} ", end="")
            print()

        # --- Verificación de Consistencia ---
        print("\n" + "="*50)
        print("Verificación de Consistencia: Lista vs. Matriz")
        print("="*50)

        inconsistencies = directed_graph.verify_consistency(matrix, index_map)
        if not inconsistencies:
            print("¡Éxito! La lista de adyacencia y la matriz son consistentes.")
        else:
            print("Se encontraron las siguientes inconsistencias:")
            for error in inconsistencies:
                print(f"   • {error}")
    
    print("\n🎉 ¡Análisis completado exitosamente!")


if __name__ == "__main__":
    main()