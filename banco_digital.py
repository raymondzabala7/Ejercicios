import os
from datetime import datetime

ARCHIVO_CUENTAS = "cuentas_banco.txt"
cuentas = {} 
def cargar_datos():
    """Carga los datos del archivo TXT al diccionario del programa."""
    global cuentas
    if not os.path.exists(ARCHIVO_CUENTAS):
        return
    
    try:
        with open(ARCHIVO_CUENTAS, "r") as f:
            for linea in f:
                partes = linea.strip().split("|")
                if len(partes) < 4: continue
                
                num_cta = int(partes[0])
                historial_lista = partes[4].split(";") if len(partes) > 4 and partes[4] else []
                
                cuentas[num_cta] = {
                    "nombre": partes[1],
                    "pin": partes[2],
                    "saldo": float(partes[3]),
                    "historial": historial_lista
                }
    except Exception as e:
        print(f"Error al cargar datos: {e}")

def guardar_datos():
    try:
        with open(ARCHIVO_CUENTAS, "w") as f:
            for num, datos in cuentas.items():
                historial_str = ";".join(datos["historial"])
                linea = f"{num}|{datos['nombre']}|{datos['pin']}|{datos['saldo']}|{historial_str}\n"
                f.write(linea)
    except Exception as e:
        print(f"Error al guardar datos: {e}")

def registrar_movimiento(num_cta, tipo, monto, saldo_res):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    movimiento = f"[{fecha}] {tipo}: ${monto:.2f} | Saldo: ${saldo_res:.2f}"
    cuentas[num_cta]["historial"].append(movimiento)

def crear_cuenta():
    print("\n--- Apertura de Cuenta CampusBank ---")
    nombre = input("Ingrese su nombre completo: ").strip().title()
    
    while True:
        pin = input("Cree un PIN de 4 dígitos: ")
        if pin.isdigit() and len(pin) == 4:
            break
        print("Error: El PIN debe ser numérico y de 4 dígitos.")
    
    nuevo_num = 1001 + len(cuentas)
    cuentas[nuevo_num] = {
        "nombre": nombre,
        "pin": pin,
        "saldo": 0.0,
        "historial": []
    }
    
    registrar_movimiento(nuevo_num, "Apertura de cuenta", 0, 0)
    guardar_datos()
    print(f"\nCuenta creada con éxito.")
    print(f"Su número de cuenta es: {nuevo_num}")
    print("No olvide su PIN.")

def iniciar_sesion():
    print("\n--- Inicio de Sesión ---")
    try:
        num_cta = int(input("Número de cuenta: "))
        if num_cta not in cuentas:
            print("Error: La cuenta no existe.")
            return None
        
        intentos = 3
        while intentos > 0:
            pin = input(f"Ingrese su PIN ({intentos} intentos restantes): ")
            if cuentas[num_cta]["pin"] == pin:
                print(f"\nBienvenido(a), {cuentas[num_cta]['nombre']}.")
                return num_cta
            else:
                intentos -= 1
                print("PIN incorrecto.")
        
        print("Demasiados intentos fallidos.")
        return None
    except ValueError:
        print("Error: Entrada no válida.")
        return None

def depositar(num_cta):
    try:
        monto = float(input("Monto a depositar: $"))
        if monto <= 0:
            print("Error: El monto debe ser positivo.")
            return
        
        cuentas[num_cta]["saldo"] += monto
        registrar_movimiento(num_cta, "Depósito", monto, cuentas[num_cta]["saldo"])
        guardar_datos()
        print(f"Depósito exitoso. Nuevo saldo: ${cuentas[num_cta]['saldo']:.2f}")
    except ValueError:
        print("Error: Ingrese un número válido.")

def retirar(num_cta):
    try:
        monto = float(input("Monto a retirar: $"))
        if monto <= 0:
            print("Error: El monto debe ser positivo.")
            return
        
        if monto > cuentas[num_cta]["saldo"]:
            print(f"Fondos insuficientes. Saldo disponible: ${cuentas[num_cta]['saldo']:.2f}")
        else:
            cuentas[num_cta]["saldo"] -= monto
            registrar_movimiento(num_cta, "Retiro", monto, cuentas[num_cta]["saldo"])
            guardar_datos()
            print(f"Retiro exitoso. Nuevo saldo: ${cuentas[num_cta]['saldo']:.2f}")
    except ValueError:
        print("Error: Ingrese un número válido.")

def transferir(origen):
    try:
        destino = int(input("Ingrese número de cuenta destino: "))
        if destino not in cuentas:
            print("Error: La cuenta destino no existe.")
            return
        if destino == origen:
            print("Error: No puede transferirse a sí mismo.")
            return
            
        monto = float(input(f"Monto a transferir a {cuentas[destino]['nombre']}: $"))
        if monto <= 0:
            print("Error: El monto debe ser positivo.")
            return
            
        if monto > cuentas[origen]["saldo"]:
            print(f"Saldo insuficiente. Tiene: ${cuentas[origen]['saldo']:.2f}")
        else:
            cuentas[origen]["saldo"] -= monto
            cuentas[destino]["saldo"] += monto
            
            registrar_movimiento(origen, f"Transferencia enviada a #{destino}", monto, cuentas[origen]["saldo"])
            registrar_movimiento(destino, f"Transferencia recibida de #{origen}", monto, cuentas[destino]["saldo"])
            
            guardar_datos()
            print("¡Transferencia realizada con éxito!")
    except ValueError:
        print("Error: Datos inválidos.")

def ver_historial(num_cta):
    print(f"\n--- Historial de Movimientos (Cuenta {num_cta}) ---")
    for mov in cuentas[num_cta]["historial"]:
        print(mov)
    print(f"Saldo Actual: ${cuentas[num_cta]['saldo']:.2f}")

def menu_usuario(num_cta):
    while True:
        print(f"\n--- CampusBank (Cuenta: {num_cta}) ---")
        print("4. Consultar saldo")
        print("5. Depositar dinero")
        print("6. Retirar dinero")
        print("7. Transferir")
        print("8. Ver historial")
        print("9. Cerrar sesión")
        
        opc = input("Seleccione una opción: ")
        
        if opc == "4":
            print(f"\nSaldo actual: ${cuentas[num_cta]['saldo']:.2f}")
        elif opc == "5": depositar(num_cta)
        elif opc == "6": retirar(num_cta)
        elif opc == "7": transferir(num_cta)
        elif opc == "8": ver_historial(num_cta)
        elif opc == "9": 
            print("Sesión cerrada.")
            break
        else:
            print("Opción no válida.")

def menu_principal():
    cargar_datos()
    while True:
        print("\n=== BIENVENIDO A CAMPUSBANK ===")
        print("1. Crear cuenta nueva")
        print("2. Iniciar sesión")
        print("3. Salir del sistema")
        
        opc = input("Seleccione una opción: ")
        
        if opc == "1":
            crear_cuenta()
        elif opc == "2":
            cuenta_activa = iniciar_sesion()
            if cuenta_activa:
                menu_usuario(cuenta_activa)
        elif opc == "3":
            print("Gracias por usar CampusBank. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu_principal()