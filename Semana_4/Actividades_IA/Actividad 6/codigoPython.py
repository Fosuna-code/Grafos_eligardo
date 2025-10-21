from collections import defaultdict
import os

class Graph:
    """
    Una implementación de un grafo ponderado (dirigido o no dirigido)
    usando una lista de adyacencia.
    """
    def __init__(self):
        """
        Inicializa un grafo vacío usando un defaultdict para la lista de adyacencia.
        """
        self.adjacency_list = defaultdict(list)

    def add_vertex(self, vertex):
        """
        Asegura que un vértice exista en el grafo, incluso si no tiene aristas.
        Gracias a defaultdict, esto no es estrictamente necesario para agregar aristas,
        pero es útil para nodos aislados.
        """
        # Acceder a la clave es suficiente para que defaultdict la cree si no existe.
        self.adjacency_list[vertex]

    def add_edge(self, from_vertex, to_vertex, weight=1.0, is_directed=True):
        """
        Agrega una arista entre dos vértices. Si el grafo no es dirigido,
        agrega también la arista en la dirección opuesta.
        """
        self.adjacency_list[from_vertex].append((to_vertex, weight))
        if not is_directed:
            self.adjacency_list[to_vertex].append((from_vertex, weight))

    def get_out_degree(self, vertex):
        """Devuelve el grado de salida (número de aristas que salen) de un vértice."""
        return len(self.adjacency_list.get(vertex, []))

    def get_in_degree(self, vertex):
        """
        Devuelve el grado de entrada (número de aristas que apuntan) a un vértice.
        Esto requiere recorrer todas las aristas del grafo.
        """
        return sum(1 for neighbors in self.adjacency_list.values()
                   for neighbor, _ in neighbors if neighbor == vertex)

    def has_edge(self, from_vertex, to_vertex):
        """Verifica si existe una arista directa de from_vertex a to_vertex."""
        if from_vertex not in self.adjacency_list:
            return False
        # Usa una expresión generadora con `any` para una búsqueda eficiente.
        return any(neighbor == to_vertex for neighbor, _ in self.adjacency_list[from_vertex])

    def export_to_file(self, filename, include_weights=True, deduplicate_undirected=False):
        """Exporta el grafo a un archivo de texto, una arista por línea."""
        processed_edges = set()
        try:
            # 'with' asegura que el archivo se cierre correctamente.
            with open(filename, 'w', encoding='utf-8') as writer:
                # Itera sobre los vértices ordenados para una salida consistente.
                for vertex in sorted(self.adjacency_list):
                    for neighbor, weight in self.adjacency_list[vertex]:
                        if deduplicate_undirected:
                            # Crea una clave canónica usando una tupla ordenada para
                            # evitar duplicados como (A, B) y (B, A).
                            edge = tuple(sorted((vertex, neighbor)))
                            if edge in processed_edges:
                                continue
                            processed_edges.add(edge)

                        if include_weights:
                            line = f"{vertex} {neighbor} {weight:.1f}"
                        else:
                            line = f"{vertex} {neighbor}"
                        writer.write(line + '\n')
            print(f"✅ Archivo '{filename}' exportado exitosamente.")
        except IOError as e:
            print(f"❌ Error al exportar archivo: {e}")

    def __str__(self):
        """Representación en string del grafo para imprimirlo fácilmente."""
        parts = ["=== Estructura del Grafo ==="]
        for vertex in sorted(self.adjacency_list):
            neighbors = ", ".join(f"{n}({w:.1f})" for n, w in self.adjacency_list[vertex])
            parts.append(f"{vertex}: [{neighbors}]")
        return "\n".join(parts)

def main():
    """
    Función principal para crear, probar y exportar los grafos.
    """
    print("🌍 === Generando Mapa de Tráfico con Python === 🌍")

    # --- Grafo No Dirigido ---
    undirected = Graph()
    print("\n🛣️  Agregando calles bidireccionales...")
    undirected.add_edge("A", "B", 2.0, is_directed=False)
    undirected.add_edge("A", "C", 3.0, is_directed=False)
    undirected.add_edge("B", "D", 1.0, is_directed=False)
    undirected.add_edge("C", "E", 4.0, is_directed=False)
    undirected.add_edge("D", "F", 5.0, is_directed=False)
    undirected.add_edge("E", "F", 2.0, is_directed=False)
    undirected.add_edge("G", "H", 6.0, is_directed=False)

    undirected.export_to_file("edges_undirected.txt", include_weights=True, deduplicate_undirected=True)

    # --- Grafo Dirigido ---
    directed = Graph()
    print("\n🚦 Creando mapa completo con calles direccionales...")

    # Aristas dirigidas específicas
    directed.add_edge("A", "G", 1.0)
    directed.add_edge("B", "H", 3.0)
    directed.add_edge("C", "D", 2.0)
    directed.add_edge("F", "E", 4.0)
    directed.add_edge("H", "A", 5.0)

    # Agregar las bidireccionales como dos aristas dirigidas
    edges_to_add = [
        ("A", "B", 2.0), ("A", "C", 3.0), ("B", "D", 1.0), ("C", "E", 4.0),
        ("D", "F", 5.0), ("E", "F", 2.0), ("G", "H", 6.0)
    ]
    for v1, v2, w in edges_to_add:
        directed.add_edge(v1, v2, w)
        directed.add_edge(v2, v1, w)

    directed.export_to_file("edges_directed.txt", include_weights=True)

    # --- Pruebas de Funcionalidad ---
    print("\n🧪 === Pruebas de Funcionalidad ===")
    print(undirected) # Imprime la estructura del grafo no dirigido
    print(f"Grado de A (no dirigido): {undirected.get_out_degree('A')} (esperado: 2)")
    print(f"¿Existe A↔B no dirigido? {undirected.has_edge('A', 'B')} (esperado: True)")
    print(f"¿Existe B↔A no dirigido? {undirected.has_edge('B', 'A')} (esperado: True)")

    print(f"\n{directed}") # Imprime la estructura del grafo dirigido
    print(f"Grado salida A (dirigido): {directed.get_out_degree('A')} (esperado: 3)")
    print(f"Grado entrada A (dirigido): {directed.get_in_degree('A')} (esperado: 1)")
    print(f"¿Existe A→G dirigido? {directed.has_edge('A', 'G')} (esperado: True)")
    print(f"¿Existe G→A dirigido? {directed.has_edge('G', 'A')} (esperado: False)")

    print("\n🎉 ¡Proyecto Python completado exitosamente!")

# Este es el punto de entrada estándar para un script de Python.
if __name__ == "__main__":
    main()