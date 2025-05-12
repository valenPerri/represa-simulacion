# Simulación de represa usando el método de Cuadrados Medios de Von Neumann

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
# 2. FUNCIÓN CUADRADOS MEDIOS
# ---------------------------
def generar_aleatorio(semilla):
    cuadrado = str(semilla**2).zfill(8)
    nuevo = int(cuadrado[2:6])  # Extrae las 4 cifras del medio
    r = nuevo / 10000.0
    return nuevo, r

# ---------------------------
# 3. FUNCIÓN PARA TRADUCIR R A INCREMENTO
# ---------------------------
def obtener_incremento(r):
    for valor, fx in distribucion:
        if r < fx:
            return valor
    return 3  # valor extremo por seguridad

# ---------------------------
# 4. FUNCIÓN PRINCIPAL DE SIMULACIÓN
# ---------------------------
def simular_represa(semilla, dias):
    nivel = 0
    alerta_roja = 0
    compuertas = [0, 0, 0, 0]
    historial = []

    for i in range(1, dias + 1):
        semilla, r = generar_aleatorio(semilla)
        incremento = obtener_incremento(r)
        nivel += incremento
        if nivel > MAX_NIVEL:
            nivel = MAX_NIVEL

        # Contar compuertas abiertas
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
semilla_inicial = 5731
alerta, compuertas, historial = simular_represa(semilla_inicial, dias)

# ---------------------------
# 6. IMPRESIÓN DE RESULTADOS
# ---------------------------
print("\n--- RESULTADOS FINALES ---")
print(f"Veces en alerta roja: {alerta}")
print(f"Compuerta 1 (≥15m): {compuertas[0]} veces")
print(f"Compuerta 2 (≥25m): {compuertas[1]} veces")
print(f"Compuerta 3 (≥32m): {compuertas[2]} veces")
print(f"Compuerta 4 (≥40m): {compuertas[3]} veces")

print("\n--- HISTORIAL DE SIMULACIÓN ---")
print("Día | Aleatorio | Incremento | Nivel del Lago")
for dia, r, inc, nivel in historial:
    print(f"{dia:3d} | {r:.4f}     | {inc:>+3d}        | {nivel:.2f}")
