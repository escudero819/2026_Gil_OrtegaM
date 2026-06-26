import arcade
import os

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))   

Colisiones_Transparentes = True

class Objeto(arcade.Sprite):

    def __init__(self, tipo, imagen_path, center_x, center_y):
        super().__init__(imagen_path, center_x=center_x, center_y=center_y)
        self.tipo = tipo

class Interactuable(Objeto):
    
    def __init__(self, nombre: str, imagen_path: str, center_x: int, center_y: int, funcion: callable, ubicacion_jugador = None):
        super().__init__("interactuable", imagen_path, center_x, center_y)
        self.nombre = nombre
        self.funcion = funcion
        if ubicacion_jugador:
            self.ubicacion_jugador = {
                "x": self.center_x + ubicacion_jugador[0],
                "y": self.center_y + ubicacion_jugador[1] 
            }
        else:
            self.ubicacion_jugador = {
                "x": center_x,
                "y": center_y
                }
            
        print(f"Interactuable '{self.nombre}' creado en ({self.center_x}, {self.center_y}) con ubicación de jugador en ({self.ubicacion_jugador['x']}, {self.ubicacion_jugador['y']})")

class Salida(Interactuable):

    def __init__(self, center_x, center_y, ancho, alto, funcion):
        if Colisiones_Transparentes:
            super().__init__("salida", CURRENT_PATH + "/transparente.png", center_x, center_y, funcion)
        else:
            super().__init__("salida", CURRENT_PATH + "/semitransparente_rojo.png", center_x, center_y, funcion)
        self.width = ancho
        self.height = alto

class Bloqueo(Objeto):

    def __init__(self, center_x, center_y, ancho, alto):
        if Colisiones_Transparentes:
            super().__init__("bloqueo", CURRENT_PATH + "/transparente.png", center_x, center_y)
        else:
            super().__init__("bloqueo", CURRENT_PATH + "/semitransparente_rojo.png", center_x, center_y)
        self.width = ancho
        self.height = alto

class Inventario():

    def __init__(self):
        self.lista_objetos = []
    
    def agregar_objeto(self, objeto):
        self.lista_objetos.append(objeto)
    
    def consultar(self, nombre_objeto):
        for objeto in self.lista_objetos:
            if objeto == nombre_objeto:
                return True
    
    def eliminar_objeto(self, nombre_objeto):
        for i in range(len(self.lista_objetos)):
            if self.lista_objetos == nombre_objeto:
                self.lista_objetos.pop(i)
                

class Sala():

    def __init__(self):
        # una lista de texturas del fondo por si el mismo es animado
        self.fondo_texturas = []
        self.fondo_lista = arcade.SpriteList()
        self.fondo_sprite = None
        # una SpriteList de las paredes invisibles para las colisiones
        self.lista_bloqueos = arcade.SpriteList(use_spatial_hash=True)
        # una lista de los objetos interactuables para poder interactuar
        self.interactuables_sprites = arcade.SpriteList(use_spatial_hash=True)
        self.interactuables_objetos = []

        # una lista de los objetos capaces de levantar del suelo e integrarse en el inventario
        self.objetos_sprites = arcade.SpriteList(use_spatial_hash=True)
        self.objetos_objetos = []

        # una SpriteList de 'Salida' para saber que cuando el jugador lo toque se pasara al siguiente nivel
        self.lista_salida = arcade.SpriteList()

        # lista para los objetos capaces de eliminar al jugador, por defecto en none para que exista posibilidad de no haber
        self.lista_eliminadores = None

        # Como el inventario sera por sala aprevechamos y tendremos dicha info en esta clase
        self.inventario = Inventario()
    
    def Fondo(self, texturas_fondo: list[arcade.Texture]):
        if self.fondo_lista:
            self.fondo_lista.pop()
        self.fondo_texturas = texturas_fondo
        self.fondo_sprite = arcade.Sprite(self.fondo_texturas[0])
        self.fondo_lista.append(self.fondo_sprite)
        self.ancho = self.fondo_texturas[0].width
        self.alto = self.fondo_texturas[0].height
        self.fondo_sprite.center_x = self.ancho/2
        self.fondo_sprite.center_y = self.alto/2
    
    def Colisiones(self, paredes: list[dict]):

        for colision in paredes:
            pared = Bloqueo(int(colision["x"]), int(colision["y"]), int(colision["ancho"]), int(colision["alto"]))
            self.lista_bloqueos.append(pared)
    
    def Interactuables(self, interactuables: list[dict]):
        
        for interactuable in interactuables:
            # Creamos el objeto que interactua y genera pantallas emergentes
            objeto_interactuable = Interactuable(interactuable["nombre"], interactuable["textura"], interactuable["x"], interactuable["y"], funcion=interactuable["funcion"], ubicacion_jugador=interactuable.get("ubicacion_jugador"))
            self.lista_bloqueos.append(objeto_interactuable)


    def Salida(self, x, y, ancho, alto, funcion):
        self.salida = Salida(x, y, ancho, alto, funcion)
        self.lista_salida.append(self.salida)
    
    def Eliminadores(self, eliminadores):
        self.lista_eliminadores = arcade.SpriteList()
        for eliminador in eliminadores:
            self.lista_eliminadores.append(Objeto("eliminador", imagen_path=eliminador["imagen"], center_x = eliminador["x"], center_y=eliminador["y"]))

    def draw(self):
        self.fondo_lista.draw()
        self.interactuables_sprites.draw()
        self.lista_bloqueos.draw()