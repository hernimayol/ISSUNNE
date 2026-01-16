'''
Score2.py
Motor de cálculo SCORE2/SCORE2-OP
Basado en ESC 2021
Region: MODERADO y MUY ALTO
'''
from tablas_score2 import SCORE2_MODERADO
from utils import discretizar, EDADES,PAS_CORTES,NO_HDL_CORTES

def determinar_modelo(edad: int) -> str:
    """
    Determina el modelo segun la edad

    """
    if edad >= 70:
        return "SCORE2-OP"
    else:
        return "SCORE2"

def categorizar_riesgo(riesgo: float, modelo: str) -> str:
    """
    Clasificacion ESC segun riesgo a 10 años.
    """
    if modelo == "SCORE2":
        if riesgo < 5:
            return "Riesgo Bajo-Moderado"
        elif riesgo < 10:
            return "Riesgo Alto"
        else:
            return "Riesgo Muy Alto"
    elif modelo == "SCORE2-OP":
        if riesgo < 7.5:
            return "Riesgo Bajo-Moderado"
        elif riesgo < 15:
            return "Riesgo Alto"
        else:
            return "Riesgo Muy Alto"
    else:
        raise ValueError("Modelo SCORE desconocido")

def validar_inputs(
        edad: int,
        sexo: str,
        pas: int,
        no_hdl: float,
        fumador: bool,
        region: str
):
    """
    Validaciones básicas de seguridad
    """
    if edad < 40:
        raise ValueError("SCORE2 aplica solo a >= 40 años")
    if sexo not in ("Hombre", "Mujer", "H", "M"):
        raise ValueError("Sexo inválido")
    if pas <= 0:
        raise ValueError("PAS inválida")
    if no_hdl <= 0:
        raise ValueError("no-HDL inválido")
    if region not in ("MODERADO" ,"Moderado","moderado", "MUY ALTO", "Muy alto", "muy alto"):
        raise ValueError("Región inválida.")

def calcular_score2(
        edad: int,
        sexo: str,
        pas: int,
        no_hdl: float,
        fumador: bool,
        region: str
):
    """
    Funcion principal del motor SCORE2.
    Devuelve:
        -riesgo_10y (float)
        -modelo (str)
        -categoria (str)
    """
    #1- Validar los datos
    validar_inputs(edad,sexo,pas,no_hdl,fumador,region)

    #2- Determinar modelo
    modelo = determinar_modelo(edad)

    #3-Calcular riesgo (PLACEHOLRDER)
    #Aca va el modelo matematico real (proximo paso)
    riesgo_10y = calcular_riesgo_modelo(
        edad,sexo,pas,no_hdl,fumador,region,modelo
    )

    #4- Categorizar
    categoria = categorizar_riesgo(riesgo_10y, modelo)

    return riesgo_10y, modelo, categoria

def calcular_riesgo_modelo(
        edad: int,
        sexo: str,
        pas: int,
        no_hdl: float,
        fumador: bool,
        region: str,
        modelo: str
):
    edad_d = discretizar(edad, EDADES)
    pas_d = discretizar(pas, PAS_CORTES)
    no_hdl_d = discretizar(no_hdl * 38.67, NO_HDL_CORTES) # mmoL/L -> mg/dL

    clave = (sexo, fumador, edad_d, pas_d, no_hdl_d)

    if region.upper()== "MODERADO":
        tabla =SCORE2_MODERADO
    else:
        raise NotImplementedError("Región aún no implementada")

    try:
        return tabla[clave]
    except KeyError:
        raise ValueError(f"No hay dato SCORE2 para {clave}")


if __name__ == "__main__":
    try:
        riesgo, modelo, categoria = calcular_score2(
            edad=45,
            sexo="Hombre",
            pas=120,
            no_hdl=3.0,
            fumador=False,
            region="MODERADO"
        )

        print(f"Riesgo a 10 años: {riesgo}%")
        print(f"Modelo: {modelo}")
        print(f"Categoría: {categoria}")

    except Exception as e:
        print("Error: ", e)

