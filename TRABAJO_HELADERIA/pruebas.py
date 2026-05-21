import tkinter as tk
from pedido import Pedido
import modo_stock
"""
pedido_actual = Pedido(1)
orden1 = {
    "nombre": "1 bocha",
    "sabores": ["Frutilla"],
    "precio": 700
}
orden2 = {
    "nombre": "1 bocha",
    "sabores": ["Banana"],
    "precio": 700
}
pedido_actual.Añadir(orden1)
pedido_actual.Añadir(orden2)
pedido_actual.Ticket()
"""
ventana = tk.Tk()
ventana.geometry("400x400")
tk.Button(ventana, text = "helado", bg = "#6C6C6C", fg = "white").pack()
tk.Button(ventana, text = "pote", bg = "#6C6C6C", fg = "white").pack()

ventana.mainloop()