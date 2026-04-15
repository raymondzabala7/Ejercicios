import random
import os
from datetime import datetime

ARCHIVO_PREGUNTAS = "preguntas_quiz.txt"
ARCHIVO_RANKING = "ranking_quiz.txt"

preguntas_base = [
    {"texto": "¿Cuál es el planeta más grande?", "opciones": ["A) Marte", "B) Júpiter", "C) Saturno", "D) Venus"], "respuesta": "B", "categoria": "Ciencia", "dificultad": "facil"},
    {"texto": "¿En qué año llegó Colón a América?", "opciones": ["A) 1492", "B) 1500", "C) 1485", "D) 1510"], "respuesta": "A", "categoria": "Historia", "dificultad": "facil"},
    {"texto": "¿Qué significa CPU?", "opciones": ["A) Central Process Unit", "B) Core Part Unity", "C) Computer Personal Utility", "D) Control Process User"], "respuesta": "A", "categoria": "Tecnología", "dificultad": "media"},
    {"texto": "¿Cuánto es 5! (factorial)?", "opciones": ["A) 60", "B) 100", "C) 120", "D) 150"], "respuesta": "C", "categoria": "Matemáticas", "dificultad": "dificil"}
]

def cargar_preguntas():
    if not os.path.exists(ARCHIVO_PREGUNTAS):
        return preguntas_base
    lista = []
    with open(ARCHIVO_PREGUNTAS, "r", encoding="utf-8") as f:
        for linea in f:
            p = linea.strip().split("|")
            lista.append({
                "texto": p[0], "opciones": p[1].split(";"),
                "respuesta": p[2], "categoria": p[3], "dificultad": p[4]
            })
    return lista

def guardar_preguntas(lista_preguntas):
    with open(ARCHIVO_PREGUNTAS, "w", encoding="utf-8") as f:
        for p in lista_preguntas:
            opciones_str = ";".join(p["opciones"])
            f.write(f"{p['texto']}|{opciones_str}|{p['respuesta']}|{p['categoria']}|{p['dificultad']}\n")

def guardar_ranking(nombre, puntaje):
    fecha = datetime.now().strftime("%Y-%m-%d")
    with open(ARCHIVO_RANKING, "a", encoding="utf-8") as f:
        f.write(f"{nombre}|{puntaje}|{fecha}\n")

def mostrar_ranking():
    if not os.path.exists(ARCHIVO_RANKING):
        print("\nEl ranking está vacío aún.")
        return
    
    records = []
    with open(ARCHIVO_RANKING, "r", encoding="utf-8") as f:
        for linea in f:
            n, p, fe = linea.strip().split("|")
            records.append((n, int(p), fe))

    records_ordenados = sorted(records, key=lambda x: x[1], reverse=True)[:10]
    
    print("\n--- TOP 10 RANKING HISTÓRICO ---")
    print(f"{'POS':<4} {'JUGADOR':<15} {'PUNTOS':<10} {'FECHA'}")
    for i, r in enumerate(records_ordenados, 1):
        print(f"{i:<4} {r[0]:<15} {r[1]:<10} {r[2]}")

# --- Lógica de Juego ---

def calcular_puntos(dificultad, correcta):
    if not correcta: return -5
    puntos = {"facil": 10, "media": 20, "dificil": 30}
    return puntos.get(dificultad, 10)

def calcular_bonus(racha):
    if racha == 3: 
        print("¡BONUS POR RACHA! +15 puntos")
        return 15
    if racha == 5: 
        print("¡SUPER RACHA! +30 puntos")
        return 30
    return 0

def jugar_ronda(jugador, preguntas):
    print(f"\n>>> TURNO DE: {jugador} <<<")
    puntaje = 0
    racha = 0
    
    for p in preguntas:
        print(f"\n[{p['categoria']} - {p['dificultad'].upper()}]")
        print(p["texto"])
        for opcion in p["opciones"]:
            print(opcion)
        
        resp = input("Tu respuesta (A, B, C o D): ").upper().strip()
        
        if resp == p["respuesta"]:
            print("¡Correcto!")
            racha += 1
            puntos_ganados = calcular_puntos(p["dificultad"], True)
            puntaje += puntos_ganados + calcular_bonus(racha)
        else:
            print(f"Incorrecto. La respuesta era {p['respuesta']}")
            racha = 0
            puntaje += calcular_puntos(p["dificultad"], False)
        
        print(f"Puntaje actual: {puntaje}")
    
    return puntaje

def administrar_preguntas():
    lista = cargar_preguntas()
    while True:
        print("\n--- ADMINISTRAR PREGUNTAS ---")
        print("1. Agregar pregunta")
        print("2. Eliminar pregunta")
        print("3. Volver")
        opc = input("Seleccione: ")
        
        if opc == "1":
            texto = input("Texto de la pregunta: ")
            opcs = [f"A) {input('Opción A: ')}", f"B) {input('Opción B: ')}", 
                    f"C) {input('Opción C: ')}", f"D) {input('Opción D: ')}"]
            resp = input("Letra correcta (A/B/C/D): ").upper()
            cat = input("Categoría: ").capitalize()
            dif = input("Dificultad (facil/media/dificil): ").lower()
            lista.append({"texto": texto, "opciones": opcs, "respuesta": resp, "categoria": cat, "dificultad": dif})
            guardar_preguntas(lista)
            print("Pregunta guardada.")
        elif opc == "2":
            for i, p in enumerate(lista): print(f"{i}. {p['texto']}")
            idx = int(input("Número de pregunta a eliminar: "))
            lista.pop(idx)
            guardar_preguntas(lista)
            print("Pregunta eliminada.")
        elif opc == "3": break

def main():
    while True:
        print("\n=== QUIZ MULTIJUGADOR 2.0 ===")
        print("1. Jugar")
        print("2. Ver Ranking")
        print("3. Administrar Preguntas")
        print("4. Salir")
        opc = input("Opción: ")
        
        if opc == "1":
            num_j = int(input("¿Cuántos jugadores (1-4)? "))
            nombres = [input(f"Nombre jugador {i+1}: ") for i in range(num_j)]
            
            preguntas_disponibles = cargar_preguntas()
            cats = list(set([p["categoria"] for p in preguntas_disponibles]))
            print(f"\nCategorías disponibles: {', '.join(cats)} o 'Todas'")
            eleccion = input("Elige una: ").capitalize()
            
            if eleccion != "Todas":
                preguntas_partida = [p for p in preguntas_disponibles if p["categoria"] == eleccion]
            else:
                preguntas_partida = preguntas_disponibles
            
            random.shuffle(preguntas_partida)
            
            resultados_partida = []
            for j in nombres:
                puntos = jugar_ronda(j, preguntas_partida)
                resultados_partida.append((j, puntos))
                guardar_ranking(j, puntos)
            
            print("\n=== RESULTADOS FINALES ===")
            for j, p in sorted(resultados_partida, key=lambda x: x[1], reverse=True):
                print(f"{j}: {p} puntos")

        elif opc == "2": mostrar_ranking()
        elif opc == "3": administrar_preguntas()
        elif opc == "4": break

if __name__ == "__main__":
    main()