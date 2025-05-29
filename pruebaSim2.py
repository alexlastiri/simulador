import streamlit as st
import pandas as pd
from itertools import product

# Datos base
EQ = 45000  # Costo del equipo

# Información de los paquetes
paquetes = {
    "B": {"PER": 60,  "VG": 90, "MXN": 5520,  "EQ_REQ": True},
    "C": {"PER": 120, "VG": 90, "MXN": 10080, "EQ_REQ": True},
    "D": {"PER": 240, "VG": 90, "MXN": 17760, "EQ_REQ": True},
    "E": {"PER": 240, "VG": 1,  "MXN": 6000,  "EQ_REQ": True},
    "F": {"PER": 240, "VG": 1,  "MXN": 24000, "EQ_REQ": True},
    "G": {"PER": 30,  "VG": 1,  "MXN": 7000,  "EQ_REQ": False},
    "H": {"PER": 60,  "VG": 1,  "MXN": 8400,  "EQ_REQ": False},
    "I": {"PER": 240, "VG": 1,  "MXN": 9500,  "EQ_REQ": False},
}

# Cálculo de capacidad y costo anual de cada paquete
for k, v in paquetes.items():
    usos_anual = 365 / v["VG"]
    paquetes[k]["USOS_ANUAL"] = usos_anual
    paquetes[k]["CAP_ANUAL"] = v["PER"] * usos_anual
    paquetes[k]["COSTO_ANUAL"] = v["MXN"] * usos_anual

MAX_CANT = 5  # límite de combinaciones por paquete

def encontrar_combinacion_optima(FU, CP):
    CP_ANUAL = CP * (365 / FU)

    mejor_combinacion = None
    costo_minimo = float('inf')

    for combo in product(range(MAX_CANT + 1), repeat=len(paquetes)):
        total_cap = 0
        total_cost = 0
        requiere_eq = False

        for count, (k, v) in zip(combo, paquetes.items()):
            total_cap += count * v["CAP_ANUAL"]
            total_cost += count * v["COSTO_ANUAL"]
            if count > 0 and v["EQ_REQ"]:
                requiere_eq = True

        if total_cap >= CP_ANUAL:
            if requiere_eq:
                total_cost += EQ
            if total_cost < costo_minimo:
                costo_minimo = total_cost
                mejor_combinacion = combo

    resultados = {
        k: mejor_combinacion[i] for i, k in enumerate(paquetes.keys())
    }
    resultados["Costo_Total"] = round(costo_minimo, 2)
    resultados["Personas_Anual"] = round(CP_ANUAL)
    resultados["Incluye_Equipo"] = any(
        mejor_combinacion[i] > 0 and v["EQ_REQ"] for i, (k, v) in enumerate(paquetes.items())
    )
    return pd.DataFrame([resultados])

# Streamlit UI
st.title("Simulador de Paquetes de Capacitación")

fu = st.selectbox("Frecuencia de uso (en días)", options=[1, 7, 30, 365], index=2)
cp = st.number_input("Cantidad de personas a capacitar por frecuencia", min_value=1, value=240)

if st.button("Calcular combinación óptima"):
    resultado = encontrar_combinacion_optima(fu, cp)
    st.subheader("Mejor combinación de paquetes")
    st.dataframe(resultado, use_container_width=True)

