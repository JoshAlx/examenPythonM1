import unittest
from unittest.mock import patch
import random
from io import StringIO
from comics_store import Producto, TiendaComics

class TestTiendaComics(unittest.TestCase):
    
    def setUp(self):
        self.tienda = TiendaComics()

    def test_registrar_producto(self):
        # Definir datos de prueba para un producto
        datos_producto = {
            "nombre": "Spider-Man",
            "precio": 10.0,
            "ubicacion": "A",
            "descripcion": "Figura de acción",
            "casa": "Marvel",
            "referencia": "SPD123",
            "pais_origen": "Estados Unidos",
            "unidades_compradas": 20,
            "garantia_extendida": True
        }

        # Crear instancia de Producto con los datos de prueba
        producto_prueba = Producto(**datos_producto)

        # Asegurar que el producto se registra exitosamente
        self.tienda.registrar_producto(producto_prueba)
        print(f"Producto registrado: {producto_prueba}")

        # Verificar que el producto se encuentre en el inventario
        self.assertIn(producto_prueba, self.tienda.inventario[datos_producto["ubicacion"].upper()])
        print(f"Inventario después de registrar producto en ubicación {datos_producto['ubicacion'].upper()}: {self.tienda.inventario[datos_producto['ubicacion'].upper()]}")

    def test_no_repetir_producto_mismo_nombre(self):
        # Definir datos de prueba para dos productos con el mismo nombre
        datos_producto1 = {
            "nombre": "Batman",
            "precio": 15.0,
            "ubicacion": "B",
            "descripcion": "Figura de colección",
            "casa": "DC",
            "referencia": "BAT789",
            "pais_origen": "Estados Unidos",
            "unidades_compradas": 25,
            "garantia_extendida": False
        }
        datos_producto2 = {
            "nombre": "Batman",
            "precio": 20.0,
            "ubicacion": "B",
            "descripcion": "Figura de colección",
            "casa": "DC",
            "referencia": "BAT890",
            "pais_origen": "Estados Unidos",
            "unidades_compradas": 30,
            "garantia_extendida": True
        }

        # Crear instancias de Producto con los datos de prueba
        producto_prueba1 = Producto(**datos_producto1)
        producto_prueba2 = Producto(**datos_producto2)

        # Registrar los dos productos con el mismo nombre
        self.tienda.registrar_producto(producto_prueba1)
        self.tienda.registrar_producto(producto_prueba2)

        # Verificar que solo se haya registrado un producto
        self.assertEqual(len(self.tienda.inventario[datos_producto1["ubicacion"].upper()]), 1)
        print(f"Inventario después de registrar productos en ubicación {datos_producto1['ubicacion'].upper()}: {self.tienda.inventario[datos_producto1['ubicacion'].upper()]}")

    def test_mostrar_productos_bodega(self):
        # Definir datos de prueba para un producto
        datos_producto = {
            "nombre": "Spider-Man",
            "precio": 10.0,
            "ubicacion": "A",
            "descripcion": "Figura de acción",
            "casa": "Marvel",
            "referencia": "SPD123",
            "pais_origen": "Estados Unidos",
            "unidades_compradas": 20,
            "garantia_extendida": True
        }

        # Crear instancia de Producto con los datos de prueba
        producto_prueba = Producto(**datos_producto)

        # Registrar el producto en la tienda
        self.tienda.registrar_producto(producto_prueba)

        # Redirigir la salida estándar para capturar la impresión
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.tienda.mostrar_productos_bodega()
            printed_output = fake_out.getvalue()

        # Verificar que el producto se muestra correctamente
        self.assertIn("Ubicación A:", printed_output)
        self.assertIn("ID: ", printed_output)
        self.assertIn("Nombre: Spider-Man", printed_output)
        self.assertIn("Unidades libres en ubicación A: 30", printed_output)
        print("Productos en bodega mostrados:")
        print(printed_output)

    def test_buscar_producto_por_nombre(self):
        # Definir datos de prueba para un producto
        datos_producto = {
            "nombre": "Spider-Man",
            "precio": 10.0,
            "ubicacion": "A",
            "descripcion": "Figura de acción",
            "casa": "Marvel",
            "referencia": "SPD123",
            "pais_origen": "Estados Unidos",
            "unidades_compradas": 20,
            "garantia_extendida": True
        }

        # Crear instancia de Producto con los datos de prueba
        producto_prueba = Producto(**datos_producto)

        # Registrar el producto en la tienda
        self.tienda.registrar_producto(producto_prueba)

        # Realizar la búsqueda del producto por nombre
        producto_encontrado = self.tienda.buscar_producto_por_nombre("Spider-Man")

        # Verificar que el producto se encuentre correctamente
        self.assertIsNotNone(producto_encontrado)
        self.assertEqual(producto_encontrado.nombre, "Spider-Man")
        print(f"Producto encontrado: {producto_encontrado}")

    def test_modificar_unidades_compradas(self):
        # Definir datos de prueba para un producto
        datos_producto = {
            "nombre": "Spider-Man",
            "precio": 10.0,
            "ubicacion": "A",
            "descripcion": "Figura de acción",
            "casa": "Marvel",
            "referencia": "SPD123",
            "pais_origen": "Estados Unidos",
            "unidades_compradas": 20,
            "garantia_extendida": True
        }

        # Crear instancia de Producto con los datos de prueba
        producto_prueba = Producto(**datos_producto)

        # Registrar el producto en la tienda
        self.tienda.registrar_producto(producto_prueba)

        # Modificar las unidades compradas del producto
        self.tienda.modificar_unidades_compradas("Spider-Man", 30)

        # Verificar que las unidades se hayan modificado correctamente
        producto_modificado = self.tienda.buscar_producto_por_nombre("Spider-Man")
        self.assertIsNotNone(producto_modificado)
        self.assertEqual(producto_modificado.unidades_compradas, 20)
        print(f"Producto modificado: {producto_modificado}")

    def test_eliminar_producto(self):
        # Definir datos de prueba para un producto
        datos_producto = {
            "nombre": "Spider-Man",
            "precio": 10.0,
            "ubicacion": "A",
            "descripcion": "Figura de acción",
            "casa": "Marvel",
            "referencia": "SPD123",
            "pais_origen": "Estados Unidos",
            "unidades_compradas": 20,
            "garantia_extendida": True
        }

        # Crear instancia de Producto con los datos de prueba
        producto_prueba = Producto(**datos_producto)

        # Registrar el producto en la tienda
        self.tienda.registrar_producto(producto_prueba)

        # Eliminar el producto de la tienda
        self.tienda.eliminar_producto("Spider-Man")

        # Verificar que el producto se haya eliminado correctamente
        producto_eliminado = self.tienda.buscar_producto_por_nombre("Spider-Man")
        self.assertIsNone(producto_eliminado)
        print("Producto eliminado correctamente.")

if __name__ == '__main__':
    unittest.main()