import tkinter as tk
from pedido import Pedido
from archivos import Tipos, Sabores

TAMAÑO_VENTANA = "400x400"
FUENTE = "Arial 18"
FUENTE_TITULO = "Arial 22 bold"

def Ventana_añadir_producto(ventana, pedido_actual):
    for widget in ventana.winfo_children():
        widget.destroy()

    ventana.title("Añadir Producto")
    global estado
    estado = "Helado" # 2 opciones "Helado"/"Pote" y "Sabores" (condicionada por la cant de sabores posibles a elegir)

    global producto_a_añadir
    producto_a_añadir = {}

    def Despedida_de_Añadir_Producto(ventana, pedido_actual, producto_a_añadir):
        for widget in ventana.winfo_children():
            widget.destroy()

        ventana.title("Pedido Añadido")
        encabezado = tk.Label(ventana, text="Pedido Añadido", font=(FUENTE_TITULO))
        encabezado.pack()
        print(producto_a_añadir)
        pedido_actual.Añadir(producto_a_añadir)
        pedido_actual.VerPedido()

        boton_volver = tk.Button(ventana, text="Volver", command= lambda: Modo_pedidos(ventana, pedido_actual), font=(FUENTE))
        boton_volver.pack(side= "bottom")
        ventana.mainloop()

    def seleccionar_sabores(ventana, cantidad_sabores, producto_a_añadir):

        for widget in ventana.winfo_children():
            widget.destroy()

        global estado
        encabezado = tk.Label(ventana, text="Seleccione los sabores", font=(FUENTE_TITULO))
        encabezado.pack()

        lista_sabores = tk.Listbox(ventana, selectmode=tk.MULTIPLE, font=(FUENTE))
        lista_sabores.pack()

        sabores = Sabores.Recopilar()
        for sabor in sabores.keys():
            if sabores[sabor]:
                texto_descriptivo = f"{sabor}"
                lista_sabores.insert(tk.END, texto_descriptivo)
        
        alto_lista_sabores = len(sabores.keys())
        ancho_lista_sabores = max(len(sabor) for sabor in sabores.keys())
        lista_sabores.config(height= alto_lista_sabores, width= ancho_lista_sabores)
        lista_sabores.pack(pady=10)

        def avanzar(boton_anterior):
            if len(lista_sabores.curselection()) > cantidad_sabores:
                texto_error = tk.Label(ventana, text="Debe seleccionar exactamente " + str(cantidad_sabores) + " sabores", font=(FUENTE))
                texto_error.pack()

            elif len(lista_sabores.curselection()) == cantidad_sabores:
                sabores_seleccionados = lista_sabores.curselection()
                producto_a_añadir["sabores"] = []
                for sabor in sabores_seleccionados:
                    sabor = lista_sabores.get(sabor)
                    producto_a_añadir["sabores"].append(sabor)
                
                Despedida_de_Añadir_Producto(ventana, pedido_actual, producto_a_añadir)
                return 
                
            elif len(lista_sabores.curselection()) < cantidad_sabores and len(lista_sabores.curselection()) != 1:
                texto_repetido = tk.Label(ventana, text="Marque que sabor desea repetir", font=(FUENTE))
                texto_repetido.pack()
                lista_opciones = []
                sabores_elegidos = lista_sabores.curselection()
                for sabor in sabores_elegidos:
                    sabor = lista_sabores.get(sabor)
                    lista_opciones.append(sabor)
                opcion_repetir = tk.Listbox(ventana, selectmode=tk.SINGLE, font=(FUENTE))
                boton_anterior.destroy()

                def avanzar_repetir():
                    eleccion_repetir = opcion_repetir.curselection()

                    if eleccion_repetir:
                        boton_anterior.destroy()
                        
                        for sabor in eleccion_repetir:
                            sabor = opcion_repetir.get(sabor)
                            lista_opciones.append(sabor)
                        
                        sabores_seleccionados = lista_opciones
                        producto_a_añadir["sabores"] = sabores_seleccionados
                        
                        Despedida_de_Añadir_Producto(ventana, pedido_actual, producto_a_añadir)
                        return

                eleccion = lista_sabores.curselection()
                if eleccion:
                    for sabor in eleccion:
                        sabor = lista_sabores.get(sabor)
                        opcion_repetir.insert(tk.END, sabor)

                alto_lista_opciones = len(opcion_repetir.get(0, tk.END))
                ancho_lista_opciones = max(len(sabor) for sabor in opcion_repetir.get(0, tk.END))
                opcion_repetir.config(height= alto_lista_opciones, width= ancho_lista_opciones)

                opcion_repetir.pack()
                
                boton_seleccionar_repetir = tk.Button(ventana, text="Seleccionar", font=(FUENTE), command=avanzar_repetir)
                boton_seleccionar_repetir.pack()

            elif len(lista_sabores.curselection()) == 1:
                eleccion = lista_sabores.curselection()
                if eleccion:
                    eleccion = lista_sabores.get(eleccion[0])
                    producto_a_añadir["sabores"] = []
                    for cantidad in range(cantidad_sabores):
                        producto_a_añadir["sabores"].append(eleccion)
                    Despedida_de_Añadir_Producto(ventana, pedido_actual, producto_a_añadir)
                    return



        boton_seleccionar = tk.Button(ventana, text="Seleccionar", command=lambda: avanzar(boton_seleccionar), font=(FUENTE))
        boton_seleccionar.pack()
        


    def seleccionar_producto(ventana):
        encabezado = tk.Label(ventana, text="Seleccione un producto", font=(FUENTE_TITULO))
        encabezado.pack()

        global producto_a_añadir
        producto_a_añadir = {}

        lista_productos = tk.Listbox(ventana, selectmode=tk.SINGLE, font=(FUENTE))
        lista_productos.pack()
        # agrego los productos a la lista
        Productos = Tipos.Recopilar()
        texto_mas_largo = ""
        for producto, caracteristicas in Productos.items():
            texto_descriptivo = f"{producto} - ${caracteristicas['precio']} - {caracteristicas['cantidad de sabores']} sabores"
            lista_productos.insert(tk.END, texto_descriptivo)
            if len(texto_descriptivo) > len(texto_mas_largo):
                texto_mas_largo = texto_descriptivo

        # ajusto el tamaño de la lista
        alto_lista_productos = len(Productos.keys())
        ancho_lista_productos = len(texto_mas_largo)
        lista_productos.config(height= alto_lista_productos, width= ancho_lista_productos)

        lista_productos.pack(pady=10)

        def avanzar():
            indices = lista_productos.curselection()
            if indices:
                indice = indices[0]
                producto = lista_productos.get(indice).split(" - ")[0]
                producto_a_añadir["nombre"] = producto
                producto_a_añadir["precio"] = Productos[producto]["precio"]
                seleccionar_sabores(ventana, Productos[producto]['cantidad de sabores'], producto_a_añadir)

        boton_seleccionar = tk.Button(ventana, text="Seleccionar", font=(FUENTE), command=avanzar)
        boton_seleccionar.pack()

    if estado == "Helado":
        seleccionar_producto(ventana)
    if estado == "salida":
        ventana.destroy()
        return 
    ventana.mainloop()

