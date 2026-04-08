# ShopManger app
# Developed in Python Version: 3.11.5
# author: © Karan Sainani

# ==============================
# Librerías necesarias
# ==============================
# Para generar identificadores únicos universales (UUID)
import uuid

# La necesitamos para medir, registrar o manipular tiempo en el programa (hora, fecha, etc)
from datetime import datetime

# Para la GUI (Graphical User Interface)
from tkinter import *
from tkinter import messagebox

# Trabajar con PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.colors import black
from reportlab.lib.styles import getSampleStyleSheet

# ==================================================
# Ficheros separados, virtualShop.py y database.py
# ==================================================
# Traemos las funciones necesarias para que la GUI pueda sacar información de
# la base de datos y guardar los cambios.
from database import obtener_inventario, actualizar_stock_producto

# ==============================
# Clase Producto
# ==============================
class Producto:

    # Constructor, definimos el objeto Producto con todos sus atributos
    def __init__(self, id, nombre, cantidad, categoria, precio):
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.categoria = categoria
        self.precio = precio

# ==============================
# Clase Carrito
# ==============================
class Carrito:

    # Constructor de Carrito
    def __init__(self):
        # Creamos una lista vacía donde se irán guardando los productos que elija el cliente
        self.items = []

    # Agregar elementos al carrito
    def agregar(self, producto):
        self.items.append(producto) # .append() -> Añadimos al final 

    # Eliminar elementos del carrito
    def eliminar(self, index):
        # Comprobamos que el producto elegido realmente existe en el carrito antes de intentar borrarlo
        if 0 <= index < len(self.items):
            self.items.pop(index) # .pop() -> Borra ese elemento


    # Para obtener el total de la compra en el carrito
    def total(self):
        # Contador para ir acumulando cada elemento comprado
        resultado_total = 0
    
        # Recorremos la lista de ítems
        for p in self.items:
            # Sumamos el precio de cada producto al acumulador
            resultado_total = resultado_total + p.precio
        
        # Devolvemos el resultado final
        return resultado_total

    # Otra forma más óptima - OK DEJAR 08/04/26
    """def total(self):
        return sum(p.precio for p in self.items)"""


# Creamos el carrito
carrito = Carrito()


# Función para contar cantidades y guardar precios de los productos. Evitamos código repetido
def agrupar_productos(items_del_carrito):
    
    conteo = {}         # Diccionario de conteo
    precios = {}        # Diccionario de precios
    
    for p in items_del_carrito:
        # Contamos cuántas unidades hay de cada producto. Obtenemos el valor, si NO existe, devuelvo 0 y le suma 1. SI existe (y tiene 1) devuelvo 1 y luego le sumo 1.
        conteo[p.nombre] = conteo.get(p.nombre, 0) + 1

        #  -------Otra forma, lo dejo a modo ilustrativo ----------
        # Miramos si el producto ya está en nuestro diccionario de conteo
        """if p.nombre in conteo:
            # Si ya existe, le sumamos 1 al número que ya teníamos guardado
            conteo[p.nombre] = conteo[p.nombre] + 1
        else:
            # Si es la primera vez que aparece, lo anotamos y ponemos que hay 1
            conteo[p.nombre] = 1"""
        # ---------------------------------------------------------

        # Guardamos el precio unitario
        precios[p.nombre] = p.precio
        
    return conteo, precios



