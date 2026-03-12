import stock
import tkinter as tk

TAMAÑO_LETRA = "15"

def Modo_stock(ventana_anterior):
    ventana = tk.Tk()
    ventana.title("Modo Stock")
    ventana.geometry("700x400")

    def Salir():
        ventana_anterior.deiconify()
        ventana.destroy()
        return

    def Renovar():
        ventana.withdraw()
        stock.Modificacion(True, ventana, "700x400")
        

    def Acabado():
        ventana.withdraw()
        stock.Modificacion(False, ventana, "700x400")

    texto_explicativo = tk.Label(ventana, text="Seleccione una opcion", font=("Arial", TAMAÑO_LETRA))
    texto_explicativo.pack()

    boton_renovar = tk.Button(ventana, text="Renovar", command=Renovar, font=("Arial", TAMAÑO_LETRA))
    boton_renovar.pack()

    boton_acabado = tk.Button(ventana, text="Acabado", command=Acabado, font=("Arial", TAMAÑO_LETRA))
    boton_acabado.pack()

    boton_salir = tk.Button(ventana, text="Salir", command=Salir, font=("Arial", TAMAÑO_LETRA))
    boton_salir.pack(side = "bottom")

    ventana.mainloop()