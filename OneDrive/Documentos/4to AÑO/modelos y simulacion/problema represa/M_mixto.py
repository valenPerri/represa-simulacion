# --- Parámetros generales ---
MAX_NIVEL = 52
ALERTA_ROJA = 45
COMP_P1, COMP_P2, COMP_P3, COMP_P4 = 15, 25, 32, 40

# --- Distribución acumulada ---
distribucion = [
    (-3, 0.037), (-2, 0.250), (-1, 0.436), (0, 0.564),
    (1, 0.749), (2, 0.962), (3, 1.000)
]

def obtener_incremento(r):
    for valor, fx in distribucion:
        if r < fx:
            return valor
    return 3

def simular_mixto(x0, dias, a=17, c=43, m=1000):
    nivel = 0
    alerta_roja = 0
    compuertas = [0, 0, 0, 0]
    historial = []

    x = x0
    for i in range(1, dias + 1):
        x = (a * x + c) % m
        r = x / m
        incremento = obtener_incremento(r)
        nivel += incremento
        if nivel > MAX_NIVEL:
            nivel = MAX_NIVEL

        if nivel >= COMP_P1: compuertas[0] += 1
        if nivel >= COMP_P2: compuertas[1] += 1
        if nivel >= COMP_P3: compuertas[2] += 1
        if nivel >= COMP_P4: compuertas[3] += 1
        if nivel > ALERTA_ROJA: alerta_roja += 1

        historial.append((i, round(r, 4), incremento, round(nivel, 2)))

    return alerta_roja, compuertas, historial

# --- Ejecutar ---
alerta, comp, hist = simular_mixto(789, dias=100)

# --- Imprimir resultados ---
print("\n--- MÉTODO MIXTO DE CONGRUENCIAS ---")
print(f"Veces en alerta roja: {alerta}")
print(f"Compuerta 1 (≥15m): {comp[0]} veces")
print(f"Compuerta 2 (≥25m): {comp[1]} veces")
print(f"Compuerta 3 (≥32m): {comp[2]} veces")
print(f"Compuerta 4 (≥40m): {comp[3]} veces")

print("\nDía | Aleatorio | Incremento | Nivel del Lago")
for dia, r, inc, nivel in hist:
    print(f"{dia:3d} | {r:.4f}     | {inc:+3d}        | {nivel:.2f}")
