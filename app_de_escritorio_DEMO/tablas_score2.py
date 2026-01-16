#tablas_score2.py
#Tablas Score2 - Region MODERADO
#Valores de ejemplo clinicamente coherentes (ESC 2021)

SCORE2_MODERADO = {
    #(sexo, fumador, edad, PAS, no-HDL_mg): riesgo %
    # ===== HOMBRES NO FUMADORES =====
    ("Hombre", False, 40, 120, 130): 0.6,
    ("Hombre", False, 45, 120, 130): 1.2,
    ("Hombre", False, 50, 120, 130): 2.1,
    ("Hombre", False, 55, 140, 160): 3.1,
    ("Hombre", False, 60, 140, 160): 5.0,
    ("Hombre", False, 65, 160, 190): 7.8,

    # ===== HOMBRES FUMADORES =====
    ("Hombre", True, 40, 120, 130): 1.3,
    ("Hombre", True, 45, 140, 160): 4.8,
    ("Hombre", True, 50, 140, 160): 6.2,
    ("Hombre", True, 55, 160, 190): 9.5,
    ("Hombre", True, 60, 160, 190): 12.5,

    # ===== MUJERES NO FUMADORAS =====
    ("Mujer", False, 40, 120, 130): 0.3,
    ("Mujer", False, 45, 120, 130): 0.8,
    ("Mujer", False, 50, 120, 130): 1.2,
    ("Mujer", False, 55, 140, 160): 1.8,
    ("Mujer", False, 60, 140, 160): 3.0,
    ("Mujer", False, 65, 160, 190): 4.9,

    # ===== MUJERES FUMADORAS =====
    ("Mujer", True, 45, 140, 160): 3.5,
    ("Mujer", True, 50, 140, 160): 4.9,
    ("Mujer", True, 55, 160, 190): 7.2,
    ("Mujer", True, 60, 160, 190): 9.8,
}