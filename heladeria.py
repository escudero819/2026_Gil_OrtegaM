
#importamos funciones
import modo_elementos
#import modo_pedidos
#import modo_stock

#importamos tkinter
import tkinter as tk 

#sacamos los valores de la apantalla
import val_pantalla
ancho, alto = val_pantalla.val_pantalla()

#ventana 
ventana = tk.Tk()
ventana.geometry(f"{ancho}x{alto}")

#botones
boton_elementos = tk.Button(ventana, text = "Elementos", command = lambda: ventana.destroy() or modo_elementos.Modo_Elementos())
boton_elementos.place(x = 0, y = 0, width = ancho//2, height = alto)

boton_pedidos = tk.Button(ventana, text = "pedidos")#, command = modo_pedidos.Modo_pedidos)
boton_pedidos.place(x = ancho//4*2, y = 0, width = ancho//2, height = alto//2)

boton_stock = tk.Button(ventana, text = "Stock")#, command = modo_stock.Modo_stock)
boton_stock.place(x = ancho//4*2, y = alto//4*2, width = ancho//2, height = alto//2)


#loop
ventana.mainloop()