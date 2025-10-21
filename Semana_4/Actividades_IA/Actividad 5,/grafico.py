import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import io

# 1. Prepara tus datos en un string multilínea
data_string = """ZONA,VECINO,DISTANCIA_KM
Condesa,Roma,3
Condesa,Polanco,4
Condesa,Coyoacán,7
Condesa,Providencia,5
Condesa,Las Condes,2
Condesa,Usaquén,8
Roma,Condesa,3
Roma,Polanco,2
Roma,Providencia,6
Roma,Chapinero,5
Roma,Bellavista,9
Polanco,Condesa,4
Polanco,Roma,2
Polanco,Las Condes,3
Polanco,Barrio Italia,7
Polanco,Coyoacán,6
Coyoacán,Condesa,7
Coyoacán,Polanco,6
Coyoacán,Santa Fe,4
Coyoacán,Xochimilco,8
Providencia,Condesa,5
Providencia,Roma,6
Providencia,Belgrano,10
Providencia,Lastarria,3
Las Condes,Condesa,2
Las Condes,Polanco,3
Las Condes,Engativá,7
Las Condes,Ñuñoa,4
Usaquén,Condesa,8
Usaquén,Chapinero,2
Usaquén,Candelaria,5
Usaquén,Palermo,9
Chapinero,Roma,5
Chapinero,Usaquén,2
Chapinero,Teusaquillo,1
Chapinero,San Telmo,10
Bellavista,Roma,9
Bellavista,Barrio Italia,1
Bellavista,Lastarria,4
Bellavista,Recoleta,6
Barrio Italia,Polanco,7
Barrio Italia,Bellavista,1
Barrio Italia,Suba,8
Barrio Italia,Montserrat,5
Belgrano,Providencia,10
Belgrano,Engativá,6
Belgrano,Zócalo,8
Engativá,Las Condes,7
Engativá,Belgrano,6
Engativá,Teusaquillo,4
Santa Fe,Coyoacán,4
Santa Fe,Xochimilco,3
Santa Fe,La Boca,10
Palermo,Usaquén,9
Palermo,San Telmo,4
Palermo,Recoleta,2
San Telmo,Chapinero,10
San Telmo,Palermo,4
San Telmo,La Boca,1
Teusaquillo,Chapinero,1
Teusaquillo,Engativá,4
Teusaquillo,Candelaria,3
Candelaria,Usaquén,5
Candelaria,Teusaquillo,3
Lastarria,Providencia,3
Lastarria,Bellavista,4
Xochimilco,Coyoacán,8
Xochimilco,Santa Fe,3
Xochimilco,Zócalo,9
Zócalo,Belgrano,8
Zócalo,Xochimilco,9
La Boca,Santa Fe,10
La Boca,San Telmo,1
Recoleta,Bellavista,6
Recoleta,Palermo,2
Ñuñoa,Las Condes,4
Ñuñoa,Suba,7
Suba,Barrio Italia,8
Suba,Ñuñoa,7
Montserrat,Barrio Italia,5
"""

# 2. Lee los datos en un DataFrame de pandas
# io.StringIO permite tratar el string como si fuera un archivo
df = pd.read_csv(io.StringIO(data_string))

# 3. Crea el grafo a partir del DataFrame
# Se usa nx.Graph() para que las conexiones no tengan dirección (A->B es lo mismo que B->A)
G = nx.from_pandas_edgelist(df, 'ZONA', 'VECINO', edge_attr='DISTANCIA_KM', create_using=nx.Graph())

# 4. Dibuja el grafo
# Define un tamaño más grande para la figura para que se vea mejor
plt.figure(figsize=(20, 16))

# Elige un algoritmo de disposición para los nodos.
# 'kamada_kawai_layout' es bueno para visualizar la estructura del grafo
pos = nx.kamada_kawai_layout(G)

# Dibuja los nodos, etiquetas y aristas con personalización
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2500,
        edge_color='gray', font_size=12, font_weight='bold', width=1.5)

# Extrae los pesos (distancias) para ponerlos como etiquetas en las aristas
edge_labels = nx.get_edge_attributes(G, 'DISTANCIA_KM')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='darkred', font_size=10)

# Añade un título al gráfico
plt.title("Grafo de Conexiones y Distancias entre Zonas", size=25)

# Guarda la figura en un archivo PNG con alta resolución
plt.savefig("grafo_conexiones.png", format="PNG", dpi=300)

# Muestra un mensaje en la consola confirmando que se guardó
print("El gráfico se ha guardado exitosamente como 'grafo_conexiones.png'")

# Opcional: si quieres mostrar el gráfico en una ventana emergente (en un entorno de escritorio)
# plt.show()