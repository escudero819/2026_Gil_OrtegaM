
#importamos funciones
from modo_pedidos import Modo_pedidos
import modo_elementos
import modo_pedidos
import modo_stock

#importamos tkinter
import tkinter as tk 

LETRA = "Arial 20"
#ventana 
ventana = tk.Tk()
ventana.geometry(f"{400}x{400}")
LETRA_TITULO = "Arial 30 bold"

titulo = tk.Label(ventana, text = "HELADERIA", font = LETRA_TITULO, relief = "sunken")
titulo.pack()

text = tk.Label(ventana, text = "selecione un modo", font = LETRA)
text.pack()

#botones
boton_elementos = tk.Button(ventana, text = "Elementos", font = LETRA, command = lambda: modo_elementos.Modo_Elementos(tk.Tk(), ventana_anterior=ventana))
boton_elementos.pack()


boton_stock = tk.Button(ventana, text = "Stock", font = LETRA,  command = lambda: modo_stock.Modo_stock(tk.Tk(), ventana_anterior=ventana))
boton_stock.pack()

def Pedir_contraseña(ventana, ventana_anterior):
    for widget in ventana.winfo_children():
        widget.destroy()
    
    ventana.geometry(ventana_anterior.geometry())
    
    texto_explicativo = tk.Label(ventana, text="Ingrese la contraseña de salida", font=LETRA_TITULO)
    texto_explicativo.pack()
    caja_contraseña = tk.Entry(ventana, font=LETRA)
    caja_contraseña.pack()
    
    def Ingresar_contraseña():
        contraseña = caja_contraseña.get()
        if contraseña:
            modo_pedidos.Previo_a_modo_pedidos(tk.Tk(), contraseña, ventana_anterior= ventana)

    boton_contraseña = tk.Button(ventana, text="ingresar", font=LETRA, command= lambda: Ingresar_contraseña())
    boton_contraseña.pack()

    def salir(ventana):
        ventana.destroy()
        ventana_anterior.deiconify()
    

boton_pedidos = tk.Button(ventana, text = "Pedidos", font = LETRA, command = lambda: Pedir_contraseña(tk.Tk(), ventana))
boton_pedidos.pack()


#loop
ventana.mainloop()