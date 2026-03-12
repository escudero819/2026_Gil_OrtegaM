import tkinter as tk
from archivos import Sabores

TAMAÑO_LETRA = "15"

def Modificacion(estado, ventana_anterior, tamaño_ventana):

    ventana = tk.Tk()
    ventana.geometry(tamaño_ventana)

    def Salir():
        ventana_anterior.deiconify()
        ventana.destroy()
        return 

    def presionar_boton():
        resultado = Sabores.Modificar_stock(sabor.get(), estado)
        sabor.delete(0, tk.END)
        if resultado[0]:
            texto_resultado.config(fg="green")
        else:
            texto_resultado.config(fg="red")
        texto_resultado.config(text=resultado[1])

    sabor = tk.Entry(ventana, font=("Arial", TAMAÑO_LETRA))
    texto_resultado = tk.Label(ventana, text="", font=("Arial", TAMAÑO_LETRA))
    boton = tk.Button(ventana, command=presionar_boton, font=("Arial", TAMAÑO_LETRA))

    if estado:
        ventana.title("Renovar Stock")
        texto_explicativo = tk.Label(ventana, text="Ingrese el sabor que desea renovar", font=("Arial", TAMAÑO_LETRA))
        boton["text"] = "Renovar"
    else:
        ventana.title("Acabado Stock")
        texto_explicativo = tk.Label(ventana, text="Ingrese el sabor que se acabó", font=("Arial", TAMAÑO_LETRA))
        boton["text"] = "ingresar"    

    boton_salida = tk.Button(ventana, text="Salir", command=Salir, font=("Arial", TAMAÑO_LETRA))

    #orden de los elementos:
    texto_explicativo.pack()
    sabor.pack()
    boton.pack()
    texto_resultado.pack()
    boton_salida.pack(side="bottom")

    ventana.mainloop()