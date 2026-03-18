"""
 objeto pedido encargado de gestionar los helados de un recibo y la compra actual,  tiene metodos para añadir, eliminar y ver el pedido
 ademas de poder armar un txt con el ticket y precio total

"""
class Pedido():
    
    PATH = "ventas/"
    
    def __init__(self, nro_pedido, contraseña):
        self.nro_pedido = nro_pedido
        self.lista_productos = {}
        self.lista_Ids = []
        self._contraseña = contraseña
        self.ID_actual = 0
    
    def Añadir(self, caracteristicas):
        self.lista_productos[str(self.ID_actual)] = caracteristicas
        self.lista_Ids.append(str(self.ID_actual))
        self.ID_actual += 1
    
    def Eliminar(self, ID_eliminar):
        for ID_loop in range(len(self.lista_Ids)):
            if self.lista_Ids[ID_loop] == ID_eliminar:
                self.lista_productos.pop(ID_eliminar)
                self.lista_Ids.pop(ID_loop)

    def VerPedido(self, sabores=True):
        lista_mostrar = []
        for ID_loop in range(len(self.lista_Ids)):
            producto = self.lista_productos[self.lista_Ids[ID_loop]]
            if sabores:
                    linea = str(ID_loop) + "- " + str(producto["nombre"]) + ": $" + str(producto["precio"]) + " | Sabores: " +str(producto["sabores"]) + "\n"
            else:
                linea = str(ID_loop) + "- " + str(producto["nombre"]) + ": $" + str(producto["precio"]) + "\n"
            lista_mostrar.append(linea)
        return lista_mostrar
    
    def _PrecioTotal(self):
        precio_total = 0
        for ID_loop in range(len(self.lista_Ids)):
            precio_total += self.lista_productos[self.lista_Ids[ID_loop]]["precio"]
        return precio_total
    
    def Ticket(self):
        archivo = self.PATH + "ticket"+str(self.nro_pedido)+".txt"
        with open(archivo, "w") as archivo:
            # Cabecera
            archivo.write("Ticket Nro: " + str(self.nro_pedido) + "\n")
            # Lista de productos
            for ID_loop in range(len(self.lista_Ids)):
                producto = self.lista_productos[self.lista_Ids[ID_loop]]
                linea = str(ID_loop) + "- " + str(producto["nombre"]) + ": $" + str(producto["precio"]) + "\n"
                archivo.write(linea)
            # Pie con el total
            archivo.write("-"*20 + "\n")
            archivo.write("Precio Total: " + str(self._PrecioTotal()) + "\n")
