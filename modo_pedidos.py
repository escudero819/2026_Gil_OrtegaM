import tkinter as tk
from pedido import Pedido
from archivos import Tipos, Sabores

def Ventana_añadir_producto(ventana_anterior, pedido_actual):
    ventana = tk.Tk()
    ventana.title("Añadir Producto")
    ventana.geometry("400x400")
    global estado
    estado = "Helado" # 2 opciones "Helado"/"Pote" y "Sabores" (condicionada por la cant de sabores posibles a elegir)

    producto_a_añadir = {}

    def Despedida_de_Añadir_Producto(ventana_anterior, pedido_actual):
        ventana_anterior.destroy()

        pedido_actual.VerPedido()

        global estado
        estado = "salida"

    def seleccionar_sabores(ventana, cantidad_sabores):
        global estado
        encabezado = tk.Label(ventana, text="Seleccione los sabores")
        encabezado.pack()

        lista_sabores = tk.Listbox(ventana, selectmode=tk.MULTIPLE)
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
                texto_error = tk.Label(ventana, text="Debe seleccionar exactamente " + str(cantidad_sabores) + " sabores")
                texto_error.pack()
                
            elif len(lista_sabores.curselection()) < cantidad_sabores and len(lista_sabores.curselection()) != 1:
                texto_repetido = tk.Label(ventana, text="Marque que sabor desea repetir")
                texto_repetido.pack()
                lista_opciones = []
                opcion_repetir = tk.Listbox(ventana, selectmode=tk.SINGLE)
                boton_anterior.destroy()

                def avanzar_repetir():
                    eleccion_repetir = opcion_repetir.curselection()

                    if eleccion_repetir:
                        boton_anterior.destroy()

                        eleccion = lista_sabores.curselection()

                        for sabor in eleccion:
                            sabor = lista_sabores.get(sabor)
                            lista_opciones.append(sabor)
                        
                        for sabor in eleccion:
                            sabor = opcion_repetir.get(sabor)
                            lista_opciones.append(sabor)
                        
                        sabores_seleccionados = lista_opciones
                        producto_a_añadir["sabores"] = sabores_seleccionados
                        
                        pedido_actual.Añadir(producto_a_añadir)

                        ventana.destroy()
                        Despedida_de_Añadir_Producto(ventana_anterior, pedido_actual)
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
                
                
                boton_seleccionar_repetir = tk.Button(ventana, text="Seleccionar", command=avanzar_repetir)
                boton_seleccionar_repetir.pack()

                ventana.destroy()
                Despedida_de_Añadir_Producto(ventana_anterior, pedido_actual)
                return

            elif len(lista_sabores.curselection()) == 1:
                eleccion = lista_sabores.curselection()
                if eleccion:
                    eleccion = lista_sabores.get(eleccion[0])
                    producto_a_añadir["sabores"] = [eleccion]
                    pedido_actual.Añadir(producto_a_añadir)
                    ventana.destroy()
                    Despedida_de_Añadir_Producto(ventana_anterior, pedido_actual)
                    return

            elif len(lista_sabores.curselection()) == cantidad_sabores:
                sabores_seleccionados = lista_sabores.curselection()
                producto_a_añadir["sabores"] = sabores_seleccionados
                pedido_actual.Añadir(producto_a_añadir)
                ventana.destroy()
                global estado
                estado = "salida"
                Despedida_de_Añadir_Producto(ventana_anterior, pedido_actual)
                return 

        boton_seleccionar = tk.Button(ventana, text="Seleccionar", command=lambda: avanzar(boton_seleccionar))
        boton_seleccionar.pack()
        


    def seleccionar_producto(ventana):
        encabezado = tk.Label(ventana, text="Seleccione un producto")
        encabezado.pack()

        lista_productos = tk.Listbox(ventana, selectmode=tk.SINGLE)
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
            encabezado.destroy()
            lista_productos.destroy()
            boton_seleccionar.destroy()
            seleccionar_sabores(ventana, caracteristicas['cantidad de sabores'])

        boton_seleccionar = tk.Button(ventana, text="Seleccionar", command=avanzar)
        boton_seleccionar.pack()

        global estado
        indices = lista_productos.curselection()
        if indices:
            indice = indices[0]
            producto = lista_productos.get(indice)
            producto_a_añadir["nombre"] = producto
            producto_a_añadir["precio"] = Productos[producto]["precio"]
            

    if estado == "Helado":
        seleccionar_producto(ventana)
    if estado == "salida":
        ventana.destroy()
        return 
    ventana.mainloop()


def Modo_pedidos(ventana_anterior, nro_pedido):
    ventana_anterior.withdraw()
    ventana = tk.Tk()
    ventana.title("Pedido")
    ventana.geometry(ventana_anterior.geometry())

    pedido_actual = Pedido(nro_pedido)

    texto_nro_pedido = tk.Label(ventana, text="Nro de Pedido: " + str(nro_pedido), font=("Arial", 16))
    texto_nro_pedido.pack()

    def Añadir_producto():
        ventana.withdraw()
        Ventana_añadir_producto(ventana, pedido_actual)

    boton_añadir_producto = tk.Button(ventana, text="Añadir Producto", command=Añadir_producto)
    boton_añadir_producto.pack()

    ventana.mainloop()
    

def Previo_a_modo_pedidos(contraseña, tamaño, ventana_anterior):

    ventana = tk.Tk()
    ventana.title("Modo de Pedidos")
    ventana.geometry(tamaño)
    global Nro
    Nro = 0

    def iniciar_pedido():
        global Nro
        Nro = Nro + 1
        ventana.withdraw()
        Modo_pedidos(ventana, Nro)


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


Previo_a_modo_pedidos("1234", "400x400", tk.Tk())


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