# ==============================
# Generar PDF factura
# ==============================
def generar_factura(carrito):
    # Generar ID único para la factura
    factura_id = str(uuid.uuid4())[:8] # [:8] Slice, esto corta solo los primeros 8 caracteres:
                                       # porque el que genera es muy grande de 128 bits.

    # Ejemplo de lo que genera: 550e8400-e29b-41d4-a716-446655440000, esto son 128bits (cada caracter esta en hex y 
    # representan 4 bits cada uno -> 32(nº de caracteres aparecidos) * 4 = 128 bits).


    # Fecha actual
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Nombre del archivo
    nombre_archivo = f"factura_{factura_id}.pdf"

    # Cimientos del documento PDF
    doc = SimpleDocTemplate(nombre_archivo) # Estructura base del PDF
    styles = getSampleStyleSheet()          # Paquete de diseños predefinidos
    contenido = []  # Lista vacía donde almacenamos todas las partes de la factura

    # ==============================
    # Datos de la empresa
    # ==============================
    contenido.append(Paragraph("Karan Sainani Electronics S.L.", styles['Normal']))
    contenido.append(Paragraph("Email: contacto@mitienda.com", styles['Normal']))
    contenido.append(Paragraph("Tel: +34 6xx xxx xxx", styles['Normal']))
    
    # Espacio para separar del título
    contenido.append(Spacer(1, 20))

    contenido.append(Paragraph("FACTURA DE COMPRA", styles['Title']))
    contenido.append(Spacer(1, 10))

    # Datos de la factura
    contenido.append(Paragraph(f"ID Factura: {factura_id}", styles['Normal']))
    contenido.append(Paragraph(f"Fecha: {fecha}", styles['Normal']))
    contenido.append(Spacer(1, 10))

    
    # Llamamos a la funcion agrupar_productos y nos devuelve los 2 diccionarios, uno con las cantidades y otro con los precios unitarios.
    conteo, precios = agrupar_productos(carrito.items)


    # ------ Generar las lineas del PDF -------
    total_factura = 0
    
    for nombre, cant in conteo.items():
        precio_unitario = precios[nombre]
        subtotal = precio_unitario * cant
        total_factura += subtotal
        
        # Formato de la línea: Nombre del producto (xCantidad) - Subtotal€
        texto_linea = f"• {nombre} (x{cant}) - {subtotal}€"
        contenido.append(Paragraph(texto_linea, styles['Normal']))

    # --- LÍNEA DIVISORIA ---
    # width="100%": ocupa todo el ancho del margen
    # thickness=1: grosor de la línea
    # lineCap='round': bordes redondeados para que sea más elegante
    linea = HRFlowable(width="100%", thickness=1, lineCap='round', color=black, spaceBefore=10, spaceAfter=10)
    contenido.append(linea)

    # ---- Pie de factura ----
    contenido.append(Spacer(1, 10))
    contenido.append(Paragraph(f"TOTAL: {total_factura}€", styles['Heading2']))

    # Construimos PDF
    doc.build(contenido)

    # Mensaje una vez completado el proceso de compra
    messagebox.showinfo("Compra Exitosa", f"Éxito. Compra realizada. \n📄 Factura generada: {nombre_archivo}")



# ==============================
# Pruebas iniciales, para meter productos manualmente desde el programa, ineficiente.
# Se deja a modo ilustrativo.
# ==============================
"""productos = [
    Producto(1, "Dell XPS", 2000),
    Producto(2, "MacBook pro M5", 4000),
    Producto(3, "iPhone 17 pro", 1400),
    Producto(4, "Samsung s23", 1000),
    Producto(5, "iPad Air M3", 650),
    Producto(6, "JBL Tune 770NC ", 80),
    Producto(7, "Beats Studio Pro", 150),
    Producto(8, "Bose QuietComfort 45", 100),
    Producto(9, "Samsung Odyssey", 100),
    Producto(10, "LG UltraFine", 250),
    Producto(11, "Google Chromecast", 60),
    Producto(12, "Apple TV", 180),
    Producto(13, "HP DeskJet 2720", 90),
    Producto(14, "Canon Pixma PRO", 160),
    Producto(15, "Seagate Backup Plus", 100),
    Producto(16, "Kingston XS1000", 90),
]"""

# Creamos el carrito
#carrito = Carrito()

# ==============================
# Funciones GUI
# ==============================

# Borra la lista visual y la vuelve a dibujar con los productos agrupados y el precio total actualizado.
def actualizar_carrito():
    # Limpiamos el Listbox del carrito 
    lista_carrito.delete(0, END)


    conteo, precios = agrupar_productos(carrito.items)
        
    # Insertamos en el Listbox de forma agrupada
    for nombre, cant in conteo.items():
        subtotal = precios[nombre] * cant
        lista_carrito.insert(END, f"{nombre} (x{cant}) - {subtotal}€")

    # Actualizamos el label con el método total() de mi clase
    label_total.config(text=f"Total: {carrito.total()}€")


