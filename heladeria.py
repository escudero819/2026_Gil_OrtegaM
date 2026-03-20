
#importamos funciones
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

boton_pedidos = tk.Button(ventana, text = "Pedidos", font = LETRA, command = lambda: modo_pedidos.Modo_pedidos(tk.Tk(), ventana_anterior=ventana))
boton_pedidos.pack()

boton_stock = tk.Button(ventana, text = "Stock", font = LETRA,  command = lambda: modo_stock.Modo_stock(tk.Tk(), ventana_anterior=ventana))
boton_stock.pack()


#loop
ventana.mainloop()