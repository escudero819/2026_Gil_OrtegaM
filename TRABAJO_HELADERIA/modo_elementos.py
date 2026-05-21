import val_pantalla
import tkinter as tk
from archivos import Sabores
from archivos import Tipos

LETRA = "Arial 20"
LETRA_TEXTO = "Arial 10"

def ventana_sabores(ventana):
     for widget in ventana.winfo_children():
          widget.destroy()

     #la info de la pantalla 
     ancho, alto = val_pantalla.val_pantalla()
     texto = tk.Label(ventana, text = "Sabores", font = LETRA)
     texto.pack()
     
     def añadir_sabor(ventana):
          for widget in ventana.winfo_children():
               widget.destroy()
          
          ingreso_nombre = tk.Entry(ventana, font = LETRA)
          ingreso_nombre.pack()

          def guardarNombre():
               nombre = ingreso_nombre.get()
               nombre = nombre.capitalize()
               print(nombre)
               Sabores.Añadir(nombre)
          
          def salir():
               Modo_Elementos(ventana)
          
          boton_guardar = tk.Button(ventana, text = "guardar", font = LETRA, command = guardarNombre)
          boton_guardar.pack()
          

          boton_salir = tk.Button(ventana, text = "salir", font = LETRA, command = salir)
          boton_salir.pack(side = "bottom")
          ventana.mainloop()
     
     boton_añadir = tk.Button(ventana, text = "añadir", font = LETRA, command = lambda: añadir_sabor(ventana))
     boton_añadir.pack()

     def eliminar_sabor(ventana):
          for widget in ventana.winfo_children():
               widget.destroy()
               
          ingreso_nombre = tk.Entry(ventana, font= LETRA)
          ingreso_nombre.pack()

          def eliminarNombre():
               nombre = ingreso_nombre.get()
               nombre = nombre.capitalize()
               Sabores.Eleminar([nombre])

          boton_eliminar = tk.Button(ventana, text = "eliminar", font = LETRA, command = eliminarNombre)
          boton_eliminar.pack()

          def Volver(ventana):
               ventana_sabores(ventana)
     
          boton_salir = tk.Button(ventana, text = "salir", font = LETRA, command = lambda: Volver(ventana))
          boton_salir.pack(side = "bottom")
          
          ventana.mainloop()
     
     boton_eliminar = tk.Button(ventana, text = "eliminar", font = LETRA, command = lambda: eliminar_sabor(ventana))
     boton_eliminar.pack()
     
     def salir(ventana):
          Modo_Elementos(ventana)
     
     boton_salir = tk.Button(ventana, text = "salir", font = LETRA, command = lambda:salir(ventana))
     boton_salir.pack(side = "bottom")

     ventana.mainloop()

def ventana_tipos(ventana):
     for widget in ventana.winfo_children():
          widget.destroy()

     #la info de la pantalla 
     ancho, alto = val_pantalla.val_pantalla()
     texto = tk.Label(ventana, text = "Tipos", font = LETRA)
     texto.pack()
     
     def añadir_tipo(ventana):
          for widget in ventana.winfo_children():
               widget.destroy()
          
          
          text_nombre = tk.Label(ventana, text= "Nombre", font = LETRA_TEXTO)
          text_nombre.pack()
          
          ingreso_nombre = tk.Entry(ventana, font = LETRA)
          ingreso_nombre.pack()
          
          text_sabores = tk.Label(ventana, text= "cantidad sabores", font = LETRA_TEXTO)
          text_sabores.pack()
          
          cantidad_de_sabores = tk.Entry(ventana, font = LETRA)
          cantidad_de_sabores.pack()
          
          text_precio = tk.Label(ventana,text= "precio", font = LETRA_TEXTO)
          text_precio.pack()
          
          ingrese_precio = tk.Entry(ventana, font = LETRA)
          ingrese_precio.pack()
          
          def guardarNombre():
               nombre = ingreso_nombre.get()
               nombre = nombre.capitalize()
               precio = int(ingrese_precio.get())
               cantidad_sabores = int(cantidad_de_sabores.get())
               añadido = { nombre: {"cantidad de sabores": cantidad_sabores, "precio": precio} }
               Tipos.Añadir(añadido)
               texto_result = tk.Label(ventana, text= f"{añadido} Añadido Correctamente")
               texto_result.pack()
               
          
          def salir():
               Modo_Elementos(ventana)
          
          boton_guardar = tk.Button(ventana, text = "guardar", font = LETRA, command = guardarNombre)
          boton_guardar.pack()
          

          boton_salir = tk.Button(ventana, text = "salir", font = LETRA, command = salir)
          boton_salir.pack(side = "bottom")
          ventana.mainloop()
     
     boton_añadir = tk.Button(ventana, text = "añadir", font = LETRA, command = lambda: añadir_tipo(ventana))
     boton_añadir.pack()

     def eliminar_tipo(ventana):
          for widget in ventana.winfo_children():
               widget.destroy()
          ingreso_nombre = tk.Entry(ventana)
          ingreso_nombre.pack()

          def eliminarNombre():
               nombre = ingreso_nombre.get()
               nombre = nombre.capitalize()
               Sabores.Eleminar([nombre])

          boton_eliminar = tk.Button(ventana, text = "eliminar", font = LETRA, command = eliminarNombre)
          boton_eliminar.pack()

          def salir(ventana):
               ventana_tipos(ventana)

          boton_salir = tk.Button(ventana, text = "salir", font = LETRA, command = lambda:salir(ventana))
          boton_salir.pack(side = "bottom")

          ventana.mainloop()
     
     boton_eliminar = tk.Button(ventana, text = "eliminar", font = LETRA, command = lambda: eliminar_tipo(ventana))
     boton_eliminar.pack()
     
     def salir(ventana):
          Modo_Elementos(ventana)
     
     boton_salir = tk.Button(ventana, text = "salir", font = LETRA, command = lambda:salir(ventana))
     boton_salir.pack(side = "bottom")

     ventana.mainloop()




def Modo_Elementos(ventana, ventana_anterior = None):
     for widget in ventana.winfo_children():
          widget.destroy()

     #la info de la pantalla 
     if ventana_anterior:
          ventana.geometry(ventana_anterior.geometry())

     texto = tk.Label(ventana, text = "Modo elementos", font = LETRA)
     texto.pack()
     #botones
     bot_sabores= tk.Button(ventana, text = "sabores", font = LETRA, command = lambda: ventana_sabores(ventana))
     bot_sabores.pack()
     
     bot_tipos= tk.Button(ventana, text = "tipos", font = LETRA, command = lambda: ventana_tipos(ventana))
     bot_tipos.pack()
     def salir(ventana, ventana_anterior):
          ventana.destroy()
          ventana_anterior.deiconify()
     boton_salir = tk.Button(ventana, text = "salir", font = LETRA, command = lambda:salir(ventana, ventana_anterior))
     boton_salir.pack(side = "bottom")
     
     #el coso del loop 
     ventana.mainloop()