def Ventana_Eliminar_Producto(ventana, pedido_actual):
    for widget in ventana.winfo_children():
        widget.destroy()
    ventana.title("Eliminar Producto")
    ventana.geometry(ventana.geometry())
    

    def avanzar():
        indices = lista_productos.curselection()
        if indices:
            indice = indices[0]
            producto = lista_productos.get(indice).split("-")[0]
            pedido_actual.Eliminar(producto)
            Ventana_Eliminar_Producto(ventana, pedido_actual)


    # agrego los productos a la lista
    Productos = pedido_actual.VerPedido()
    if Productos:
        lista_productos = tk.Listbox(ventana, selectmode=tk.SINGLE, font=(FUENTE, 12))
        lista_productos.pack()
        texto_mas_largo = ""
        for producto in Productos:
            lista_productos.insert(tk.END, producto)
            if len(producto) > len(texto_mas_largo):
                texto_mas_largo = producto
        # ajusto el tamaño de la lista
        alto_lista_productos = len(Productos)
        ancho_lista_productos = len(texto_mas_largo)
        lista_productos.config(height= alto_lista_productos, width= ancho_lista_productos)

        lista_productos.pack(pady=10)

        boton_seleccionar = tk.Button(ventana, text="Seleccionar", font=(FUENTE), command=avanzar)
        boton_seleccionar.pack()
        
    else:
        texto_no_productos = tk.Label(ventana, text="No hay productos en el pedido", font=(FUENTE))
        texto_no_productos.pack()

    boton_salir = tk.Button(ventana, text="Volver", command=lambda: Modo_pedidos(ventana, pedido_actual), font=(FUENTE))
    boton_salir.pack(side= "bottom")

    ventana.mainloop()


