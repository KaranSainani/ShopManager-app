# ShopManger app
# Developed in Python Version: 3.11.5
# author: © Karan Sainani

# Importamos librería para trabajar con Base de datos SQLite
import sqlite3

# Función para obtener datos de la BD
def obtener_inventario():
    # Abre el archivo de base de datos
    conexion = sqlite3.connect("ShopManager.db")

    # Para devolver de forma que pueda acceder a los datos por su nombre
    conexion.row_factory = sqlite3.Row

    # El operario, que va entrar en la BD a buscar lo que le pida,
    # la conexión es el cable, el cursor es quien camina por él. 
    cursor = conexion.cursor()

    # Traemos los datos que queremos tratar
    cursor.execute("SELECT id, Name, Quantity, Category, Price FROM Producto")

    # Convertimos cada fila en un diccionario y el cursor trae todas las filas que encontró
    productos = [dict(fila) for fila in cursor.fetchall()]

    # Corta la conexión con el archivo de BD, porque si dejas las conexiones abiertas el archivo de BD podría bloquearse o corromperse
    conexion.close()

    # Entrega de resultados
    return productos

# --- Probando la salida ---
"""inventario = obtener_inventario()

for p in inventario:
    # Ahora accedes directamente por el nombre de la columna en la DB
    print(f"Producto: {p['Name']} | Stock disponible: {p['Quantity']}")"""



# Función para actualizar el stock del producto en la BD
def actualizar_stock_producto(id_producto):
    conexion = sqlite3.connect("ShopManager.db")
    cursor = conexion.cursor()
    
    # Descuenta una unidad de stock al producto específico (por ID) 
    # solo si todavía quedan unidades disponibles (> 0), evitando stocks negativos.

    # el ? se pone porque actua como un filtro de seguridad, le dice que solo aplique el descuento al producto cuyo ID coincida con el que le paso
    cursor.execute("""
        UPDATE Producto 
        SET Quantity = Quantity - 1 
        WHERE id = ? AND Quantity > 0
    """, (id_producto,))
    
    conexion.commit()   # Sin commit no se guardan los cambios
    conexion.close()