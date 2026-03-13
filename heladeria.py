"""
import modo_elementos
import modo_pedidos
import modo_stock
"""
import tkinter as tk 

#sacamos la info de la pantalla 
root = tk.Tk()
root.withdraw()
ancho = root.winfo_screenwidth()
alto  = root.winfo_screenheight()

#tama;o de los botones 
ANCHO_BOTONES = ancho//70
ALTO_BOTONES = alto//60


ventana = tk.Tk()
ventana.geometry(f"{ancho}x{alto}")

#botones
boton_modo_elementos = tk.Button(ventana, text="Modo Elementos", width=ANCHO_BOTONES, height=ALTO_BOTONES)
boton_modo_elementos.pack()

#loop
ventana.mainloop()