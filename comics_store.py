import random

class Producto:
    def __init__(self, nombre, precio, ubicacion, descripcion, casa, referencia, pais_origen, unidades_compradas, garantia_extendida):
        self.id = random.randint(1, 100)  # Generar un ID aleatorio de 1 a 100
        self.nombre = nombre
        self.precio = precio
        self.ubicacion = ubicacion
        self.descripcion = descripcion
        self.casa = casa
        self.referencia = referencia
        self.pais_origen = pais_origen
        self.unidades_compradas = unidades_compradas
        self.garantia_extendida = garantia_extendida

    def __str__(self):
        return f"ID: {self.id}, Nombre: {self.nombre}, Precio: {self.precio}, Ubicación: {self.ubicacion}, Descripción: {self.descripcion}, Casa: {self.casa}, Referencia: {self.referencia}, País de origen: {self.pais_origen}, Unidades compradas: {self.unidades_compradas}, Garantía extendida: {self.garantia_extendida}"

class TiendaComics:
    
    def __init__(self):
        self.inventario = {'A': [], 'B': [], 'C': [], 'D': []}

    def registrar_producto(self, producto):
        ubicacion = producto.ubicacion.upper()

        # Verifico si la ubicación está llena
        if len(self.inventario[ubicacion]) >= 50:
            print("La ubicación está llena.")
            return

        # Verificar si el producto ya está en la ubicación
        for prod in self.inventario[ubicacion]:
            if prod.nombre == producto.nombre:
                pass
                return

        # Si la ubicación seleccionada no está llena y el producto no está en la ubicación, agregar el producto
        self.inventario[ubicacion].append(producto)
        print("Producto registrado exitosamente.")

        # Verificar si tengo espacio suficiente para ceder las unidades excedentes a la siguiente ubicación
        unidades_totales = sum(p.unidades_compradas for p in self.inventario[ubicacion])
        if unidades_totales > 50:
            unidades_excedentes = unidades_totales - 50
            siguiente_ubicacion = chr(ord(ubicacion) + 1)
            if siguiente_ubicacion <= 'D':
                producto_siguiente = Producto(producto.nombre, producto.precio, siguiente_ubicacion, producto.descripcion, producto.casa, producto.referencia, producto.pais_origen, unidades_excedentes, producto.garantia_extendida)
                self.registrar_producto(producto_siguiente)

    def mostrar_productos_bodega(self):
        for ubicacion, productos in self.inventario.items():
            print(f"Ubicación {ubicacion}:")
            unidades_totales = sum(producto.unidades_compradas for producto in productos)
            if unidades_totales > 50:
                print(f"Unidades excedentes en la ubicación {ubicacion}: {unidades_totales - 50}")
                # Ceder unidades excedentes a la siguiente ubicación
                siguiente_ubicacion = chr(ord(ubicacion) + 1)
                if siguiente_ubicacion > 'D':
                    print("No hay más ubicaciones disponibles para almacenar las unidades excedentes.")
                else:
                    print(f"Las unidades excedentes serán transferidas a la ubicación {siguiente_ubicacion}.")
                    unidades_excedentes = unidades_totales - 50
                    for producto in reversed(productos):  # Iterar en reversa para comenzar desde el último producto registrado
                        if unidades_excedentes > 0:
                            unidades_a_transferir = min(unidades_excedentes, producto.unidades_compradas)
                            producto.unidades_compradas -= unidades_a_transferir
                            unidades_excedentes -= unidades_a_transferir
                            producto_siguiente = Producto(producto.nombre, producto.precio, siguiente_ubicacion, producto.descripcion, producto.casa, producto.referencia, producto.pais_origen, unidades_a_transferir, producto.garantia_extendida)
                            self.registrar_producto(producto_siguiente)
                            if unidades_excedentes == 0:
                                break
            for producto in productos:
                print(producto)
            unidades_libres = max(0, 50 - sum(producto.unidades_compradas for producto in productos))
            print(f"Unidades libres en ubicación {ubicacion}: {unidades_libres}\n")

    def buscar_producto_por_nombre(self, nombre):
        for ubicacion, productos in self.inventario.items():
            for producto in productos:
                if producto.nombre.lower() == nombre.lower():
                    return producto
        return None

    def mostrar_info_producto(self, nombre):
        producto = self.buscar_producto_por_nombre(nombre)
        if producto:
            print(producto)
        else:
            print("Producto no encontrado.")

    def modificar_unidades_compradas(self, nombre, nuevas_unidades):
        producto = self.buscar_producto_por_nombre(nombre)
        if producto:
            if nuevas_unidades <= producto.unidades_compradas:
                producto.unidades_compradas = nuevas_unidades
                print("Unidades modificadas exitosamente.")
            else:
                print("No puedes aumentar el número de unidades compradas.")
        else:
            print("Producto no encontrado.")

    def eliminar_producto(self, nombre):
        producto = self.buscar_producto_por_nombre(nombre)
        if producto:
            confirmacion = input("¿Estás seguro de que deseas eliminar este producto? (s/n): ")
            if confirmacion.lower() == 's':
                ubicacion = producto.ubicacion.upper()
                self.inventario[ubicacion].remove(producto)
                print("Producto eliminado exitosamente.")
        else:
            print("Producto no encontrado.")

# Función para mostrar el menú y manejar las opciones
def mostrar_menu():
    print("\nMenú:")
    print("1. Registrar un producto")
    print("2. Mostrar productos en bodega")
    print("3. Buscar producto por nombre")
    print("4. Modificar unidades compradas de un producto")
    print("5. Eliminar un producto")
    print("6. Salir")

# Función principal
def main():
    tienda = TiendaComics()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            nombre = input("Nombre del producto: ")
            precio = float(input("Precio unitario del producto: "))
            ubicacion = input("Ubicación en la tienda (A, B, C o D): ")
            descripcion = input("Descripción del producto: ")
            casa = input("Casa a la que pertenece el producto: ")
            referencia = input("Referencia del producto: ")
            pais_origen = input("País de origen del producto: ")
            unidades_compradas = int(input("Número de unidades compradas del producto: "))
            garantia_extendida = input("Producto con garantía extendida (true/false): ").lower() == 'true'

            producto = Producto(nombre, precio, ubicacion, descripcion, casa, referencia, pais_origen, unidades_compradas, garantia_extendida)
            tienda.registrar_producto(producto)

        elif opcion == '2':
            tienda.mostrar_productos_bodega()

        elif opcion == '3':
            nombre = input("Ingrese el nombre del producto: ")
            tienda.mostrar_info_producto(nombre)

        elif opcion == '4':
            nombre = input("Ingrese el nombre del producto: ")
            nuevas_unidades = int(input("Ingrese el nuevo número de unidades compradas: "))
            tienda.modificar_unidades_compradas(nombre, nuevas_unidades)

        elif opcion == '5':
            nombre = input("Ingrese el nombre del producto que desea eliminar: ")
            tienda.eliminar_producto(nombre)

        elif opcion == '6':
            print("¡Hasta luego!")
            break

        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()