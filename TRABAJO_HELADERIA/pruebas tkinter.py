import tkinter

ventana = tkinter.Tk()
ventana.geometry("1280x720")

#etiqueta = tkinter.Label(ventana, text = "Hola Mundo", bg= "blue")
#etiqueta.pack(fill= tkinter.BOTH, expand= True) #fill estirar con expand=True, side, donde se pondra el texto

#def saludo(nombre):
#    print("hola " + nombre)

#boton1 = tkinter.Button(ventana, text= "Presiona", padx= 40, pady = 50, command = lambda: saludo("python")) #siempre sin el parentesis si no tiene parametros, usar lambda para darle los parametros
#boton1.pack()

# manejo de cajas de texto, y replicacion en una etiqueta
"""
cajaTexto = tkinter.Entry(ventana) #font= <<fuente>>
cajaTexto.pack()

etiqueta = tkinter.Label(ventana)
etiqueta.pack()
def textoDeLaCaja():
    texto = cajaTexto.get()
    etiqueta["text"] = texto

boton1 = tkinter.Button(ventana, text = "click", command= textoDeLaCaja)
boton1.pack()
"""

#metodo Grid

boton1 = tkinter.Button(ventana, text= "Boton1", width= 10, height= 5)
boton2 = tkinter.Button(ventana, text= "Boton2", width= 10, height= 5)
boton3 = tkinter.Button(ventana, text= "Boton3", width= 10, height= 5)

boton1.grid(row= 0, column = 0)
boton2.grid(row= 2, column = 0)
boton3.grid(row= 1, column = 0)

ventana.mainloop()