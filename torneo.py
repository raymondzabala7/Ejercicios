import random
import getpass  

jugadores = []  
estadisticas = {}  
historial = []  

def registrar_jugadores():
    global jugadores, estadisticas
    jugadores = []
    estadisticas = {}
    
    print("\n--- Registro de Jugadores (Mínimo 4, Máximo 8) ---")
    while len(jugadores) < 8:
        nombre = input(f"Ingrese nombre del jugador {len(jugadores)+1} (o 'fin' para terminar): ").strip().capitalize()
        
        if nombre.lower() == 'fin':
            if len(jugadores) >= 4: break
            else: print("Error: Necesitas al menos 4 jugadores.")
            continue
            
        if nombre in jugadores:
            print("Error: Este nombre ya existe.")
        elif nombre == "":
            print("Error: El nombre no puede estar vacío.")
        else:
            jugadores.append(nombre)
            estadisticas[nombre] = {"piedra": 0, "papel": 0, "tijera": 0, "victorias": 0, "eliminado": "Activo"}
            
    print(f"Registro completado: {', '.join(jugadores)}")

def determinar_ganador(e1, e2):
    if e1 == e2: return 0  
    if (e1 == "piedra" and e2 == "tijera") or \
       (e1 == "papel" and e2 == "piedra") or \
       (e1 == "tijera" and e2 == "papel"):
        return 1  
    return 2  

def pedir_eleccion(nombre):
    while True:
        eleccion = input(f"{nombre}, elige (piedra/papel/tijera): ").lower().strip()
        if eleccion in ["piedra", "papel", "tijera"]:
            estadisticas[nombre][eleccion] += 1
            return eleccion
        print("Opción no válida. Intenta de nuevo.")

def jugar_enfrentamiento(j1, j2, ronda_nombre):
    print(f"\n--- {j1} VS {j2} ---")
    victorias_j1 = 0
    victorias_j2 = 0
    
    while victorias_j1 < 2 and victorias_j2 < 2:
        print(f"Marcador: {j1} {victorias_j1} - {victorias_j2} {j2}")
        e1 = pedir_eleccion(j1)
        e2 = pedir_eleccion(j2)
        
        resultado = determinar_ganador(e1, e2)
        if resultado == 1:
            print(f"¡Ronda para {j1}!")
            victorias_j1 += 1
        elif resultado == 2:
            print(f"¡Ronda para {j2}!")
            victorias_j2 += 1
        else:
            print("¡Empate en esta ronda!")
            
    ganador = j1 if victorias_j1 == 2 else j2
    perdedor = j2 if ganador == j1 else j1
    
    estadisticas[ganador]["victorias"] += 1
    estadisticas[perdedor]["eliminado"] = ronda_nombre
    historial.append([ronda_nombre, f"{j1} vs {j2}", f"Ganador: {ganador}"])
    
    print(f"*** {ganador} avanza a la siguiente ronda ***")
    return ganador

def iniciar_torneo():
    if len(jugadores) < 4:
        print("Error: Registra al menos 4 jugadores primero.")
        return

    competidores_actuales = jugadores[:]
    random.shuffle(competidores_actuales)
    ronda_num = 1

    while len(competidores_actuales) > 1:
        ronda_nombre = f"Ronda {ronda_num}"
        if len(competidores_actuales) == 2: ronda_nombre = "Final"
        
        print(f"\n=== {ronda_nombre.upper()} ===")
        ganadores_ronda = []
        
        # Si es impar, uno pasa directo
        if len(competidores_actuales) % 2 != 0:
            suertudo = competidores_actuales.pop()
            print(f"{suertudo} pasa automáticamente por ser número impar.")
            ganadores_ronda.append(suertudo)
            
        for i in range(0, len(competidores_actuales), 2):
            ganador = jugar_enfrentamiento(competidores_actuales[i], competidores_actuales[i+1], ronda_nombre)
            ganadores_ronda.append(ganador)
            
        competidores_actuales = ganadores_ronda
        ronda_num += 1

    campeon = competidores_actuales[0]
    estadisticas[campeon]["eliminado"] = "¡CAMPEON!"
    print(f"\n EL CAMPEÓN DEL TORNEO ES: {campeon} ")

def ver_historial():
    if not historial:
        print("\nNo hay enfrentamientos registrados.")
        return
    print("\n--- HISTORIAL DE ENFRENTAMIENTOS ---")
    print(f"{'RONDA':<10} | {'ENFRENTAMIENTO':<25} | {'RESULTADO'}")
    for h in historial:
        print(f"{h[0]:<10} | {h[1]:<25} | {h[2]}")

def ver_estadisticas():
    if not estadisticas:
        print("\nNo hay estadísticas disponibles.")
        return
    print("\n--- ESTADÍSTICAS DE JUGADORES ---")
    for nombre, datos in estadisticas.items():
        total_elecciones = datos["piedra"] + datos["papel"] + datos["tijera"]
        win_rate = (datos["victorias"] / (total_elecciones/2)) * 100 if total_elecciones > 0 else 0
        
        print(f"\nJugador: {nombre} ({datos['eliminado']})")
        print(f"- Piedra: {datos['piedra']} | Papel: {datos['papel']} | Tijera: {datos['tijera']}")
        print(f"- Victorias en partidas: {datos['victorias']}")

def menu():
    while True:
        print("\n--- TORNEO PIEDRA, PAPEL O TIJERA ---")
        print("1. Registrar jugadores")
        print("2. Iniciar torneo")
        print("3. Ver historial")
        print("4. Ver estadísticas")
        print("5. Salir")
        
        opc = input("Seleccione una opción: ")
        
        if opc == "1": registrar_jugadores()
        elif opc == "2": iniciar_torneo()
        elif opc == "3": ver_historial()
        elif opc == "4": ver_estadisticas()
        elif opc == "5": break
        else: print("Opción inválida.")

if __name__ == "__main__":
    menu()