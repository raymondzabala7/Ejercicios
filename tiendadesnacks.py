productos = {
    "papas": 2500,
    "gaseosa": 3000,
    "galletas": 1800,
    "chocolate": 2200,
    "jugo": 2800
}

carrito = []

def ver_productos():
    print("\nProductos Disponibles")
    for nombre, precio in productos.items():
        print(f"{nombre.capitalize()} - ${precio}")
    print("")


def agregar_al_carrito():
    producto = input("Ingrese el nombre del producto: ").lower()

    if producto in productos:
        carrito.append(producto)
        print(f"{producto.capitalize()} agregado al carrito ")
    else:
        print("Producto no existe")


def ver_carrito():
    if not carrito:
        print("El carrito está vacío")
        return

    print("\nCarrito de Compras")
    total = 0

    for producto in carrito:
        precio = productos[producto]
        print(f"{producto.capitalize()} - ${precio}")
        total += precio

    print(f"Total a pagar: ${total}")
    print("")


def pagar():
    if not carrito:
        print("No hay productos para pagar")
        return False

    total = 0
    for producto in carrito:
        total += productos[producto]

    print(f"Total a pagar: ${total}")
    confirmacion = input("¿Desea pagar? (s/n): ").lower()

    if confirmacion == "s":
        print("Gracias por su compra!")
        return True
    else:
        print("Pago cancelado")
        return False


while True:
    print("\nTIENDA DE SNACKS")
    print("6. Ver productos disponibles")
    print("7. Agregar producto al carrito")
    print("8. Ver carrito de compras")
    print("9. Pagar y salir")
    print("0. Salir sin comprar")

    opcion = input("Seleccione una opcion: ")

    if opcion == "6":
        ver_productos()
    elif opcion == "7":
        agregar_al_carrito()
    elif opcion == "8":
        ver_carrito()
    elif opcion == "9":
        if pagar():
            break
    elif opcion == "0":
        print("Saliste sin comprar")
        break
    else:
        print("Opcion invalida")