def Ventana_Recibo(ventana, pedido_actual):
    for widget in ventana.winfo_children():
        widget.destroy()
    ventana.title("Recibo")
    ventana.geometry(ventana.geometry())

    texto_nro_pedido = tk.Label(ventana, text="Nro de Pedido: " + str(pedido_actual.nro_pedido), font=(FUENTE_TITULO))
    texto_nro_pedido.pack()

    for producto in pedido_actual.VerPedido():
        mostrar_producto = tk.Label(ventana, text=producto, font=(FUENTE))
        mostrar_producto.pack()
    
    linea = tk.Label(ventana, text="-"*len(max(pedido_actual.VerPedido(), key=len)), font=(FUENTE))
    linea.pack()
    precio_total = tk.Label(ventana, text="Precio Total: $" + str(pedido_actual._PrecioTotal()), font=(FUENTE))
    precio_total.pack()

    linea_Id_ticket = tk.Label(ventana, text="Guardando como ticket" + str(pedido_actual.nro_pedido) + ".txt", font=(FUENTE))
    linea_Id_ticket.pack()

    def Salir():
        pedido_actual.Ticket()
        Previo_a_modo_pedidos(ventana, pedido_actual._contraseña)
    
    boton_salir = tk.Button(ventana, text="Volver", command=Salir, font=(FUENTE))
    boton_salir.pack(side= "bottom")

def Ventana_Ver_Pedido(ventana, pedido_actual):
    for widget in ventana.winfo_children():
        widget.destroy()
    ventana.title("Pedido")
    ventana.geometry(ventana.geometry())

    texto_nro_pedido = tk.Label(ventana, text="Nro de Pedido: " + str(pedido_actual.nro_pedido), font=(FUENTE_TITULO))
    texto_nro_pedido.pack()

    for producto in pedido_actual.VerPedido():
        mostrar_producto = tk.Label(ventana, text=producto, font=(FUENTE))
        mostrar_producto.pack()
    
    linea = tk.Label(ventana, text="-"*len(max(pedido_actual.VerPedido(), key=len)), font=(FUENTE))
    linea.pack()
    precio_total = tk.Label(ventana, text="Precio Total: $" + str(pedido_actual._PrecioTotal()), font=(FUENTE))
    precio_total.pack()

    def Añadir_producto():
        Ventana_añadir_producto(ventana, pedido_actual)

    boton_añadir_producto = tk.Button(ventana, text="Añadir Producto", command=Añadir_producto, font=(FUENTE))
    boton_añadir_producto.pack()

    def Eliminar_producto():
        Ventana_Eliminar_Producto(ventana, pedido_actual)

    boton_eliminar_producto = tk.Button(ventana, text="Eliminar Producto", command=Eliminar_producto, font=(FUENTE))
    boton_eliminar_producto.pack()

    def Obtener_Recibo():
        Ventana_Recibo(ventana, pedido_actual)
    
    boton_obtener_recibo = tk.Button(ventana, text="Obtener Recibo", command=Obtener_Recibo, font=(FUENTE))
    boton_obtener_recibo.pack()

    def Volver():
        Modo_pedidos(ventana, pedido_actual)

    boton_volver = tk.Button(ventana, text="Volver", command=Volver, font=(FUENTE))
    boton_volver.pack(side= "bottom")


