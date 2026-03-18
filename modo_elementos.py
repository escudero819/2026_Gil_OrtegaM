import val_pantalla
import tkinter as tk
def Modo_Elementos():

    #la info de la pantalla 
    ancho, alto = val_pantalla.val_pantalla()

    def vent_inicial():
         ventana_inicio = tk.Tk()
         ventana_inicio.geometry(f"{ancho}x{alto}")
         ventana_inicio.config(bg = "black")

         #botones
         bot_añadir= tk.Button(ventana_inicio, text = "añadir", bg = "#6C6C6C", fg = "white", command = lambda: ventana_inicio.destroy() or vent_agre())
         bot_añadir.place(x = ancho//100*45, y = alto//100*45, width = ancho//10, height = alto//10)
         
         bot_eliminar= tk.Button(ventana_inicio, text = "eliminar", bg = "#6C6C6C", fg = "white", command = lambda: ventana_inicio.destroy() or vent_elim())
         bot_eliminar.place(x = ancho//100*45, y = alto//100*55, width = ancho//10, height = alto//10)
         

         #el coso del loop 
         ventana_inicio.mainloop()


    def vent_agre():
         ventana_agre = tk.Tk()
         ventana_agre.geometry(f"{ancho}x{alto}")
         ventana_agre.config(bg = "black")
         caja_texto = tk.Entry(ventana_agre)
         caja_texto.place(x = ancho//100*42, y = alto//100*50, width = ancho//6, height = alto//25)


         def coso():
               with open("elementos.txt", "a", encoding="utf-8") as archivo:
                    archivo.write(caja_texto.get() + "\n")

         bot_guar = tk.Button(ventana_agre, text = "guardar", bg = "#6C6C6C", fg = "white", command = coso)
         bot_guar.place(x = ancho//100*45, y = alto//100*55, width = ancho//10, height = alto//25)
         ventana_agre.mainloop()


         def vent_elim():
         ventana_elim = tk.Tk()
         ventana_elim.geometry(f"{ancho}x{alto}")
         ventana_elim.config(bg = "black")
         caja_texto = tk.Entry(ventana_elim)
         caja_texto.place(x = ancho//100*42, y = alto//100*50, width = ancho//6, height = alto//25)


         def coso():
               with open("elementos.txt", "a", encoding="utf-8") as archivo:
                    archivo.write(caja_texto.get() + "\n")

         bot_guar = tk.Button(ventana_elim, text = "guardar", bg = "#6C6C6C", fg = "white", command = coso)
         bot_guar.place(x = ancho//100*45, y = alto//100*55, width = ancho//10, height = alto//25)
         ventana_elim.mainloop()

     vent_inicial() 