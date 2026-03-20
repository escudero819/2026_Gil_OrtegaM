from stock import Modificacion
import tkinter as tk
from archivos import Sabores
FUENTE = "Arial 18"
FUENTE_TITULO = "Arial 22 bold"

def Modificacion(estado, ventana):
    for widget in ventana.winfo_children():
        widget.destroy()

    ventana.geometry("500x400")

    def Salir():
        Modo_stock(ventana)

    def presionar_boton():
        resultado = Sabores.Modificar_stock(sabor.get(), estado)
        sabor.delete(0, tk.END)
        if resultado[0]:
            texto_resultado.config(fg="green")
        else:
            texto_resultado.config(fg="red")
        texto_resultado.config(text=resultado[1])

    sabor = tk.Entry(ventana, font=FUENTE)
    texto_resultado = tk.Label(ventana, text="", font=FUENTE)
    boton = tk.Button(ventana, command=presionar_boton, font=FUENTE)

    if estado:
        ventana.title("Renovar Stock")
        texto_explicativo = tk.Label(ventana, text="Ingrese el sabor que desea renovar", font=FUENTE_TITULO)
        boton["text"] = "Renovar"
    else:
        ventana.title("Acabado Stock")
        texto_explicativo = tk.Label(ventana, text="Ingrese el sabor que se acabó", font=FUENTE_TITULO)
        boton["text"] = "ingresar"    

    boton_salida = tk.Button(ventana, text="Salir", command=Salir, font=FUENTE)

    #orden de los elementos:
    texto_explicativo.pack()
    sabor.pack()
    boton.pack()
    texto_resultado.pack()
    boton_salida.pack(side="bottom")

    ventana.mainloop()


def Modo_stock(ventana):
    for widget in ventana.winfo_children():
        widget.destroy()
    ventana.title("Modo Stock") 
    ventana.geometry("400x400")

    def Salir():
        return ventana


    def Renovar():
        Modificacion(True, ventana)
        
    def Acabado():
        Modificacion(False, ventana)

    texto_explicativo = tk.Label(ventana, text="Seleccione una opcion", font=FUENTE_TITULO)
    texto_explicativo.pack()

    boton_renovar = tk.Button(ventana, text="Renovar", command=Renovar, font=FUENTE)
    boton_renovar.pack()

    boton_acabado = tk.Button(ventana, text="Acabado", command=Acabado, font=FUENTE)
    boton_acabado.pack()

    boton_salir = tk.Button(ventana, text="Salir", command=Salir, font=FUENTE)
    boton_salir.pack(side = "bottom")

    ventana.mainloop()
