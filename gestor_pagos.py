import os

def validar_monto():
    while True:
        entrada = input("Ingrese el monto del gasto: ")
        try:
            monto = float(entrada)
            if monto > 0:
                return monto
            else:
                print("Error: El monto debe ser un número positivo.")
        except ValueError:
            print("Error: Entrada no válida. Por favor, ingrese solo números.")

def guardar_gasto(monto, categoria):
    with open("datos_gastos.txt", "a") as archivo:
        archivo.write(f"{monto},{categoria}\n")

def leer_gastos():
    gastos = []
    if os.path.exists("datos_gastos.txt"):
        with open("datos_gastos.txt", "r") as archivo:
            for linea in archivo:
                monto, categoria = linea.strip().split(",")
                gastos.append({"monto": float(monto), "categoria": categoria})
    return gastos

def mostrar_menu():
    while True:
        print("\n--- GESTOR DE GASTOS ---")
        print("1. Agregar gasto")
        print("2. Ver total de gastos")
        print("3. Filtrar por categoría")
        print("4. Salir")
        
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            monto = validar_monto()
            categoria = input("Ingrese la categoría (ej. Comida, Transporte): ").capitalize()
            guardar_gasto(monto, categoria)
            print("¡Gasto guardado con éxito!")

        elif opcion == "2":
            gastos = leer_gastos()
            total = sum(g["monto"] for g in gastos)
            print(f"\nEl gasto total acumulado es: ${total:.2f}")

        elif opcion == "3":
            gastos = leer_gastos()
            cat_buscar = input("¿Qué categoría desea consultar?: ").capitalize()
            filtrados = [g for g in gastos if g["categoria"] == cat_buscar]
            
            if filtrados:
                subtotal = sum(f["monto"] for f in filtrados)
                print(f"\nGastos en '{cat_buscar}':")
                for f in filtrados:
                    print(f"- ${f['monto']:.2f}")
                print(f"Subtotal de la categoría: ${subtotal:.2f}")
            else:
                print(f"No se encontraron gastos en la categoría '{cat_buscar}'.")

        elif opcion == "4":
            print("Saliendo del programa")
            break
        else:
            print("Opción no válida, intente de nuevo.")

if __name__ == "__main__":
    mostrar_menu()