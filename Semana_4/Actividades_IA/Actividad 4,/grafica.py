#Codigo Creado en conjunto Fernando Osuna Manzo y Gemini
# Para ver la grafica, asegúrate de tener matplotlib instalado:
# pip install matplotlib numpy



import matplotlib.pyplot as plt
import numpy as np

# --- Datos Experimentales ---
# (n, tiempo_naive, tiempo_heap)
datos_dispersos = [
    (100, 0.0031, 0.0004),
    (500, 0.2815, 0.0025),
    (1000, 2.1521, 0.0058),
    (2000, 16.995, 0.0139),
    (5000, 175.0, 0.0415) # Usando el valor estimado para la curva
]

# (n, tiempo_naive, tiempo_heap)
datos_densos = [
    (100, 0.0049, 0.0028),
    (500, 0.4933, 0.0989),
    (1000, 4.6850, 0.4552),
    (2000, 35.841, 2.1091)
    # Excluimos el n=5000 para el ajuste naive denso por ser un estimado muy lejano
]

# --- Extracción de datos para graficar ---
n_dispersos = [d[0] for d in datos_dispersos]
naive_dispersos = [d[1] for d in datos_dispersos]
heap_dispersos = [d[2] for d in datos_dispersos]

n_densos = [d[0] for d in datos_densos]
naive_densos = [d[1] for d in datos_densos]
heap_densos = [d[2] for d in datos_densos]

# --- Creación de la Gráfica ---
# plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(10, 7))

# --- Graficar los puntos de datos experimentales ---
ax.scatter(n_dispersos, naive_dispersos, color='blue', label='Naive - Disperso ($O(n^2 \log n)$)', s=50)
ax.scatter(n_densos, naive_densos, color='cornflowerblue', marker='x', label='Naive - Denso', s=50)
ax.scatter(n_dispersos, heap_dispersos, color='green', label='Heap - Disperso ($O(m \log n)$)', s=50)
ax.scatter(n_densos, heap_densos, color='limegreen', marker='x', label='Heap - Denso', s=50)


# --- Ajuste y Gráfica de Curvas de Regresión (Polinómica en espacio logarítmico) ---
# Se ajusta un polinomio a los datos transformados a logaritmo, que equivale a una ley de potencias.

# Regresión para Naive (ajuste de grado 2 para capturar mejor la curva n^2*log(n))
n_fit = np.linspace(min(n_dispersos), max(n_dispersos), 400)
log_n = np.log(n_dispersos)
log_t_naive = np.log(naive_dispersos)
fit_naive = np.polyfit(log_n, log_t_naive, 2)
p_naive = np.poly1d(fit_naive)
ax.plot(n_fit, np.exp(p_naive(np.log(n_fit))), color='darkblue', linestyle='--')

# Regresión para Heap (ajuste de grado 1, ya que se aproxima a n*log(n))
log_n_heap = np.log(n_dispersos + n_densos)
log_t_heap = np.log(heap_dispersos + heap_densos)
fit_heap = np.polyfit(log_n_heap, log_t_heap, 1)
p_heap = np.poly1d(fit_heap)
ax.plot(n_fit, np.exp(p_heap(np.log(n_fit))), color='darkgreen', linestyle='--')


# --- Configuración de la Gráfica ---
ax.set_xscale('log')
ax.set_yscale('log')

ax.set_title('Análisis Experimental: Havel-Hakimi (Naive vs. Heap)', fontsize=16)
ax.set_xlabel('Tamaño de la Secuencia (n) - Escala Logarítmica', fontsize=12)
ax.set_ylabel('Tiempo de Ejecución (segundos) - Escala Logarítmica', fontsize=12)
ax.legend()
ax.minorticks_off()

# --- Mostrar Gráfica ---
# plt.show()
plt.savefig('./grafica_havel_hakimi.png', dpi=300)