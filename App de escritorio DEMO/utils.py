# utils.py

EDADES = [40, 45, 50, 55, 60, 65, 70, 75]
PAS_CORTES = [120, 140, 160, 180]
NO_HDL_CORTES = [130, 160, 190, 220]

def discretizar(valor, cortes):
    """
    Devuelve el mayor corte <= valor
    """
    for c in reversed(cortes):
        if valor >= c:
            return c
    return cortes[0]