def Modo_pedidos(ventana, pedido_actual):
    for widget in ventana.winfo_children():
        widget.destroy()

    ventana.title("Pedido")
    ventana.geometry(ventana.geometry())

    texto_nro_pedido = tk.Label(ventana, text="Nro de Pedido: " + str(pedido_actual.nro_pedido), font=(FUENTE_TITULO))
    texto_nro_pedido.pack()

    def Añadir_producto():
        Ventana_añadir_producto(ventana, pedido_actual)

    boton_añadir_producto = tk.Button(ventana, text="Añadir Producto", command=Añadir_producto, font=(FUENTE))
    boton_añadir_producto.pack()

    def Eliminar_producto():
        Ventana_Eliminar_Producto(ventana, pedido_actual)

    boton_eliminar_producto = tk.Button(ventana, text="Eliminar Producto", command=Eliminar_producto, font=(FUENTE))
    boton_eliminar_producto.pack()

    def Ver_pedido():
        Ventana_Ver_Pedido(ventana, pedido_actual)

    boton_ver_pedido = tk.Button(ventana, text="Ver Pedido", command=Ver_pedido, font=(FUENTE))
    boton_ver_pedido.pack()

    def Salir():
        ventana.destroy()
        ventana_anterior.deiconify()

    boton_salir = tk.Button(ventana, text="Salir", command=Salir, font=(FUENTE))
    boton_salir.pack(side= "bottom")

    ventana.mainloop()
    

def Previo_a_modo_pedidos(ventana, contraseña):

    for widget in ventana.winfo_children():
        widget.destroy()
    
    ventana.title("Modo de Pedidos")

    global Nro
    Nro = 0

    def iniciar_pedido():
        global Nro
        Nro = Nro + 1
        pedido_actual = Pedido(Nro, contraseña)
        Modo_pedidos(ventana, pedido_actual)


    texto_contrasena = tk.Label(ventana, text="Ingrese la contraseña")
    texto_contrasena.pack(side= "bottom")
    caja_contrasena = tk.Entry(ventana, show="*")
    caja_contrasena.pack(side= "bottom")

    def volver():
        verificacion = caja_contrasena.get()
        if verificacion == contraseña:
            ventana_anterior.deiconify()
            ventana.destroy()
        else:
            texto_contrasena.config(text="Contraseña incorrecta")
            texto_contrasena.pack(side= "bottom")

    boton_iniciar_pedido = tk.Button(ventana, text="Iniciar Pedido", command= iniciar_pedido)
    boton_iniciar_pedido.pack()

    boton_volver = tk.Button(ventana, text="Volver", command=volver)
    boton_volver.pack(side= "bottom")

    ventana.mainloop()


ventana_x = tk.Tk()
ventana_x.geometry(TAMAÑO_VENTANA)
ventana_x.title("Menu Principal")
Previo_a_modo_pedidos(ventana_x, "1234")

"""
print("1- Agregar")
print("2- Eliminar")
print("3- ver Pedido")
print("4- Terminaar Pedido")
print("5- cancelar pedido")
op = int(input("--"))

if op == 1:
    # aca se deriva a la funcion de agregar un cono / pote

if op == 2:
    # aca derivara a mostrar la listas de conos / potes y pedira que ingrese el indice O el nombre de la persona

if op == 3:
    # muestra la lista de helados con helados con sus caracteristicas, precios y total

if op == 4:
    # alculara el total y mostrara un recibo creado en un txt aparte

if op == 5:
    # en esta opcion debera pedir el codigo de salida que se entrega al iniciar este modo y retornara o ejecutara el menu principal
"""