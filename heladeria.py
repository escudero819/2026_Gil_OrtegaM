"""
import modo_elementos
import modo_pedidos
import modo_stock
"""
import tkinter

ANCHO_BOTONES = 20
ALTO_BOTONES = 5
FUENTE = "italica 20"

ventana = tkinter.Tk()
ventana.geometry("1280x720")


boton_modo_elementos = tkinter.Button(ventana, text= "Modo Elementos",font= FUENTE, width= ANCHO_BOTONES, height= ALTO_BOTONES)
boton_modo_pedidos = tkinter.Button(ventana, text= "Modo de Pedidos",font= FUENTE, width= ANCHO_BOTONES, height= ALTO_BOTONES)
boton_modo_stock = tkinter.Button(ventana, text= "Modo Stock",font= FUENTE, width= ANCHO_BOTONES, height= ALTO_BOTONES)

boton_modo_pedidos.pack()
boton_modo_elementos.pack()


ventana.mainloop()