# Para añadir en carrito con la cantidad seleccionada
def agregar_producto():

    # Flag, de entrada asumo que el usuario no ha seleccionado nada
    hay_seleccion = False

    # Recorremos todas las cantidades que el usuario marcó con [+] y [-]
    for i, cantidad in enumerate(cantidades_seleccionadas):
        if cantidad > 0:
            hay_seleccion = True
            # Añadimos el producto al carrito 'n' veces
            for _ in range(cantidad):
                # Usamos la lista de objetos que creamos de la DB
                carrito.agregar(productos_db_objetos[i])
            
            # Resetear el contador visual a 0 tras agregar
            cantidades_seleccionadas[i] = 0
            labels_cantidades[i].config(text="0")

    # Si no hay selección     
    if not hay_seleccion:
        messagebox.showwarning("Atención", "No has seleccionado ninguna cantidad.")
    
    # Refrescamos la lista visual del carrito (derecha)
    actualizar_carrito()


# Función para descartar producto del carrito
def eliminar_producto():

    # Vemos si hay seleccion en el carrito
    seleccion = lista_carrito.curselection() 
    if seleccion:
        index = seleccion[0]
        carrito.eliminar(index)
        actualizar_carrito()


# Función para el proceso de finalizar compra
def finalizar_compra():
    if not carrito.items:
        messagebox.showwarning("Error", "El carrito está vacío")
        return

    confirmar = messagebox.askyesno("Confirmar", "¿Deseas finalizar la compra?")
    if confirmar:
        generar_factura(carrito)

        for p in carrito.items:
            # Ahora enviamos el ID para que en la base de datos se actualice y no aparezca ese producto que fue comprado finalmente
            actualizar_stock_producto(p.id)

        carrito.items.clear()
        actualizar_carrito()


# Función para no dejar que el usuario pida más de lo que realmente tengo en el almacén (BD).
def sumar_cantidad(idx):
    # Obtenemos el stock real disponible desde nuestro objeto , idx -> posición en lista, sirve para localizar el contador y la etiqueta correctos en la interfaz.
    stock_disponible = inventario[idx]['Quantity']  # Accedemos primero al producto por su posición [idx] y luego extraemos su valor de stock usando la clave ['Quantity'].
    
    # Vemos si podemos sumar
    if cantidades_seleccionadas[idx] < stock_disponible:
        cantidades_seleccionadas[idx] += 1
        # Actualizamos el texto del cuadro visual
        labels_cantidades[idx].config(text=str(cantidades_seleccionadas[idx]))

    # Si no podemos sumar más
    else:
        messagebox.showwarning("Stock Insuficiente", "No puedes añadir más de lo que hay en inventario.")


# Para quitar elementos 
def restar_cantidad(idx):
    if cantidades_seleccionadas[idx] > 0:
        cantidades_seleccionadas[idx] -= 1
        labels_cantidades[idx].config(text=str(cantidades_seleccionadas[idx]))
    


# ==============================
# Interfaz - GUI
# ==============================
root = Tk()
root.title("Karan Sainani Electronics S.L.")
root.geometry("1300x825") # AnchoxAlto de ventana

# Productos disponibles
Label(root, text="Productos disponibles", font=("Arial", 20, "bold")).grid(row=0, column=0, pady=20, padx=20, sticky="w")

# Lista de productos disponibles
lista_productos = Frame(root, bd=1, relief="sunken", padx=10, pady=10)
lista_productos.grid(row=1, column=0, sticky="nsew", padx=20)

# Lista para guardar las variables de control
vars_productos = []
productos_db_objetos = [] # Aqui guardaremos los objetos con su ID de SQLite

# Lista para guardar las etiquetas de cantidad y poder actualizarlas
labels_cantidades = []
cantidades_seleccionadas = []   # Lista de enteros [0, 0, 0...]

# # --- OBTENER DATOS Y RENDERIZAR ---
inventario = obtener_inventario()


