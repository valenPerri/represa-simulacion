# Simulación de represa usando el método MULTIPLICATIVO de congruencias

# ---------------------------
# 1. PARÁMETROS DEL MODELO
# ---------------------------
MAX_NIVEL = 52           # Altura máxima física de la represa
ALERTA_ROJA = 45         # Nivel a partir del cual hay alerta
COMP_P1 = 15             # Compuerta 1 se abre a los 15m
COMP_P2 = 25             # Compuerta 2 a los 25m
COMP_P3 = 32             # Compuerta 3 a los 32m
COMP_P4 = 40             # Compuerta 4 a los 40m

# Tabla de distribución acumulada
distribucion = [
    (-3, 0.037),
    (-2, 0.250),
    (-1, 0.436),
    ( 0, 0.564),
    ( 1, 0.749),
    ( 2, 0.962),
    ( 3, 1.000)
]

# ---------------------------
# 2. FUNCIÓN GENERADOR MULTIPLICATIVO
# ---------------------------
def generar_aleatorio_multiplicativo(x_anterior, a, m):
    x_nuevo = (a * x_anterior) % m
    r = x_nuevo / m
    return x_nuevo, r

# ---------------------------
# 3. FUNCIÓN PARA TRADUCIR R A INCREMENTO
# ---------------------------
def obtener_incremento(r):
    for valor, fx in distribucion:
        if r < fx:
            return valor
    return 3

# ---------------------------
# 4. FUNCIÓN PRINCIPAL DE SIMULACIÓN
# ---------------------------
def simular_represa_congruencial(x0, dias, a=17, m=1000):
    nivel = 0
    alerta_roja = 0
    compuertas = [0, 0, 0, 0]
    historial = []

    x = x0
    for i in range(1, dias + 1):
        x, r = generar_aleatorio_multiplicativo(x, a, m)
        incremento = obtener_incremento(r)
        nivel += incremento
        if nivel > MAX_NIVEL:
            nivel = MAX_NIVEL

        # Compuertas y alertas
        if nivel >= COMP_P1:
            compuertas[0] += 1
        if nivel >= COMP_P2:
            compuertas[1] += 1
        if nivel >= COMP_P3:
            compuertas[2] += 1
        if nivel >= COMP_P4:
            compuertas[3] += 1
        if nivel > ALERTA_ROJA:
            alerta_roja += 1

        historial.append((i, r, incremento, nivel))

    return alerta_roja, compuertas, historial

# ---------------------------
# 5. EJECUCIÓN DEL MODELO
# ---------------------------
dias = 100
x0 = 573  # semilla inicial (debe ser mayor que 0)
alerta, compuertas, historial = simular_represa_congruencial(x0, dias)

# ---------------------------
# 6. IMPRESIÓN DE RESULTADOS
# ---------------------------
print("\n--- RESULTADOS FINALES (Congruencias Multiplicativas) ---")
print(f"Veces en alerta roja: {alerta}")
print(f"Compuerta 1 (≥15m): {compuertas[0]} veces")
print(f"Compuerta 2 (≥25m): {compuertas[1]} veces")
print(f"Compuerta 3 (≥32m): {compuertas[2]} veces")
print(f"Compuerta 4 (≥40m): {compuertas[3]} veces")

print("\n--- HISTORIAL DE SIMULACIÓN ---")
print("Día | Aleatorio | Incremento | Nivel del Lago")
for dia, r, inc, nivel in historial:
    print(f"{dia:3d} | {r:.4f}     | {inc:>+3d}        | {nivel:.2f}")
