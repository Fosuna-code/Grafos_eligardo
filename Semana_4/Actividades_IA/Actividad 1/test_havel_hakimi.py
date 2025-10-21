from typing import List
def is_graphical_sequence(degrees: List[int]) -> bool:
    """
    Valida secuencia gráfica con Havel-Hakimi.
    Complejidad: O(n² log n) por reordenamiento en cada iteración.
    """
    if not degrees:
        return True
    
    # Crear copia para no modificar original
    seq = sorted(degrees, reverse=True)
    
    # Verificar suma par y máx grado
    total_sum = sum(seq)
    if total_sum % 2 != 0 or seq[0] >= len(seq):
        return False
    
    while seq:
        d1 = seq.pop(0)
        
        if d1 == 0:
            return True
        
        if d1 > len(seq):
            return False
        
        # Restar 1 de los siguientes d1
        for i in range(d1):
            seq[i] -= 1
            if seq[i] < 0:
                return False
        
        # CRÍTICO: Reordenar después de modificar
        seq.sort(reverse=True)
    
    return True


secuencias_validas = [
    [2, 2, 1, 1],          # n=4
    [5, 1, 1, 1, 1, 1],    # n=6
    [4, 4, 4, 4, 4, 4, 4, 4], # n=8
    [7, 6, 5, 4, 4, 3, 2, 1, 1, 1], # n=10
    [10, 9, 8, 7, 6, 5, 5, 4, 3, 2, 2, 2, 1, 1, 1] # n=15
]
for secuencia in secuencias_validas:
    if not is_graphical_sequence(secuencia):
        print(f"Error: La secuencia válida {secuencia} fue marcada como inválida.")
    if is_graphical_sequence(secuencia) == True:
        print(f"Secuencia válida {secuencia} correctamente identificada.")   

secuencias_invalidas = [
    [4, 3, 2, 1, 1],       # Razón: Suma impar
    [6, 5, 4, 3, 2, 1],    # Razón: Grado máximo >= n
    [5, 4, 3, 1, 1, 0],    # Razón: Genera grados negativos
    [5, 5, 4, 3, 2, 1],    # Razón: Falla estructural en iteración intermedia
    [5, 5, 5, 1, 1, 1]     # Razón: Estructura imposible de construir
]

for secuencia in secuencias_invalidas:
    if is_graphical_sequence(secuencia):
        print(f"Error: La secuencia inválida {secuencia} fue marcada como válida.")
    if is_graphical_sequence(secuencia) == False:
        print(f"Secuencia inválida {secuencia} correctamente identificada.")