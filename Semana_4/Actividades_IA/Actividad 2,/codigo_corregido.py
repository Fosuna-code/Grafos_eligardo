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