# Recorremos el inventario para crear automáticamente la interfaz de cada producto
# Anotación: Usamos enumerate porque mi inventario es una lista de diccionarios
for i, p in enumerate(inventario):
    # 1. Definimos las variables por defecto
    cantidad = p['Quantity']
    estado_boton = "normal"
    
    # 2. Aplicamos la lógica de umbrales (Thresholds)
    if cantidad > 10:
        texto_stock = "In Stock"
        color_stock = "#28a745"  # Un verde más profesional
    elif 0 < cantidad <= 10:
        texto_stock = f"Low Stock ({cantidad})" # Mostramos cuántos quedan para alertar
        color_stock = "#ff8c00"  # Naranja/Ámbar
    else:
        texto_stock = "Out of Stock"
        color_stock = "#dc3545"  # Rojo intenso
        estado_boton = "disabled" 

    nuevo_obj_producto = Producto(p['id'], p['Name'], p['Quantity'], p['Category'], p['Price'])
    productos_db_objetos.append(nuevo_obj_producto)

    # Inicializamos la cantidad seleccionada para este producto a 0
    cantidades_seleccionadas.append(0)

# --- Renderizado de la fila (Checkbutton + Labels)  ---
    var = IntVar()                  # Para saber si hay algo marcado
    vars_productos.append(var)      # Guardamos en mi lista de control para consultarlo después
    
    # Creamos un frame pequeñito para cada fila
    fila = Frame(lista_productos)
    fila.pack(fill="x", anchor="w", pady=2)
    
    # Checkbox para marcar que productos quiere el usuario
    cb = Checkbutton(fila, variable=var, state=estado_boton)
    cb.pack(side="left")
    
    # Texto con nombre de producto con su precio
    lbl_nombre = Label(
        fila, 
        text=f"{p['Name']} - {p['Price']}€", 
        font=("Arial", 10), 
        width=30, 
        anchor="w"
    )
    lbl_nombre.pack(side="left", padx=5)

    # Texto stock disponible
    lbl_stock = Label(
        fila, 
        text=texto_stock, 
        fg=color_stock, 
        font=("Arial", 9, "bold"),
        width=15,
        anchor="e"
    )
    lbl_stock.pack(side="right", padx=10)


    # Texto copyright
    lbl_copyright = Label(
        root, 
        text="© Karan Sainani 2026 - All Rights Reserved.", 
        font=("Arial", 11, "italic"), 
        fg="gray"
    )
    lbl_copyright.grid(row=4, column=0, columnspan=3, pady=(30, 10))

    # --- Botones ---
    # Botón Menos
    btn_menos = Button(fila, text="-", width=2, 
                       command=lambda idx=i: restar_cantidad(idx))
    btn_menos.pack(side="left", padx=2)

    # Cuadro de visualización de cantidades
    lbl_cant = Label(fila, text="0", width=3, relief="sunken", bg="white")
    lbl_cant.pack(side="left", padx=2)
    labels_cantidades.append(lbl_cant) # La guardamos para cambiar su texto luego

    # Botón Más
    btn_mas = Button(fila, text="+", width=2, 
                     command=lambda idx=i: sumar_cantidad(idx))
    btn_mas.pack(side="left", padx=2)


# --- Resto de botones  ---
frame_botones = Frame(root)
frame_botones.grid(row=1, column=1, padx=10)

# Botón Agregar selección
Button(frame_botones, text="Agregar selección →", command=agregar_producto, width=20).pack(pady=5)
Button(frame_botones, text="← Descartar del carrito", command=eliminar_producto, width=20).pack(pady=5)


# Icono del carrito
Label(root, text="🛒", font=("Arial", 40)).grid(row=0, column=2, pady=10)

# Lista del carrito
lista_carrito = Listbox(root, width=40, height=15, font=("Arial", 15))
lista_carrito.grid(row=1, column=2, padx=20, sticky="nsew")

# --- Total ---
label_total = Label(root, text="Total: 0€", font=("Arial", 12, "bold"), fg="blue")
label_total.grid(row=2, column=2, sticky="e", padx=20, pady=5)

# Botón para finalizar compra
Button(root, text="Finalizar compra", command=finalizar_compra, width=20).grid(row=3, column=2, pady=3)

# Inicia el ciclo de vida de la aplicación. Mantiene la ventana abierta y queda a la espera de que el usuario interactúe.
root.mainloop()





