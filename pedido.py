class Pedido():
    
    def __init__(self, nro_pedido):
        self.nro_pedido = nro_pedido
        self.lista_productos = {}
        self.lista_Ids = []
        self.ID_actual = 0
    
    def Añadir(self, caracteristicas):
        self.lista_productos[self.ID_actual] = caracteristicas
        self.lista_Ids.append(self.ID_actual)
        self.ID_actual += 1
    
    def Eliminar(self, ID_eliminar):
        print(self.lista_productos)
        for ID_loop in range(len(self.lista_Ids)):
            print(ID_loop)
            if self.lista_Ids[ID_loop] == ID_eliminar:
                self.lista_productos.pop(ID_eliminar)
                self.lista_Ids.pop(ID_loop)

    def VerPedido(self):
        lista_mostrar = []
        for ID_loop in range(len(self.lista_Ids)):
            producto = self.lista_productos[self.lista_Ids[ID_loop]]
            linea = str(ID_loop) + "- " + str(producto["nombre"]) + ": $" + str(producto["precio"]) + "\n"
            print(linea)
            lista_mostrar.append(linea)
        return lista_mostrar
            